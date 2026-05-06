import os
import shutil
from consts import CONFIG_DIR
import yaml
from utils.cli import wait_for_user_confirmation 

__configs = {}

def has_no_configurations():
    return not os.path.exists(CONFIG_DIR)

def initialize_reinitialize_configurations(interactive: bool = True):
    # Check if the configuration directory exists
    if os.path.exists(CONFIG_DIR):
        if interactive:
            yes = wait_for_user_confirmation(f"Configuration directory already exists at {CONFIG_DIR}.\nDo you want to overwrite it?")
            if not yes:
                print("Aborting configuration initialization.")
                return

        shutil.rmtree(CONFIG_DIR)

    # Create the configuration directory
    if interactive:
        yes = wait_for_user_confirmation(f"Configuration directory will be created at {CONFIG_DIR}.\nDo you want to proceed?")
        if not yes:
            print("Aborting configuration initialization.")
            return
    os.makedirs(CONFIG_DIR)
    print(f"Configuration directory created at {CONFIG_DIR}")

    # default configs to write as yaml
    default_configs = {
        "default_template": "Default",
        "templates_dir": os.path.join(CONFIG_DIR, "templates")
    }

    # Copy `templates` to the config directory
    assets_dir = os.path.join(os.path.dirname(__file__), "../assets")
    shutil.copytree(os.path.join(assets_dir, "templates"), os.path.join(CONFIG_DIR, "templates"), dirs_exist_ok=True)

    # Write the default configurations to a YAML file
    with open(os.path.join(CONFIG_DIR, "config.yaml"), "w") as config_file:
        yaml.dump(default_configs, config_file)

def load_configurations(configs_file_path: str = None):
    global __configs

    if not configs_file_path:
        configs_file_path = os.path.join(CONFIG_DIR, "config.yaml")

    if not os.path.exists(configs_file_path):
        raise FileNotFoundError(f"Configurations file not found at {configs_file_path}. Please run 'yaml-to-resume init' to set up configurations.")

    with open(configs_file_path, "r") as config_file:
        __configs = yaml.safe_load(config_file)

    return __configs 

def get_configuration(key: str, default: any = None):
    return __configs.get(key, default)
