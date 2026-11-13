import unittest
import tempfile
import os
import yaml
from utils.new import create_new_yaml_resume, create_new_template

class TestNewCommands(unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_create_new_yaml_resume(self):
        output_file = os.path.join(self.temp_dir.name, 'my_resume.yaml')
        create_new_yaml_resume(output_file)

        self.assertTrue(os.path.exists(output_file))
        with open(output_file, 'r') as f:
            data = yaml.safe_load(f)
        self.assertIn('resume', data)
        self.assertEqual(data['resume']['name'], "Your Name")
        self.assertEqual(data['resume']['job_title'], "Your Job Title")

    def test_create_new_yaml_resume_with_inherit(self):
        output_file = os.path.join(self.temp_dir.name, 'child_resume.yaml')
        create_new_yaml_resume(output_file, inherit=['parent.yaml'])

        self.assertTrue(os.path.exists(output_file))
        with open(output_file, 'r') as f:
            data = yaml.safe_load(f)
        self.assertEqual(data['resume']['inherit'], 'parent.yaml')

    def test_create_new_template_based_on_latex(self):
        template_name = "MyCustomTemplate"
        create_new_template(template_name, output_dir=self.temp_dir.name)

        target_dir = os.path.join(self.temp_dir.name, template_name)
        self.assertTrue(os.path.isdir(target_dir))
        
        # Verify structure
        self.assertTrue(os.path.exists(os.path.join(target_dir, "layout", "layout.html")))
        self.assertTrue(os.path.exists(os.path.join(target_dir, "layout", "header.html")))
        self.assertTrue(os.path.exists(os.path.join(target_dir, "layout", "education.html")))
        self.assertTrue(os.path.exists(os.path.join(target_dir, "layout", "projects.html")))
        self.assertTrue(os.path.exists(os.path.join(target_dir, "css", "style.css")))
        self.assertTrue(os.path.exists(os.path.join(target_dir, "README.md")))

        # Verify it has LaTeX typography elements
        with open(os.path.join(target_dir, "css", "style.css"), 'r') as f:
            css_content = f.read()
        self.assertIn("Computer Modern", css_content)

if __name__ == '__main__':
    unittest.main()
