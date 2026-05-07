import yaml
import os

from blocks import Block, EducationBlock, ExperienceBlock, HeaderBlock, ProjectsBlock, SkillsBlock, SummaryBlock

class YAMLResume:
    def __init__(self, file_path='vars.yaml'):
        if file_path.startswith('/'):
            self.current_dir = '/'.join(file_path.split('/')[:-1])
        else:
            self.current_dir = os.getcwd() + '/' + \
                '/'.join(file_path.split('/')[:-1])

        self.__vars_d = {}
        self.__open_yaml(file_path)

        self.__resume = self.get('resume')
        if not self.__resume:
            raise Exception('Missing the `resume` key')

        self.name = self.__resume.get('name')
        self.job_title = self.__resume.get('job title')
        self.output = self.__resume.get('output')
        self.content = self.__cast_to_blocks(self.__resume.get('content'))

    def __open_yaml(self, vars_path, vars_path_dir=None):
        if vars_path.startswith("$"):
            vars_path = vars_path.replace(
                '$', self.current_dir if vars_path_dir is None else vars_path_dir, 1)

        with open(vars_path) as f:
            loaded_vars = yaml.safe_load(f)
            self.__apply_vars(loaded_vars)

            self.__load_inherited_vars(vars_path)

    def __apply_vars(self, loaded_vars):
        # only apply vars if they are not already in vars_d
        for key, value in loaded_vars.items():
            if key not in self.__vars_d:
                self.__vars_d[key] = value

    def __load_inherited_vars(self, vars_path):
        if 'inherit' not in self.__vars_d:
            return
        vars_path = '/'.join(vars_path.split('/')[:-1])

        inherit = self.__vars_d['inherit']

        # remove inherit from vars_d
        self.__vars_d.pop('inherit')

        # if inherit is a list
        if isinstance(inherit, list):
            for i in inherit:
                self.__open_yaml(i, vars_path)

        # if inherit is a string
        if isinstance(inherit, str):
            self.__open_yaml(inherit, vars_path)

    
    def __cast_to_blocks(self, content):
        if not content:
            return []

        if type(content) is not list:
            raise TypeError('Content must be a list')

        blocks: list[Block] = []
        for item in content:
            if not isinstance(item, dict):
                raise TypeError('Each item in content must be a dict')
            
            # the dict should have one key
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

            # find the block class based on the block name
            block_class = blockname_to_class.get(block_name)
            if not block_class:
                raise ValueError(f'Unknown block type: {block_name}')

            if block_name in ['education', 'experience', 'projects'] and isinstance(block_data, list):
                for sub_item in block_data:
                    blocks.append(block_class(**sub_item))
            elif block_name == 'header' and isinstance(block_data, list):
                header_data = {}
                for sub_item in block_data:
                    if isinstance(sub_item, dict):
                        header_data.update(sub_item)
                blocks.append(block_class(name=self.name, job_title=self.job_title, **header_data))
            elif isinstance(block_data, dict):
                blocks.append(block_class(**block_data))
            else:
                blocks.append(block_class(block_data))

        return blocks

    def get(self, var_name):
        if var_name not in self.__vars_d:
            raise Exception(f'({var_name}) not found')
        else:
            return self.__vars_d[var_name]
