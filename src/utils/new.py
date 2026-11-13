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
    
    # Use LaTeX as the default starter template
    latex_dir = os.path.join(base_dir, 'LaTeX')
    if not os.path.exists(latex_dir):
        assets_dir = os.path.join(os.path.dirname(__file__), "../assets/templates/LaTeX")
        if os.path.exists(assets_dir):
            latex_dir = assets_dir

    if os.path.exists(latex_dir):
        shutil.copytree(latex_dir, path)
        print(f"Created template {name} (based on LaTeX)")
        return

    os.makedirs(os.path.join(path, 'layout'), exist_ok=True)
    os.makedirs(os.path.join(path, 'css'), exist_ok=True)
    
    with open(os.path.join(path, 'css', 'style.css'), 'w') as f:
        f.write("@import url('https://fonts.cdnfonts.com/css/computer-modern');\n\n@page { size: A4; margin: 1.25cm 1.4cm; }\nbody { font-family: 'Computer Modern Serif', 'Latin Modern Roman', 'CMU Serif', 'DejaVu Serif', serif; font-size: 9.5pt; color: #000; }")

    with open(os.path.join(path, 'README.md'), 'w') as f:
        f.write(TEMPLATE_GUIDE)

    layout_content = """<!DOCTYPE html>
<html>
  <body>
    {% for block in blocks if block.block_type == 'header' %}{% include 'layout/header.html' %}{% endfor %}
    <main class="latex-content">
      {% for block in blocks if block.block_type == 'summary' %}
          {% if loop.first %}<section class="latex-section"><h2 class="latex-section-title">Summary</h2>{% endif %}
          {% include 'layout/summary.html' %}
          {% if loop.last %}</section>{% endif %}
      {% endfor %}
      {% for block in blocks if block.block_type == 'skills' %}
          {% if loop.first %}<section class="latex-section"><h2 class="latex-section-title">Technical Skills</h2>{% endif %}
          {% include 'layout/skills.html' %}
          {% if loop.last %}</section>{% endif %}
      {% endfor %}
      {% for block in blocks if block.block_type == 'experience' %}
          {% if loop.first %}<section class="latex-section"><h2 class="latex-section-title">Experience</h2>{% endif %}
          {% include 'layout/experience.html' %}
          {% if loop.last %}</section>{% endif %}
      {% endfor %}
      {% for block in blocks if block.block_type == 'education' %}
          {% if loop.first %}<section class="latex-section"><h2 class="latex-section-title">Education</h2>{% endif %}
          {% include 'layout/education.html' %}
          {% if loop.last %}</section>{% endif %}
      {% endfor %}
      {% for block in blocks if block.block_type == 'projects' %}
          {% if loop.first %}<section class="latex-section"><h2 class="latex-section-title">Projects</h2>{% endif %}
          {% include 'layout/projects.html' %}
          {% if loop.last %}</section>{% endif %}
      {% endfor %}
    </main>
  </body>
</html>"""

    header_content = """{% macro render_header_item(key, value) %}
    {% set val_str = value | string %}
    {% if val_str and ('@' in val_str or key == 'email') %}
        <a href="mailto:{{ value }}">{{ value }}</a>
    {% elif val_str and (val_str.startswith('+') or key == 'phone' or key == 'tel') %}
        <a href="tel:{{ value }}">{{ value }}</a>
    {% elif val_str and (val_str.startswith('http') or val_str.startswith('www') or '.com' in val_str or '.org' in val_str or '.net' in val_str or '.io' in val_str) %}
        {% set clean_link = value | replace('https://', '') | replace('http://', '') | replace('www.', '') %}
        {% if clean_link.endswith('/') %}{% set clean_link = clean_link[:-1] %}{% endif %}
        <a href="{{ value if val_str.startswith('http') else 'https://' ~ value }}">{{ key if (key and key not in ['link', 'url', 'portfolio', 'github', 'linkedin', 'website', 'other']) else clean_link }}</a>
    {% else %}
        <span>{{ value }}</span>
    {% endif %}
{% endmacro %}

<header class="latex-header">
    <h1 class="latex-name">{{ name }}</h1>
    {% if job_title %}<div class="latex-title">{{ job_title }}</div>{% endif %}
    <div class="latex-contacts">
        {% for block in blocks if block.block_type == 'header' %}
            {% for key, value in block.other_info.items() %}
                <span class="latex-contact-item">{{ render_header_item(key, value) }}</span>
            {% endfor %}
            {% for extra in block.extras %}
                <span class="latex-contact-item">{{ render_header_item('', extra) }}</span>
            {% endfor %}
        {% endfor %}
    </div>
</header>"""

    files = {
        'layout/layout.html': layout_content,
        'layout/header.html': header_content,
        'layout/summary.html': '<div class="latex-summary"><p>{{ block.summary | format_text }}</p></div>',
        'layout/skills.html': """<div class="latex-skills">
    <ul class="latex-skills-list">
        {% for skill in block.skills %}
        <li>
            {% if ':' in skill %}
                {% set parts = skill.split(':', 1) %}
                <strong>{{ parts[0] }}:</strong>{{ parts[1] }}
            {% else %}
                {{ skill }}
            {% endif %}
        </li>
        {% endfor %}
    </ul>
</div>""",
        'layout/experience.html': """<div class="latex-entry">
    <div class="latex-entry-header">
        <div class="latex-entry-row">
            <span class="latex-bold">{{ block.company }}</span>
            {% if block.location %}<span class="latex-italic">{{ block.location }}</span>{% endif %}
        </div>
        <div class="latex-entry-row">
            <span class="latex-italic">{{ block.job_title }}</span>
            {% if block.date_range %}<span class="latex-date">{{ block.date_range }}</span>{% endif %}
        </div>
    </div>
    {% if block.description %}
        {% if block.description is string %}
            <p class="latex-entry-desc">{{ block.description | format_text }}</p>
        {% else %}
            <ul class="latex-bullets">
                {% for line in block.description %}
                <li>{{ line | format_text }}</li>
                {% endfor %}
            </ul>
        {% endif %}
    {% endif %}
</div>""",
        'layout/education.html': """<div class="latex-entry">
    <div class="latex-entry-header">
        <div class="latex-entry-row">
            <span class="latex-bold">{{ block.institution }}</span>
            {% if block.date %}<span class="latex-date">{{ block.date }}</span>{% endif %}
        </div>
        <div class="latex-entry-row">
            <span class="latex-italic">{{ block.degree }}{% if block.field_of_study %} &mdash; {{ block.field_of_study }}{% endif %}</span>
            {% if block.location %}<span class="latex-italic">{{ block.location }}</span>{% endif %}
        </div>
    </div>
    {% if block.description %}
        {% if block.description is string %}
            <p class="latex-entry-desc">{{ block.description | format_text }}</p>
        {% else %}
            <ul class="latex-bullets">
                {% for line in block.description %}
                <li>{{ line | format_text }}</li>
                {% endfor %}
            </ul>
        {% endif %}
    {% endif %}
</div>""",
        'layout/projects.html': """<div class="latex-entry">
    <div class="latex-entry-header">
        <div class="latex-entry-row">
            <span class="latex-bold">{{ block.title }}</span>
            {% if block.date %}<span class="latex-date">{{ block.date }}</span>{% endif %}
        </div>
    </div>
    {% if block.description %}
        {% if block.description is string %}
            <p class="latex-entry-desc">{{ block.description | format_text }}</p>
        {% else %}
            <ul class="latex-bullets">
                {% for line in block.description %}
                <li>{{ line | format_text }}</li>
                {% endfor %}
            </ul>
        {% endif %}
    {% endif %}
</div>"""
    }

    for rel_path, content in files.items():
        with open(os.path.join(path, rel_path), 'w') as f: f.write(content)
    print(f"Created template {name} (based on LaTeX)")
