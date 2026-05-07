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

### 3. Create a New Resume
```bash
yaml-to-resume new yaml my_resume.yaml
```

### 4. Build PDF
```bash
yaml-to-resume build my_resume.yaml
```

---

## Usage Examples

### Create a Custom Template
```bash
# Create a starter template in the default directory
yaml-to-resume new template MyModernStyle

# Or specify a custom directory
yaml-to-resume new template MyStyle --output ./templates
```

### Build with Options
```bash
# Use a specific template
yaml-to-resume build my_resume.yaml --template Default

# Custom output filename
yaml-to-resume build my_resume.yaml -o professional_resume.pdf

# Custom output directory
yaml-to-resume build my_resume.yaml -o ./exports/
```

---

## YAML Structure Example (my_resume.yaml)

```yaml
resume:
  name: "John Doe"
  job title: "Software Engineer"
  primary color: "008080" # Hex color for templates that support it
  content:
    - header:
        - email: "john.doe@example.com"
        - LinkedIn: "https://linkedin.com/in/johndoe"
        - location: "New York, NY"

    - summary: |
        Experienced software engineer with a focus on Python and Cloud architecture.

    - skills:
        - Python
        - Docker
        - AWS
        - Jinja2

    - experience:
        - company: "Tech Corp"
          role: "Senior Developer"
          duration: "2020 - Present"
          description:
            - Led a team of 5 to migrate legacy systems to AWS.
            - Reduced CI/CD pipeline time by 40%.

    - education:
        - institution: "State University"
          degree: "B.S. Computer Science"
          date: "2019"
```

---

## Configuration
Templates and global configs are stored in:
- Linux: `~/.config/yaml-to-resume/`
- macOS: `~/Library/Application Support/yaml-to-resume/`
- Windows: `C:\Users\<User>\AppData\Local\yaml-to-resume\`

To find your config path:
```bash
yaml-to-resume config
```
