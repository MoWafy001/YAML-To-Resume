import os
import yaml
import shutil
from utils.configuration import get_configuration

YAML_BOILERPLATE = """# YAML Resume Boilerplate
resume:
  # inherit: "base_resume.yaml"
  name: "Your Name"
  job_title: "Your Job Title"
  output: "resume.pdf"
  primary_color: "008080"
  content:
    - header:
      - location: "City, State"
      - email: "your.email@example.com"
      - phone: "(123) 456-7890"
    - summary: "A brief summary."
    - skills: ["Python", "Jinja2"]
    - experience:
      - company: "Company Name"
        job_title: "Job Title" # Alternative: role
        date_range: "Jan 2020 - Present" # Alternative: duration
        location: "City, State"
        description: ["Task 1", "Task 2"]
    - education:
      - degree: "Degree Name"
        institution: "University Name"
        date: "May 2019"
        field_of_study: "Computer Science"
    # Note: Many fields have alternatives (e.g., 'role' for 'job_title'). 
    # See docs/yaml_resume.md for the full list.
"""

TEMPLATE_GUIDE = """# Template Context Reference

## Global Variables
| Variable | Type | Description | Always Present |
| :--- | :--- | :--- | :--- |
| `name` | string | Full name from resume | Yes |
| `job_title` | string | Professional title | Yes |
| `primary_color` | string | Hex color (e.g., "008080") | No |
| `blocks` | list | List of all Block objects | Yes |
| `[key]` | any | Any other top-level key from the `resume` object (spaces -> `_`) | No |

## Block Reference (`block.block_type`)

### `header`
| Attribute | Type | Description | Always Present |
| :--- | :--- | :--- | :--- |
| `name` | string | Full name | Yes |
| `job_title` | string | Job title | Yes |
| `profile_picture` | string | Image path/URL | No |
| `extras` | list | List of unkeyed strings | Yes |
| `other_info` | dict | Dictionary of all key-value pairs | Yes |

### `summary`
| Attribute | Type | Description | Always Present |
| :--- | :--- | :--- | :--- |
| `summary` | string | The summary text | Yes |

### `skills`
| Attribute | Type | Description | Always Present |
| :--- | :--- | :--- | :--- |
| `skills` | list | List of skill strings | Yes |

### `experience`
| Attribute | Type | Description | Always Present |
| :--- | :--- | :--- | :--- |
| `job_title` | string | Role title | Yes |
| `company` | string | Company name | Yes |
| `location` | string | Location string | No |
| `date_range` | string | Duration string | Yes |
| `description` | string | list | Bullet points or block text | Yes |

### `education`
| Attribute | Type | Description | Always Present |
| :--- | :--- | :--- | :--- |
| `degree` | string | Degree obtained | Yes |
| `institution` | string | School name | Yes |
| `field_of_study` | string | Major area | No |
| `date` | string | Graduation date | No |
| `description` | string | Optional details | No |

### `projects`
| Attribute | Type | Description | Always Present |
| :--- | :--- | :--- | :--- |
| `title` | string | Project name | Yes |
| `date` | string | Completion date | No |
| `description` | string | Project details | Yes |

## Implementation Patterns

### Iterating Specific Blocks
```html
{% for block in blocks if block.block_type == 'experience' %}
  <div>{{ block.company }}</div>
{% endfor %}
```

### Handling String vs List (Description)
```html
{% if block.description is string %}
  <p>{{ block.description | format_text }}</p>
{% else %}
  <ul>
    {% for point in block.description %}
      <li>{{ point | format_text }}</li>
    {% endfor %}
  </ul>
{% endif %}
```

## CSS Styling
The following CSS variables are automatically injected:
- `var(--primary-color)`: The hex color from YAML.
- `var(--primary-color-light)`: Hex + "66" opacity.
- `var(--primary-color-very-light)`: Hex + "11" opacity.
"""

def create_new_yaml_resume(filename, inherit=None):
    if not filename.endswith(('.yaml', '.yml')): filename += '.yaml'
    if os.path.exists(filename): return print(f"File {filename} exists.")
    
    if not inherit:
        with open(filename, 'w') as f: f.write(YAML_BOILERPLATE.strip())
    else:
        data = yaml.safe_load(YAML_BOILERPLATE)
        data['resume']['inherit'] = inherit[0] if len(inherit) == 1 else inherit
        with open(filename, 'w') as f: yaml.dump(data, f, sort_keys=False)
    print(f"Created {filename}")

def create_new_template(name, output_dir=None):
    base_dir = output_dir if output_dir else get_configuration('templates_dir')
    path = os.path.join(base_dir, name)
    if os.path.exists(path): return print(f"Template {name} exists.")
    
    os.makedirs(os.path.join(path, 'layout'), exist_ok=True)
    os.makedirs(os.path.join(path, 'css'), exist_ok=True)
    
    with open(os.path.join(path, 'css', 'style.css'), 'w') as f:
        f.write("body { font-family: sans-serif; }\na { color: var(--primary-color, #008080); text-decoration: none; }\na:hover { opacity: 0.8; }")

    with open(os.path.join(path, 'README.md'), 'w') as f:
        f.write(TEMPLATE_GUIDE)

    layout_content = """<html>
  <body>
    {% for block in blocks if block.block_type == 'header' %}{% include 'layout/header.html' %}{% endfor %}
    <div class="content">
      {% for block in blocks if block.block_type == 'summary' %}{% include 'layout/summary.html' %}{% endfor %}
      {% for block in blocks if block.block_type == 'skills' %}{% include 'layout/skills.html' %}{% endfor %}
      {% for block in blocks if block.block_type == 'experience' %}
          {% if loop.first %}<section class="experience"><h1>Experience</h1>{% endif %}
          {% include 'layout/experience.html' %}
          {% if loop.last %}</section>{% endif %}
      {% endfor %}
    </div>
  </body>
</html>"""

    header_content = """{% macro render_header_item(key, value) %}
    {% set val_str = value | string %}
    {% if val_str and ('@' in val_str or key == 'email') %}
        <a href="mailto:{{ value }}">{{ value }}</a>
    {% elif val_str and (val_str.startswith('+') or key == 'phone' or key == 'tel') %}
        <a href="tel:{{ value }}">{{ value }}</a>
    {% elif val_str and (val_str.startswith('http') or val_str.startswith('www') or '.com' in val_str or '.org' in val_str or '.net' in val_str) %}
        <a href="{{ value if val_str.startswith('http') else 'http://' ~ value }}">{{ key if (key and key != 'link' and key != 'url') else value }}</a>
    {% else %}
        <span>{{ value }}</span>
    {% endif %}
{% endmacro %}

<header>
    <h1>{{ name }}</h1>
    <h2>{{ job_title }}</h2>
    <div class="links">
        {% for block in blocks if block.block_type == 'header' %}
            {% for key, value in block.other_info.items() %}
                {{ render_header_item(key, value) }}
            {% endfor %}
            {% for extra in block.extras %}
                {{ render_header_item('', extra) }}
            {% endfor %}
        {% endfor %}
    </div>
</header>"""

    files = {
        'layout/layout.html': layout_content,
        'layout/header.html': header_content,
        'layout/summary.html': "<div>{{ block.summary | format_text }}</div>",
        'layout/skills.html': "<ul>{% for s in block.skills %}<li>{{ s }}</li>{% endfor %}</ul>",
        'layout/experience.html': """<div>
    <h2>{{ block.job_title }} at {{ block.company }}</h2>
    {% if block.description is string %}
        <p>{{ block.description | format_text }}</p>
    {% else %}
        <ul>{% for line in block.description %}<li>{{ line | format_text }}</li>{% endfor %}</ul>
    {% endif %}
</div>""",
        'layout/education.html': "",
        'layout/projects.html': ""
    }

    for rel_path, content in files.items():
        with open(os.path.join(path, rel_path), 'w') as f: f.write(content)
    print(f"Created template {name}")
