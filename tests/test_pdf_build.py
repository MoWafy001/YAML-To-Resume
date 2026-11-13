import unittest
import tempfile
import os
import yaml
import pathlib
from utils.pdf import create_resume

class TestPDFBuild(unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_end_to_end_resume_pdf_generation(self):
        # Create a sample YAML resume
        resume_data = {
            'resume': {
                'name': 'End-to-End Tester',
                'job_title': 'Automation Engineer',
                'template': 'LaTeX',
                'content': [
                    {'header': {
                        'email': 'tester@example.com',
                        'location': 'Earth'
                    }},
                    {'summary': 'Thorough end-to-end automated test runner.'},
                    {'skills': [
                        'Languages: Python, Bash',
                        'Testing: Unittest, Pytest'
                    ]},
                    {'experience': [{
                        'company': 'Quality Assurance Labs',
                        'job_title': 'Lead QA',
                        'location': 'Remote',
                        'date_range': '2022 - Present',
                        'description': [
                            'Automated integration pipelines.',
                            'Maintained high test coverage across microservices.'
                        ]
                    }]},
                    {'education': [{
                        'institution': 'Tech Institute',
                        'degree': 'B.S.',
                        'field_of_study': 'Software Engineering',
                        'date': '2018 - 2022'
                    }]},
                    {'projects': [{
                        'title': 'Test Automation Framework',
                        'date': '2023',
                        'description': ['Built scalable testing harness.']
                    }]}
                ]
            }
        }
        yaml_path = os.path.join(self.temp_dir.name, 'resume.yaml')
        with open(yaml_path, 'w') as f:
            yaml.dump(resume_data, f)

        pdf_output = os.path.join(self.temp_dir.name, 'output.pdf')
        latex_template_dir = str(pathlib.Path(__file__).parent.parent / "src" / "assets" / "templates" / "LaTeX")

        create_resume(
            file_path=yaml_path,
            template_arg=latex_template_dir,
            output_arg=pdf_output,
            verbose=False
        )

        self.assertTrue(os.path.exists(pdf_output), "PDF output file was not created.")
        self.assertGreater(os.path.getsize(pdf_output), 1000, "PDF file is suspiciously small or empty.")

if __name__ == '__main__':
    unittest.main()
