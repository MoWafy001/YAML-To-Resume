from consts import CONFIG_DIR
from utils.cli import parse_cli_arguments
from utils.configuration import get_configuration, has_no_configurations, initialize_reinitialize_configurations, load_configurations
from utils.pdf import create_resume_or_resumes
from utils.new import create_new_template, create_new_yaml_resume


def handle_init_command(cli_arguments):
    initialize_reinitialize_configurations(cli_arguments.y)


def handle_config_command(_):
    print("Configuration files are located at:", CONFIG_DIR)


def handle_build_command(cli_arguments):
    create_resume_or_resumes(
        cli_arguments.input_path,
        cli_arguments.template,
        cli_arguments.output
    )


def handle_new_command(cli_arguments):
    if cli_arguments.new_type == "yaml":
        create_new_yaml_resume(cli_arguments.filename, cli_arguments.inherit)
    elif cli_arguments.new_type == "template":
        create_new_template(cli_arguments.name, cli_arguments.output)
    else:
        raise ValueError(f"Unknown new type: {cli_arguments.new_type}")


def handle_command(cli_arguments):
    command = {
        "init": handle_init_command,
        "config": handle_config_command,
        "build": handle_build_command,
        "new": handle_new_command
    }.get(cli_arguments.command)

    if command:
        command(cli_arguments)
    else:
        raise ValueError(f"Unknown command: {cli_arguments.command}")


def run():
    cli_arguments = parse_cli_arguments()

    # Initialize configurations if needed
    if has_no_configurations():
        initialize_reinitialize_configurations()
        return

    # Load configurations
    load_configurations(
        configs_file_path=cli_arguments.configs if 'configs' in cli_arguments else None
    )

    handle_command(cli_arguments)

if __name__ == "__main__":
    run()