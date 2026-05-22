<img width="930" height="589" alt="image" src="https://github.com/user-attachments/assets/34d729cc-bfb1-457a-bc40-68dcd681760b" />

# YAML-To-Resume (`ytr`)

Generate professional PDF resumes from simple YAML files using Jinja2 templates.

## Key Features

- **Advanced Inheritance**: Compose resumes from multiple YAML files.
- **Deep Merging**: Intelligently merge nested data and content blocks.
- **Multiple Strategies**: Choose between `extend` (deep merge + list append) or `overwrite` (deep merge + list replacement).
- **Verbose Logging**: Use the `-v` flag to debug the build process and inheritance chain.
- **Custom Templates**: Easily create and use your own Jinja2 templates.

## Quick Start

### 1. Install
```bash
pip install yaml-to-resume
```

### 2. Initialize
```bash
# You can use the full command or the alias 'ytr'
ytr init -y
```

### 3. Build Resume
```bash
# 'build' is the default command, so you can just pass the file
ytr examples/01-basic/resume.yaml
```

---

## Documentation

Comprehensive technical references are available in the [docs/](docs/) folder:

- **[CLI Tool Reference](docs/cli.md)**: Detailed command usage, flags, and subcommands.
- **[YAML Resume Schema](docs/yaml_resume.md)**: Full specification for writing resume data files, including all supported block types.
- **[Template Development Guide](docs/templates.md)**: Technical guide for creating and modifying Jinja2 templates.

---

## Examples

For progressive examples ranging from basic to advanced inheritance, see the [examples/](examples/) directory.
