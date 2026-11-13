import unittest
import tempfile
import os
import yaml
from utils.yaml_resume import YAMLResume
from blocks import HeaderBlock, SummaryBlock, SkillsBlock, ExperienceBlock, EducationBlock, ProjectsBlock

class TestYAMLResume(unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()

    def tearDown(self):
        self.temp_dir.cleanup()

    def _write_yaml(self, filename, data):
        path = os.path.join(self.temp_dir.name, filename)
        with open(path, 'w') as f:
            yaml.dump(data, f)
        return path

    def test_basic_resume_load(self):
        resume_data = {
            'resume': {
                'name': 'Alice Smith',
                'job_title': 'DevOps Engineer',
                'output': 'alice.pdf',
                'content': [
                    {'summary': 'Cloud specialist.'},
                    {'skills': ['AWS', 'Docker', 'Kubernetes']}
                ]
            }
        }
        path = self._write_yaml('basic.yaml', resume_data)
        r = YAMLResume(path)

        self.assertEqual(r.name, 'Alice Smith')
        self.assertEqual(r.job_title, 'DevOps Engineer')
        self.assertEqual(r.output, 'alice.pdf')
        self.assertEqual(len(r.content), 2)
        self.assertIsInstance(r.content[0], SummaryBlock)
        self.assertEqual(r.content[0].summary, 'Cloud specialist.')
        self.assertIsInstance(r.content[1], SkillsBlock)
        self.assertEqual(r.content[1].skills, ['AWS', 'Docker', 'Kubernetes'])

    def test_overwrite_strategy(self):
        # Base resume
        base_data = {
            'resume': {
                'name': 'Bob Base',
                'job_title': 'Base Engineer',
                'content': [
                    {'summary': 'Base summary'},
                    {'skills': ['Python', 'Django']},
                    {'education': [
                        {'institution': 'Base University', 'degree': 'B.Sc.'}
                    ]}
                ]
            }
        }
        self._write_yaml('base.yaml', base_data)

        # Child resume overriding skills and summary using overwrite strategy
        child_data = {
            'resume': {
                'inherit': 'base.yaml',
                'inherit_strategy': 'overwrite',
                'job_title': 'Senior Engineer',
                'content': [
                    {'summary': 'Overwritten summary'},
                    {'skills': ['Go', 'Kubernetes']}
                ]
            }
        }
        child_path = self._write_yaml('child.yaml', child_data)
        r = YAMLResume(child_path)

        self.assertEqual(r.name, 'Bob Base')  # inherited
        self.assertEqual(r.job_title, 'Senior Engineer')  # overridden
        
        # Verify content blocks
        block_types = [b.block_type for b in r.content]
        self.assertIn('summary', block_types)
        self.assertIn('skills', block_types)
        self.assertIn('education', block_types)

        summary_block = next(b for b in r.content if b.block_type == 'summary')
        self.assertEqual(summary_block.summary, 'Overwritten summary')

        skills_block = next(b for b in r.content if b.block_type == 'skills')
        self.assertEqual(skills_block.skills, ['Go', 'Kubernetes'])

        edu_block = next(b for b in r.content if b.block_type == 'education')
        self.assertEqual(edu_block.institution, 'Base University')

    def test_extend_strategy(self):
        base_data = {
            'resume': {
                'name': 'Charlie Base',
                'content': [
                    {'skills': ['Python']}
                ]
            }
        }
        self._write_yaml('base_ext.yaml', base_data)

        child_data = {
            'resume': {
                'inherit': 'base_ext.yaml',
                'inherit_strategy': 'extend',
                'content': [
                    {'skills': ['Rust']}
                ]
            }
        }
        child_path = self._write_yaml('child_ext.yaml', child_data)
        r = YAMLResume(child_path)

        skills_block = next(b for b in r.content if b.block_type == 'skills')
        self.assertEqual(skills_block.skills, ['Python', 'Rust'])

    def test_multi_parent_inheritance(self):
        # Component 1: Header
        comp1 = {
            'resume': {
                'name': 'Multi Parent Tester',
                'content': [
                    {'header': {'email': 'test@example.com'}}
                ]
            }
        }
        self._write_yaml('header.yaml', comp1)

        # Component 2: Education
        comp2 = {
            'resume': {
                'content': [
                    {'education': [{'institution': 'MIT', 'degree': 'M.S.'}]}
                ]
            }
        }
        self._write_yaml('education.yaml', comp2)

        # Child inherits both
        child_data = {
            'resume': {
                'inherit': ['header.yaml', 'education.yaml'],
                'job_title': 'Researcher',
                'content': [
                    {'summary': 'Research summary'}
                ]
            }
        }
        child_path = self._write_yaml('multi_child.yaml', child_data)
        r = YAMLResume(child_path)

        self.assertEqual(r.name, 'Multi Parent Tester')
        self.assertEqual(r.job_title, 'Researcher')
        block_types = [b.block_type for b in r.content]
        self.assertEqual(block_types, ['header', 'education', 'summary'])

    def test_invalid_resume_raises_value_error(self):
        # No 'resume' key
        path = self._write_yaml('invalid.yaml', {'foo': 'bar'})
        with self.assertRaises(ValueError):
            YAMLResume(path)

    def test_invalid_strategy_raises_value_error(self):
        data = {
            'resume': {
                'inherit_strategy': 'non_existent_strategy',
                'content': []
            }
        }
        path = self._write_yaml('bad_strategy.yaml', data)
        with self.assertRaises(ValueError):
            YAMLResume(path)

    def test_unknown_block_type_raises_value_error(self):
        data = {
            'resume': {
                'name': 'Test',
                'content': [
                    {'unknown_block': 'some data'}
                ]
            }
        }
        path = self._write_yaml('bad_block.yaml', data)
        with self.assertRaises(ValueError):
            YAMLResume(path)

if __name__ == '__main__':
    unittest.main()
