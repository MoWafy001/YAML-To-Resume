import argparse


def wait_for_user_confirmation(prompt: str) -> bool:
    response = input(prompt + " (y/n): ")
    return response.lower() == "y"


def parse_cli_arguments():
    """
    Parse command-line arguments for the YAML to Resume converter.
    Uses subcommands to separate initialization from the conversion logic.
    
    returns: argparse.Namespace with a 'command' attribute to distinguish 
             between 'init' and 'build'.
    """
    parser = argparse.ArgumentParser(
        prog="yaml-to-resume",
        description="A CLI tool to convert YAML data into PDF resumes using customizable templates."
    )

    # Creating the subparser handler
    subparsers = parser.add_subparsers(
        dest="command", 
        required=True, 
        help="Available commands"
    )

    # --- 'init' Command ---
    init_parser = subparsers.add_parser(
        'init', 
        help="Initialize the application environment."
    )
    init_parser.description = (
        "Sets up the default configuration directory and copies base "
        "templates to your local config path (e.g., ~/.config/yaml-to-resume/)."
    )

    # auto yes
    init_parser.add_argument(
        "-y",
        action="store_true",
        help="Automatically confirm all prompts."
    )

    # --- 'config' Command ---
    config_parser = subparsers.add_parser(
        'config',
        help="Manage configuration settings."
    )
    config_parser.description = (
        "Displays the location of configuration files. Use this command to find where your templates and config.yaml are stored."
    )

    # --- 'build' Command ---
    build_parser = subparsers.add_parser(
        'build', 
        help="Convert YAML data into a PDF resume."
    )
    build_parser.description = (
        "Takes a YAML file or directory and processes it into a finished PDF. "
        "Allows for template selection and custom output paths."
    )

    # Build: Positional Argument
    build_parser.add_argument(
        "input_path", 
        type=str, 
        help="Path to a specific .yaml file or a directory containing multiple YAML files."
    )

    # Build: Template Options
    build_parser.add_argument(
        "--template", "-t",
        help="Name of a built-in template (e.g., 'modern') or a direct path to a custom .html template."
    )

    # Build: Configs
    build_parser.add_argument(
        "--configs", 
        help="Path to a custom YAML configuration file to override default behavior."
    )

    # Build: Output
    build_parser.add_argument(
        "-o", "--output", 
        help="The destination path. Can be a filename (ending in .pdf) or a directory path."
    )

    return parser.parse_args()