# CLI Tool Reference

The primary command is `yaml-to-resume` (alias `ytr`). If no subcommand is provided, the tool defaults to the `build` command.

## Subcommands

### 1. `build` (Default)
Converts YAML data into a PDF resume.

| Argument | Flag | Description | Always Present |
| :--- | :--- | :--- | :--- |
| `input_path` | (Positional) | Path to a `.yaml` file or directory | Yes |
| `--template` | `-t` | Template name or direct path to `layout.html` | No |
| `--output` | `-o` | Destination filename (.pdf) or directory | No |
| `--configs` | - | Path to a custom `config.yaml` override | No |
| `--verbose` | `-v` | Enable detailed logging for debugging | No |

**Examples:**
```bash
# Simple build
ytr resume.yaml

# Explicit build with template
ytr build resume.yaml --template Default

# Build with custom output
ytr resume.yaml -o exports/my_resume.pdf
```

---

### 2. `init`
Sets up the default configuration directory and base templates.

| Flag | Description |
| :--- | :--- |
| `-y` | Automatically confirm all prompts |

**Examples:**
```bash
# Standard initialization
ytr init

# Forced/Silent initialization
ytr init -y
```

---

### 3. `new`
Creates starter artifacts.

#### `new yaml`
| Argument | Description |
| :--- | :--- |
| `filename` | Name/path of the new YAML file |
| `--inherit` (`-i`) | Path to a YAML file to inherit from (can be used multiple times) |

**Example:**
```bash
ytr new yaml my_resume.yaml -i base.yaml
```

#### `new template`
| Argument | Flag | Description |
| :--- | :--- | :--- |
| `name` | (Positional) | Name of the new template folder |
| `--output` | `-o` | Custom directory to store the template |

**Example:**
```bash
ytr new template ModernStyle -o ./my_templates
```

---

### 4. `config`
Displays the current system configuration paths.

**Example:**
```bash
ytr config
```

---

---

## Configuration File

The `config.yaml` file (created during `init`) allows you to set global defaults.

| Key | Description | Default |
| :--- | :--- | :--- |
| `default_template` | The template used if none is specified. | `Default` |
| `default_inherit_strategy` | Global inheritance strategy (`extend`, `overwrite`). | `extend` |
| `templates_dir` | Path to the directory where templates are stored. | (System dependent) |

---

## Path Resolution
- **Linux:** `~/.config/yaml-to-resume/`
- **macOS:** `~/Library/Application Support/yaml-to-resume/`
- **Windows:** `C:\Users\<User>\AppData\Local\yaml-to-resume\`
