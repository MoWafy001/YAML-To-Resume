import yaml
import os

class YAMLResume:
    def __init__(self, file_path='vars.yaml'):
        if file_path.startswith('/'):
            self.current_dir = '/'.join(file_path.split('/')[:-1])
        else:
            self.current_dir = os.getcwd() + '/' + \
                '/'.join(file_path.split('/')[:-1])

        self.vars_d = {}
        self.open_yaml(file_path)

    def open_yaml(self, vars_path, vars_path_dir=None):
        if vars_path.startswith("$"):
            vars_path = vars_path.replace(
                '$', self.current_dir if vars_path_dir is None else vars_path_dir, 1)

        with open(vars_path) as f:
            loaded_vars = yaml.safe_load(f)
            self.apply_vars(loaded_vars)

            self.loadInheritedVars(vars_path)

    def apply_vars(self, loaded_vars):
        # only apply vars if they are not already in vars_d
        for key, value in loaded_vars.items():
            if key not in self.vars_d:
                self.vars_d[key] = value

    def loadInheritedVars(self, vars_path):
        if 'inherit' not in self.vars_d:
            return
        vars_path = '/'.join(vars_path.split('/')[:-1])

        inherit = self.vars_d['inherit']

        # remove inherit from vars_d
        self.vars_d.pop('inherit')

        # if inherit is a list
        if isinstance(inherit, list):
            for i in inherit:
                self.open_yaml(i, vars_path)

        # if inherit is a string
        if isinstance(inherit, str):
            self.open_yaml(inherit, vars_path)

    def get(self, var_name):
        if var_name not in self.vars_d:
            raise Exception(f'({var_name}) not found')
        else:
            return self.vars_d[var_name]
