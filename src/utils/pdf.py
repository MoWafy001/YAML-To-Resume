from weasyprint import HTML, CSS
import os
import pathlib
import re
from jinja2 import Environment, FileSystemLoader
from markupsafe import Markup
from utils.configuration import get_configuration
from utils.yaml_resume import YAMLResume

def __create_pdf(htmlstr, file_path, template_dir):
    css_dir = os.path.join(template_dir, 'css')

    default_css = """
    @page {
        size: A4 auto;
        margin: 0;
    }
    """

    css_files = [CSS(string=default_css)]
    if os.path.exists(css_dir):
        css_files.extend([CSS(filename=os.path.join(css_dir, css_file)) for css_file in os.listdir(css_dir) if css_file.endswith('.css')])

    output_dir = os.path.dirname(os.path.abspath(file_path))
    if not os.path.exists(output_dir):
        os.makedirs(output_dir, exist_ok=True)

    HTML(string=htmlstr).write_pdf(file_path, stylesheets=css_files)
    print(f"Created successfully: {file_path}")


def format_text(text):
    """
    Jinja2 filter to:
    1. Convert URLs to clickable links.
    2. Convert newlines to <br> tags.
    """
    if not isinstance(text, str):
        return text
    
    # Escape existing HTML to prevent XSS, then convert to Markup
    text = Markup.escape(text)
    
    # Linkify URLs
    url_pattern = re.compile(r'(https?://[^\s]+)')
    text = url_pattern.sub(r'<a href="\1">\1</a>', text)
    
    # Preserve line breaks
    text = text.replace('\n', '<br>')
    
    return Markup(text)


def create_resume(file_path, template_arg, output_arg = None, verbose = False):
    if verbose:
        print(f"--- Starting build for: {file_path} ---")
    
    yaml_resume = YAMLResume(file_path, verbose=verbose)
    
    # Priority: 1. CLI Argument, 2. YAML file, 3. Config default
    template = template_arg if template_arg else yaml_resume.template
    if not template:
        template = get_configuration('default_template')
    
    if verbose:
        print(f"Using template: {template}")
    
    template_p = pathlib.Path(template)

    if template_p.is_dir():
        template_dir = template_p
        layout_path = template_dir / 'layout' / 'layout.html'
    elif template.endswith('layout.html'):
        template_dir = template_p.parent.parent
        layout_path = pathlib.Path(template)
    else:
        template_dir = pathlib.Path(get_configuration('templates_dir')) / template
        layout_path = template_dir / 'layout' / 'layout.html'

    if verbose:
        print(f"Resolved template directory: {template_dir}")
        print(f"Resolved layout path: {layout_path}")

    if not layout_path.exists():
        raise FileNotFoundError(f"Layout file not found at {layout_path}")

    file_loader = FileSystemLoader(str(template_dir.absolute()))
    env = Environment(loader=file_loader, autoescape=True)
    env.filters['format_text'] = format_text
    template_obj = env.get_template('layout/layout.html')
    
    render_vars = {
        'blocks': yaml_resume.content,
        'name': yaml_resume.name,
        'job_title': yaml_resume.job_title,
    }
    resume_data = yaml_resume.get('resume')
    if isinstance(resume_data, dict):
        for k, v in resume_data.items():
            if k not in render_vars and k != 'content':
                render_vars[k] = v

    if verbose:
        print(f"Rendering with variables: {list(render_vars.keys())}")

    html = template_obj.render(**render_vars)

    # Determine final output path
    default_filename = yaml_resume.output if yaml_resume.output else f"{yaml_resume.name}_{yaml_resume.job_title}"
    if not default_filename.lower().endswith('.pdf'):
        default_filename += '.pdf'
    
    # sanitize default filename (replace spaces with underscores)
    default_filename = default_filename.replace(' ', '_')

    if not output_arg:
        final_output_path = default_filename
    elif os.path.isdir(output_arg) or output_arg.endswith(('/', '\\')):
        final_output_path = os.path.join(output_arg, default_filename)
    else:
        final_output_path = output_arg
        if not final_output_path.lower().endswith('.pdf'):
            final_output_path += '.pdf'

    if verbose:
        print(f"Final output path: {final_output_path}")

    __create_pdf(html, final_output_path, str(template_dir.absolute()))

def create_resume_or_resumes(file_or_dir_path, template, output_name = None, verbose = False):
    if os.path.isdir(file_or_dir_path):
        yaml_files = [os.path.join(file_or_dir_path, f) for f in os.listdir(file_or_dir_path) if f.endswith('.yaml') or f.endswith('.yml')]
        if verbose:
            print(f"Found {len(yaml_files)} YAML files in directory: {file_or_dir_path}")
        for f in yaml_files:
            create_resume(f, template, output_name, verbose)
    else:
        create_resume(file_or_dir_path, template, output_name, verbose)
