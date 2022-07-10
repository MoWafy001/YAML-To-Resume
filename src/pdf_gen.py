import pdfkit
import os

options = {
    'page-size': 'Letter',
    'margin-top': '0',
    'margin-right': '0',
    'margin-bottom': '0',
    'margin-left': '0',
    'encoding': "UTF-8",
    'custom-header': [
        ('Accept-Encoding', 'gzip')
    ],
    'no-outline': None
}

# load the css file names automaticlly from the css directory
dir_name = 'css'
css = list(map(lambda x: f"{dir_name}/{x}" , os.listdir(dir_name)))

def create_pdf(layout):
    pdfkit.from_string(layout, 'out.pdf', options=options, css=css)