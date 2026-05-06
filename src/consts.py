from platformdirs import PlatformDirs

APP_NAME = "yaml-to-resume"
CONFIG_DIR = PlatformDirs(APP_NAME).user_config_dir