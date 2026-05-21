# CLI Tool Reference

The primary command is `yaml-to-resume`. If no subcommand is provided, the tool defaults to the `build` command.

## Subcommands

### 1. `build` (Default)
Converts YAML data into a PDF resume.

| Argument | Flag | Description | Always Present |
| :--- | :--- | :--- | :--- |
| `input_path` | (Positional) | Path to a `.yaml` file or directory | Yes |
| `--template` | `-t` | Template name or direct path to `layout.html` | No |
| `--output` | `-o` | Destination filename (.pdf) or directory | No |
| `--configs` | - | Path to a custom `config.yaml` override | No |

**Examples:**
```bash
# Simple build
yaml-to-resume resume.yaml

# Explicit build with template
yaml-to-resume build resume.yaml --template Default

# Build with custom output
yaml-to-resume resume.yaml -o exports/my_resume.pdf
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
yaml-to-resume init

# Forced/Silent initialization
yaml-to-resume init -y
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
yaml-to-resume new yaml my_resume.yaml -i base.yaml
```

#### `new template`
| Argument | Flag | Description |
| :--- | :--- | :--- |
| `name` | (Positional) | Name of the new template folder |
| `--output` | `-o` | Custom directory to store the template |

**Example:**
```bash
yaml-to-resume new template ModernStyle -o ./my_templates
```

---

### 4. `config`
Displays the current system configuration paths.

**Example:**
```bash
yaml-to-resume config
```

---

## Path Resolution
- **Linux:** `~/.config/yaml-to-resume/`
- **macOS:** `~/Library/Application Support/yaml-to-resume/`
- **Windows:** `C:\Users\<User>\AppData\Local\yaml-to-resume\`
