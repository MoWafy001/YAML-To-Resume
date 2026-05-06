![image](https://user-images.githubusercontent.com/47895671/232782487-3b04eaaf-c40b-442e-8085-d92e4ceb4242.png)

# Resume Creator

> [!WARNING]
> This project is currently a **Work in Progress**. The CLI interface and features are subject to change.

This python script creates PDF resumes using variables from a YAML file. 

# Installation

For now, this package is not published yet. 

### Method 1: Install as a CLI tool (Recommended)
To use the `yaml-to-resume` command globally in your environment:
```bash
pip install -e .
```

### Method 2: Manual Setup (Running as a script)
If you prefer not to install the package, you can set up a virtual environment and run the script directly:

1. **Create and activate a virtual environment:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Linux/macOS
   # OR
   .\venv\Scripts\activate   # On Windows
   ```

2. **Install requirements:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the tool:**
   ```bash
   python3 src/main.py build resume.yaml
   ```

# Usage

## Using the CLI

Once installed via Method 1, you can use the `yaml-to-resume` command:

```bash
# Basic usage with a yaml file
yaml-to-resume build resume.yaml

# Specify a template
yaml-to-resume build resume.yaml --template Default

# Specify an output path or directory
yaml-to-resume build resume.yaml -o my_resume.pdf
yaml-to-resume build resume.yaml -o exports/

# Use a custom configuration file
yaml-to-resume build resume.yaml --configs custom_config.yaml
```

## Configuration

1. Add the data you want to display in the resume to `vars.yaml` or any YAML file you want to use. Some fields are requried and some aren't, depending on the template.

Look in the `examples` directory for examples.

```yaml
template: Default

# color in hex: rrggbb
primary color: 008080


full name: Mohamed Wafy


job title: Frontend Developer


summary: |
  Frontend Developer, Backend Developer, and Computer Science student with experince with frontend and backend technologies, cloud, linux and teamwork.

links:
  - Portfolio: https://mowafy001.github.io/portfolio/
  - GitHub: https://github.com/MoWafy001
  - LinkedIn: https://linkedin.com/in/mohamedwafy
  - wafy123445@gmail.com: mailto:wafy123445@gmail.com
  - "+201127813978": tel:+201127813978


not_links:
  - Egypt
  - Egypt | Alex
  - Egypt | Cairo


skills:
  - React
  - SASS
  - Bootstrap
  - NodeJS
  - GitHub
  - Linux
  - Cloud
  - Googling
  - CSS
  - JavaScript
  - Python
  - PHP


experience:
  - Intern Backend Developer, Airdonex:
    - Sep 2021 - Dec 2021
    - |
      - Created RESTful APIs
      - Created a login system
      - Managed a PostgreSQL Database

      Highlighted skills: Django - PostgreSQL

  - Fullstack Developer, freelance:
    - Mar 2021 - May 2021
    - |
      - Created a Speech-To-Text API
      - Another API to convert file formats
      - Created a Systemd service to automate
      - processes on a Linux server
      - Created a flask app to render DZI images

      Highlighted skills: Linux - Flask - Python - API Development

  - Member of The Google Developer Student Club - GDSC Damanhour University:
    - Aug 2021 - Jun 2022
    - |
      - Teaching fellow students coding, Node JS in particular.
      - Creating a course and find materials.
      - Giving online session, and doing projects.

      Highlighted skills: Team Work - NodeJS



education:
  - React Developement Cross-Skilling Nanodegree, Udacity:
    - "2022"
    - |
      Highlighted skills:
      ReactJS
      Redux

  - Advanced Web Development Nano Degree, Udacity:
    - "2021"
    - |
      Highlighted skills:
      Flask
      API Development
      Backend Developement
      Model View Controller Model

  - Web Development Professional Nano Degree, Udacity:
    - "2020"
    - |
      Highlighted skills:
      NodeJS
      Building responsive pages
      Integrating APIs

  - Intermediate Python, DataCamp:
    - "2022"
    - |
      Highlighted skills:
      Python
```

# Output
The name of the output file is the `full name` of the user followed by an `_` followed by the `job title`.
```
Full_Name_Job_Title.pdf
```
