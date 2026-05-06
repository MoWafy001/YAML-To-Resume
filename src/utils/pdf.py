from weasyprint import HTML, CSS
import os
import pathlib

from utils.configuration import get_configuration
from utils.html import TemplateEngine
from utils.yaml_resume import YAMLResume

def __create_pdf(htmlstr, file_name, template_dir):
    # Load CSS file paths automatically from the CSS directory
    css_dir = os.path.join(template_dir, 'css')

    # Default CSS with fallback margins
    default_css = """
    @page {
        size: A4 auto;
        margin: 0; /* Default margins */
    }
    """

    css_files = [
        CSS(string=default_css),
        *[CSS(filename=os.path.join(css_dir, css_file)) for css_file in os.listdir(css_dir) if css_file.endswith('.css')]
    ]


    # Generate the PDF
    if not file_name.endswith('.pdf'):
        file_name += '.pdf'

    output_dir = str(pathlib.Path(file_name).parent.absolute())
    if not os.path.exists(output_dir):
        os.mkdir(output_dir)

    HTML(string=htmlstr).write_pdf(file_name, stylesheets=css_files)

    print(f"{file_name} created successfully at {output_dir}")


def create_resume(file_path, template, output_name):
    yaml_resume = YAMLResume(file_path)
    template = template if template else yaml_resume.get('template')
    template = template if template else get_configuration('default_template')
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

    if not layout_path.exists():
        raise FileNotFoundError(f"Layout file not found at {layout_path}. Please ensure the template directory contains a 'layout/layout.html' file and that the template name is valid. Example: 'Default'")

    # render the template
    engine = TemplateEngine(
        str(layout_path.absolute()), yaml_resume.get)
    html, file_name = engine.render()

    # create the pdf
    __create_pdf(
        html, 
        output_name if output_name else file_name, 
        str(template_dir.absolute()))
