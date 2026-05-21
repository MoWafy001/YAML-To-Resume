<img width="914" height="721" alt="image" src="https://github.com/user-attachments/assets/958cb01e-ec57-4415-b336-d7e2f9289c4e" />

# YAML-To-Resume

Generate professional PDF resumes from simple YAML files using Jinja2 templates.

## Quick Start

### 1. Install
```bash
git clone https://github.com/MoWafy001/YAML-To-Resume.git
cd YAML-To-Resume
pip install -e .
```

### 2. Initialize
```bash
yaml-to-resume init -y
```

### 3. Build Resume
```bash
# 'build' is the default command, so you can just pass the file
yaml-to-resume examples/01-basic/resume.yaml
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
