import yaml
import os
import copy
from typing import Any, Dict, List, Optional

from blocks import (
    Block, EducationBlock, ExperienceBlock, HeaderBlock, 
    ProjectsBlock, SkillsBlock, SummaryBlock
)
from consts import DEFAULT_TEMPLATE, DEFAULT_INHERIT_STRATEGY, INHERIT_STRATEGIES
from utils.configuration import get_configuration

class YAMLResume:
    """
    Handles loading, inheriting, and merging resume data from YAML files.
    Converts raw YAML data into structured Block objects for rendering.
    """

    BLOCK_MAP = {
        'header': HeaderBlock,
        'summary': SummaryBlock,
        'skills': SkillsBlock,
        'education': EducationBlock,
        'experience': ExperienceBlock,
        'projects': ProjectsBlock
    }

    def __init__(self, file_path: str = 'vars.yaml', verbose: bool = False):
        # Initialize directory context for relative path resolution
        self.current_dir = os.path.dirname(os.path.abspath(file_path))
        self.verbose = verbose
        
        # Load global defaults from configuration
        self._default_template = get_configuration('default_template', DEFAULT_TEMPLATE)
        self._default_strategy = get_configuration('default_inherit_strategy', DEFAULT_INHERIT_STRATEGY)

        # State for merging
        self._resume_vars: Dict[str, Any] = {}
        self._inherit_strategy = self._default_strategy
        
        # Load and process YAML files (handles inheritance)
        self._load_yaml_recursive(file_path)

        if not self._resume_vars:
            raise ValueError(f"No 'resume' key found in {file_path}")

        # Map merged variables to instance attributes
        self.name = self._resume_vars.get('name')
        self.job_title = self._resume_vars.get('job_title')
        self.output = self._resume_vars.get('output')
        self.template = self._resume_vars.get('template', self._default_template)
        
        if self.verbose:
            print(f"Final merged variables: {list(self._resume_vars.keys())}")

        # Cast raw content to block objects
        self.content = self._parse_content_blocks(self._resume_vars.get('content', []))

    def _resolve_path(self, path: str, base_dir: Optional[str] = None) -> str:
        """Resolves absolute paths, handling the '$' shortcut for current_dir."""
        if path.startswith("$"):
            return path.replace('$', base_dir or self.current_dir, 1)
        
        if os.path.isabs(path):
            return path
            
        return os.path.join(base_dir or os.getcwd(), path)

    def _load_yaml_recursive(self, vars_path: str, base_dir: Optional[str] = None):
        """Recursively loads YAML files following the 'inherit' chain."""
        full_path = self._resolve_path(vars_path, base_dir)
        
        if self.verbose:
            print(f"Loading YAML: {full_path}")

        if not os.path.exists(full_path):
            if self.verbose:
                print(f"Warning: File not found: {full_path}")
            return

        with open(full_path, 'r') as f:
            data = yaml.safe_load(f)
            if not data or 'resume' not in data:
                if self.verbose:
                    print(f"Warning: No 'resume' key in {full_path}")
                return

            resume_data = data['resume']
            file_dir = os.path.dirname(os.path.abspath(full_path))

            # Determine strategy for THIS file (local override > current state > default)
            strategy = resume_data.get('inherit_strategy', self._inherit_strategy)
            if strategy not in INHERIT_STRATEGIES:
                raise ValueError(f"Invalid strategy '{strategy}'. Use: {INHERIT_STRATEGIES}")

            # 1. Process inheritance first (bottom-up)
            inherit = resume_data.get('inherit')
            if inherit:
                parents = [inherit] if isinstance(inherit, str) else inherit
                if self.verbose:
                    print(f"Inheriting from: {parents}")
                for parent in parents:
                    self._load_yaml_recursive(parent, file_dir)

            # 2. Apply current file's variables using its resolved strategy
            if self.verbose:
                print(f"Merging {full_path} using strategy: {strategy}")
            self._merge_vars(resume_data, strategy)

    def _merge_vars(self, new_data: Dict[str, Any], strategy: str):
        """Applies the specified strategy to merge new_data into state."""
        skip = {'inherit', 'inherit_strategy'}
        
        for key, value in new_data.items():
            if key in skip:
                continue
                
            if key not in self._resume_vars:
                self._resume_vars[key] = copy.deepcopy(value)
                continue

            if strategy == 'extend':
                self._resume_vars[key] = self._extend_merge(self._resume_vars[key], value, key == 'content')
            else: # overwrite
                self._resume_vars[key] = self._overwrite_merge(self._resume_vars[key], value, key == 'content')

    @staticmethod
    def _extend_merge(base: Any, override: Any, is_content: bool = False) -> Any:
        """Deep merge: merges dicts, extends lists, overrides scalars."""
        if is_content and isinstance(base, list) and isinstance(override, list):
            if YAMLResume._is_keyed_list(base) and YAMLResume._is_keyed_list(override):
                return YAMLResume._merge_keyed_lists(base, override, strategy='extend')

        if isinstance(base, dict) and isinstance(override, dict):
            merged = copy.deepcopy(base)
            for k, v in override.items():
                merged[k] = YAMLResume._extend_merge(merged.get(k), v) if k in merged else copy.deepcopy(v)
            return merged

        if isinstance(base, list) and isinstance(override, list):
            return copy.deepcopy(base) + copy.deepcopy(override)

        return copy.deepcopy(override)

    @staticmethod
    def _overwrite_merge(base: Any, override: Any, is_content: bool = False) -> Any:
        """Deep merge for dicts, but replacement for lists and scalars."""
        if is_content and isinstance(base, list) and isinstance(override, list):
            if YAMLResume._is_keyed_list(base) and YAMLResume._is_keyed_list(override):
                return YAMLResume._merge_keyed_lists(base, override, strategy='overwrite')

        if isinstance(base, dict) and isinstance(override, dict):
            merged = copy.deepcopy(base)
            for k, v in override.items():
                merged[k] = YAMLResume._overwrite_merge(merged.get(k), v) if k in merged else copy.deepcopy(v)
            return merged

        return copy.deepcopy(override)

    @staticmethod
    def _merge_keyed_lists(base: List[Dict], override: List[Dict], strategy: str) -> List[Dict]:
        """Merges two lists of single-key dicts by matching their keys."""
        merged_map = {next(iter(item)): copy.deepcopy(item[next(iter(item))]) for item in base}
        order = [next(iter(item)) for item in base]

        for item in override:
            key = next(iter(item))
            if key in merged_map:
                if strategy == 'extend':
                    merged_map[key] = YAMLResume._extend_merge(merged_map[key], item[key])
                else: # overwrite
                    merged_map[key] = copy.deepcopy(item[key])
            else:
                merged_map[key] = copy.deepcopy(item[key])
                order.append(key)

        return [{k: merged_map[k]} for k in order]

    @staticmethod
    def _is_keyed_list(lst: List[Any]) -> bool:
        """Returns True if every item in the list is a dict with exactly one key."""
        return bool(lst) and all(isinstance(i, dict) and len(i) == 1 for i in lst)

    def _parse_content_blocks(self, content: List[Dict[str, Any]]) -> List[Block]:
        """Converts raw content dictionaries into Block objects."""
        if not isinstance(content, list):
            raise TypeError("Resume 'content' must be a list of blocks.")

        blocks = []
        for item in content:
            if not isinstance(item, dict) or len(item) != 1:
                raise ValueError("Each content item must be a dict with exactly one key (the block type).")

            type_name, data = next(iter(item.items()))
            block_cls = self.BLOCK_MAP.get(type_name)
            
            if not block_cls:
                raise ValueError(f"Unknown block type: {type_name}")

            # Special handling for complex blocks
            if type_name == 'header':
                blocks.append(self._create_header_block(data))
            elif type_name in ['education', 'experience', 'projects'] and isinstance(data, list):
                for entry in data:
                    if isinstance(entry, dict):
                        blocks.append(block_cls(**entry))
            elif isinstance(data, dict):
                blocks.append(block_cls(**data))
            else:
                blocks.append(block_cls(data))

        if self.verbose:
            print(f"Parsed {len(blocks)} content blocks.")

        return blocks

    def _create_header_block(self, data: Any) -> HeaderBlock:
        """Specialized logic for merging header data with name/job_title."""
        header_vars = {'name': self.name, 'job_title': self.job_title, 'extras': []}
        
        if isinstance(data, list):
            for item in data:
                if isinstance(item, dict):
                    header_vars.update(item)
                else:
                    header_vars['extras'].append(item)
        elif isinstance(data, dict):
            header_vars.update(data)
            
        return HeaderBlock(**header_vars)

    def get(self, key: str) -> Any:
        """Public accessor for merged resume variables."""
        if key == 'resume':
            return self._resume_vars
        if key not in self._resume_vars:
            raise KeyError(f"Variable '{key}' not found in resume data.")
        return self._resume_vars[key]
