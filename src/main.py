from consts import CONFIG_DIR
from utils.cli import parse_cli_arguments
from utils.configuration import get_configuration, has_no_configurations, initialize_reinitialize_configurations, load_configurations
from utils.pdf import create_resume


def run():
    cli_arguments = parse_cli_arguments()

    # Initialize configurations if needed
    if cli_arguments.command == "init" or has_no_configurations():
        initialize_reinitialize_configurations(
            interactive=cli_arguments.y is False
        )
        return
    
    # config mode
    if cli_arguments.command == "config":
        print("Configuration files are located at:", CONFIG_DIR)
        return

    # Load configurations
    load_configurations(
        configs_file_path=cli_arguments.configs # if None, will default to CONFIG_DIR
    )

    # build mode
    if cli_arguments.command == "build":
        template_to_use = cli_arguments.template if cli_arguments.template else get_configuration('default_template')

        create_resume(
            cli_arguments.input_path,
            template_to_use,
            cli_arguments.output # can be None
        )
        return

if __name__ == "__main__":
    run()