import os
import yaml
import shutil
from utils.configuration import get_configuration

YAML_BOILERPLATE = """# YAML Resume Boilerplate
# This file defines the structure and content of your resume.
# You can use standard YAML syntax to organize your information.

resume:
  # Inheritance: Use this to base your resume on another YAML file.
  # Helpful for maintaining a master resume and creating custom versions for specific jobs.
  # inherit: "base_resume.yaml" # can be a string or a list of filenames
  
  name: "Your Name"
  job title: "Your Job Title"
  output: "resume.pdf" # The default name for the generated PDF
  
  # Content: List of blocks to be rendered in the resume.
  # Supported block types: header, summary, skills, experience, education, projects.
  content:
    - header:
      # Common header fields. Templates may support more.
      - location: "City, State"
      - email: "your.email@example.com"
      - phone: "(123) 456-7890"
      
    - summary: |
        A brief, compelling summary of your professional background, 
        key achievements, and career goals.
        
    - skills: 
      - Python
      - Jinja2
      - YAML
      
    - experience:
      - company: "Company Name"
        role: "Job Title"
        duration: "Jan 2020 - Present"
        location: "City, State"
        description:
          - Achieved X by doing Y, resulting in Z.
          - Collaborated with team A to implement feature B.
          
    - education:
      - degree: "Bachelor of Science in Computer Science"
        institution: "University Name"
        date: "May 2019"
        field_of_study: "Computer Science"
        description: "GPA: 3.8/4.0, Honors: Magna Cum Laude"
"""

def create_new_yaml_resume(filename, inherit=None):
    if not filename.endswith('.yaml') and not filename.endswith('.yml'):
        filename += '.yaml'
    
    if os.path.exists(filename):
        print(f"File {filename} already exists. Skipping creation.")
        return

    data = yaml.safe_load(YAML_BOILERPLATE)
    if inherit:
        data['resume']['inherit'] = inherit[0] if len(inherit) == 1 else inherit

    # Using a custom dumper to preserve comments is complex with pyyaml, 
    # for simplicity we write the boilerplate string directly if no inheritance,
    # otherwise we dump and lose comments but gain inheritance.
    if not inherit:
        with open(filename, 'w') as f:
            f.write(YAML_BOILERPLATE.strip())
    else:
        with open(filename, 'w') as f:
            yaml.dump(data, f, sort_keys=False)
    
    print(f"Created new YAML resume: {filename}")

def create_new_template(name, output_dir=None):
    if output_dir:
        templates_dir = output_dir
    else:
        templates_dir = get_configuration('templates_dir')
    
    new_template_path = os.path.join(templates_dir, name)
    
    if os.path.exists(new_template_path):
        print(f"Template {name} already exists at {new_template_path}. Skipping creation.")
        return

    # Create directory structure
    os.makedirs(os.path.join(new_template_path, 'layout'), exist_ok=True)
    os.makedirs(os.path.join(new_template_path, 'css'), exist_ok=True)

    # Create a basic CSS file
    with open(os.path.join(new_template_path, 'css', 'style.css'), 'w') as f:
        f.write("/* Main Stylesheet */\n/* Use this file to define the visual look of your resume */\nbody { font-family: 'Helvetica', 'Arial', sans-serif; line-height: 1.6; color: #333; }")

    # Create basic layout files with Jinja2 comments
    layout_content = """<!-- Main Layout Template -->
<!-- This file defines the overall structure of your resume. -->
<!-- blocks: a list of block objects from the YAML content -->
<html>
  <head>
    <link rel="stylesheet" href="css/style.css">
  </head>
  <body>
    <!-- Iterate through blocks and include their respective partials -->
    {% for block in blocks if block.block_type == 'header' %}
        {% include 'layout/header.html' %}
    {% endfor %}
    
    <div class="content">
      {% for block in blocks if block.block_type == 'summary' %}
          {% include 'layout/summary.html' %}
      {% endfor %}
      
      {% for block in blocks if block.block_type == 'skills' %}
          {% include 'layout/skills.html' %}
      {% endfor %}
      
      {% for block in blocks if block.block_type == 'experience' %}
          {% if loop.first %}
              <section class="experience">
                  <h1 class="section-title">Experience</h1>
          {% endif %}
          {% include 'layout/experience.html' %}
          {% if loop.last %}</section>{% endif %}
      {% endfor %}
      
      {% for block in blocks if block.block_type == 'education' %}
          {% if loop.first %}
              <section class="education">
                  <h1 class="section-title">Education</h1>
          {% endif %}
          {% include 'layout/education.html' %}
          {% if loop.last %}</section>{% endif %}
      {% endfor %}
    </div>
  </body>
</html>"""

    header_content = """<!-- Header Partial -->
<!-- block.name: full name -->
<!-- block.job_title: job title -->
<!-- block.other_info: dict of additional fields (location, email, etc) -->
<header>
    <h1>{{ block.name }}</h1>
    <h2>{{ block.job_title }}</h2>
    <div class="contact-info">
        {% for label, value in block.other_info.items() %}
            <span>{{ label }}: {{ value }}</span>
        {% endfor %}
    </div>
</header>"""

    summary_content = """<!-- Summary Partial -->
<!-- block.summary: the summary text -->
<section class="summary">
    <h2>Professional Summary</h2>
    <p>{{ block.summary }}</p>
</section>"""

    skills_content = """<!-- Skills Partial -->
<!-- block.skills: list of skill strings -->
<section class="skills">
    <h2>Skills</h2>
    <ul>
        {% for skill in block.skills %}
        <li>{{ skill }}</li>
        {% endfor %}
    </ul>
</section>"""

    experience_content = """<!-- Experience Item Partial -->
<!-- This template is rendered for EACH experience entry -->
<div class="experience-item">
    <div class="header">
        <span class="role">{{ block.job_title }}</span>
        <span class="company">{{ block.company }}</span>
    </div>
    <div class="meta">
        <span class="duration">{{ block.date_range }}</span>
        <span class="location">{{ block.location }}</span>
    </div>
    <!-- description can be a string or a list -->
    {% if block.description is string %}
        <p>{{ block.description }}</p>
    {% else %}
        <ul>
            {% for point in block.description %}
                <li>{{ point }}</li>
            {% endfor %}
        </ul>
    {% endif %}
</div>"""

    education_content = """<!-- Education Item Partial -->
<div class="education-item">
    <h3>{{ block.degree }}</h3>
    <p>{{ block.institution }} | {{ block.date }}</p>
    {% if block.field_of_study %}<p>Field of Study: {{ block.field_of_study }}</p>{% endif %}
</div>"""

    projects_content = """<!-- Projects Item Partial -->
<div class="project-item">
    <h3>{{ block.title }}</h3>
    <p class="date">{{ block.date }}</p>
    <p>{{ block.description }}</p>
</div>"""

    files_to_create = {
        'layout/layout.html': layout_content,
        'layout/header.html': header_content,
        'layout/summary.html': summary_content,
        'layout/skills.html': skills_content,
        'layout/experience.html': experience_content,
        'layout/education.html': education_content,
        'layout/projects.html': projects_content,
    }

    for rel_path, content in files_to_create.items():
        with open(os.path.join(new_template_path, rel_path), 'w') as f:
            f.write(content)

    print(f"Created new template '{name}' at {new_template_path}")
