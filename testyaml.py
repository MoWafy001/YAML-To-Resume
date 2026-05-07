import yaml
from pprint import pprint

with open("examples/resume.yaml", "r") as file:
    resume_data = yaml.safe_load(file)

v = resume_data.get('resume').get('content')
print(v, type(v))
