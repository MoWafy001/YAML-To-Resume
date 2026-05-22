import yaml
import os
import copy

from blocks import Block, EducationBlock, ExperienceBlock, HeaderBlock, ProjectsBlock, SkillsBlock, SummaryBlock
from consts import DEFAULT_TEMPLATE

class YAMLResume:
    def __init__(self, file_path='vars.yaml'):
        if file_path.startswith('/'):
            self.current_dir = '/'.join(file_path.split('/')[:-1])
        else:
            self.current_dir = os.getcwd() + '/' + \
                '/'.join(file_path.split('/')[:-1])

        self.__resume_vars = {}
        self.__open_yaml(file_path)

        if not self.__resume_vars:
            raise Exception('Missing the `resume` key')

        # Use snake_case keys consistently
        self.name = self.__resume_vars.get('name')
        self.job_title = self.__resume_vars.get('job_title')
        self.output = self.__resume_vars.get('output')
        self.content = self.__cast_to_blocks(self.__resume_vars.get('content'))
        self.template = self.__resume_vars.get('template') if 'template' in self.__resume_vars else DEFAULT_TEMPLATE

    def __open_yaml(self, vars_path, vars_path_dir=None):
        if vars_path.startswith("$"):
            vars_path = vars_path.replace(
                '$', self.current_dir if vars_path_dir is None else vars_path_dir, 1)
        
        if not os.path.isabs(vars_path):
            if vars_path_dir:
                vars_path = os.path.join(vars_path_dir, vars_path)
            else:
                vars_path = os.path.join(os.getcwd(), vars_path)

        if not os.path.exists(vars_path):
             return

        with open(vars_path) as f:
            loaded_data = yaml.safe_load(f)
            if not loaded_data or 'resume' not in loaded_data:
                return

            resume_data = loaded_data['resume']

            if 'inherit' in resume_data:
                inherit = resume_data['inherit']
                current_file_dir = os.path.dirname(os.path.abspath(vars_path))
                
                if isinstance(inherit, list):
                    for i in inherit:
                        self.__open_yaml(i, current_file_dir)
                elif isinstance(inherit, str):
                    self.__open_yaml(inherit, current_file_dir)

            self.__apply_resume_vars(resume_data)

    @staticmethod
    def __is_keyed_list(lst):
        """Check if a list is a 'keyed list' — every item is a dict with exactly one key."""
        return (
            len(lst) > 0
            and all(isinstance(item, dict) and len(item) == 1 for item in lst)
        )

    @staticmethod
    def __deep_merge(base, override):
        """
        Recursively deep-merge override into base.
        - For dicts: keys from override take precedence; shared keys are merged recursively.
        - For keyed lists (lists of single-key dicts): items are matched and merged by
          their dict key. New keys from override are appended. Base-only keys are kept.
        - For other lists: override replaces base entirely.
        - For all other types: override wins.
        """
        if isinstance(base, dict) and isinstance(override, dict):
            merged = copy.deepcopy(base)
            for key, value in override.items():
                if key in merged:
                    merged[key] = YAMLResume.__deep_merge(merged[key], value)
                else:
                    merged[key] = copy.deepcopy(value)
            return merged

        if isinstance(base, list) and isinstance(override, list):
            # Keyed-list merge: match items by their single dict key
            if YAMLResume.__is_keyed_list(base) and YAMLResume.__is_keyed_list(override):
                # Build an ordered dict from base items
                merged_keys = {}
                merged_order = []
                for item in base:
                    key = next(iter(item))
                    merged_keys[key] = copy.deepcopy(item[key])
                    merged_order.append(key)

                for item in override:
                    key = next(iter(item))
                    if key in merged_keys:
                        # Deep-merge the value for this key
                        merged_keys[key] = YAMLResume.__deep_merge(
                            merged_keys[key], item[key]
                        )
                    else:
                        merged_keys[key] = copy.deepcopy(item[key])
                        merged_order.append(key)

                return [{k: merged_keys[k]} for k in merged_order]

            # For regular lists, override replaces base
            return copy.deepcopy(override)

        # For scalars (str, int, etc.) or mismatched types, override wins
        return copy.deepcopy(override)

    def __apply_resume_vars(self, resume_data):
        for key, value in resume_data.items():
            if key == 'inherit':
                continue
            if key in self.__resume_vars:
                self.__resume_vars[key] = YAMLResume.__deep_merge(
                    self.__resume_vars[key], value
                )
            else:
                self.__resume_vars[key] = copy.deepcopy(value)

    def __cast_to_blocks(self, content):
        if not content:
            return []

        if type(content) is not list:
            raise TypeError('Content must be a list')

        blocks: list[Block] = []
        for item in content:
            if not isinstance(item, dict):
                raise TypeError('Each item in content must be a dict')
            
            d_keys = list(item.keys())
            if len(d_keys) != 1:
                raise ValueError('Each item in content must have exactly one key')

            block_name = d_keys[0]
            block_data = item[block_name]
            blockname_to_class = {
                'header': HeaderBlock,
                'summary': SummaryBlock,
                'skills': SkillsBlock,
                'education': EducationBlock,
                'experience': ExperienceBlock,
                'projects': ProjectsBlock
            }

            block_class = blockname_to_class.get(block_name)
            if not block_class:
                raise ValueError(f'Unknown block type: {block_name}')

            if block_name in ['education', 'experience', 'projects'] and isinstance(block_data, list):
                for sub_item in block_data:
                    if isinstance(sub_item, dict):
                        blocks.append(block_class(**sub_item))
            elif block_name == 'header' and isinstance(block_data, list):
                header_data = {}
                extras = []
                for sub_item in block_data:
                    if isinstance(sub_item, dict):
                        header_data.update(sub_item)
                    else:
                        extras.append(sub_item)
                
                merged_header = {'name': self.name, 'job_title': self.job_title, 'extras': extras}
                merged_header.update(header_data)
                blocks.append(block_class(**merged_header))
            elif isinstance(block_data, dict):
                blocks.append(block_class(**block_data))
            else:
                blocks.append(block_class(block_data))

        return blocks

    def get(self, var_name):
        if var_name == 'resume':
            return self.__resume_vars
        if var_name not in self.__resume_vars:
            raise Exception(f'({var_name}) not found')
        else:
            return self.__resume_vars[var_name]
