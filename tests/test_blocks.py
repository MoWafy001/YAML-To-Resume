import unittest
from blocks import (
    Block, HeaderBlock, SummaryBlock, SkillsBlock,
    EducationBlock, ExperienceBlock, ProjectsBlock
)

class TestBlocks(unittest.TestCase):

    def test_base_block(self):
        block = Block('custom')
        self.assertEqual(block.block_type, 'custom')

    def test_header_block(self):
        header = HeaderBlock(
            name="John Doe",
            job_title="Software Engineer",
            email="john@example.com",
            phone="+1234567890",
            extras=["Extra Note"]
        )
        self.assertEqual(header.block_type, 'header')
        self.assertEqual(header.name, "John Doe")
        self.assertEqual(header.job_title, "Software Engineer")
        self.assertEqual(header.extras, ["Extra Note"])
        self.assertEqual(header.other_info.get('email'), "john@example.com")
        self.assertEqual(header.other_info.get('phone'), "+1234567890")

    def test_summary_block(self):
        s1 = SummaryBlock(summary="Experienced engineer.")
        self.assertEqual(s1.block_type, 'summary')
        self.assertEqual(s1.summary, "Experienced engineer.")

        # Test content fallback
        s2 = SummaryBlock(content="Alternative summary.")
        self.assertEqual(s2.summary, "Alternative summary.")

    def test_skills_block(self):
        sk1 = SkillsBlock(skills=["Python", "Go"])
        self.assertEqual(sk1.block_type, 'skills')
        self.assertEqual(sk1.skills, ["Python", "Go"])

        # Test content fallback
        sk2 = SkillsBlock(content=["TypeScript"])
        self.assertEqual(sk2.skills, ["TypeScript"])

    def test_education_block(self):
        edu = EducationBlock(
            institution="University of Cairo",
            degree="B.Sc.",
            field_of_study="Computer Science",
            date="2020 - 2024",
            description="Graduated with honors"
        )
        self.assertEqual(edu.block_type, 'education')
        self.assertEqual(edu.institution, "University of Cairo")
        self.assertEqual(edu.degree, "B.Sc.")
        self.assertEqual(edu.field_of_study, "Computer Science")
        self.assertEqual(edu.date, "2020 - 2024")
        self.assertEqual(edu.description, "Graduated with honors")

        # Test alternatives (name, study, duration)
        edu_alt = EducationBlock(
            name="M.Sc.",
            study="Data Science",
            duration="2024 - 2026"
        )
        self.assertEqual(edu_alt.degree, "M.Sc.")
        self.assertEqual(edu_alt.field_of_study, "Data Science")
        self.assertEqual(edu_alt.date, "2024 - 2026")

    def test_experience_block(self):
        exp = ExperienceBlock(
            company="Tech Corp",
            job_title="Backend Developer",
            location="Remote",
            date_range="Jan 2022 - Present",
            description=["Built microservices", "Optimized queries"]
        )
        self.assertEqual(exp.block_type, 'experience')
        self.assertEqual(exp.company, "Tech Corp")
        self.assertEqual(exp.job_title, "Backend Developer")
        self.assertEqual(exp.location, "Remote")
        self.assertEqual(exp.date_range, "Jan 2022 - Present")
        self.assertEqual(len(exp.description), 2)

        # Test alternatives (role, duration, name)
        exp_alt = ExperienceBlock(
            name="Startup Inc",
            role="Lead Architect",
            duration="2020 - 2022"
        )
        self.assertEqual(exp_alt.company, "Startup Inc")
        self.assertEqual(exp_alt.job_title, "Lead Architect")
        self.assertEqual(exp_alt.date_range, "2020 - 2022")

    def test_projects_block(self):
        proj = ProjectsBlock(
            title="Open Source CLI",
            description=["Created a Python CLI", "100+ GitHub stars"],
            date="2024"
        )
        self.assertEqual(proj.block_type, 'projects')
        self.assertEqual(proj.title, "Open Source CLI")
        self.assertEqual(proj.date, "2024")
        self.assertEqual(len(proj.description), 2)

        # Test alternative name and duration
        proj_alt = ProjectsBlock(name="Web App", duration="2023")
        self.assertEqual(proj_alt.title, "Web App")
        self.assertEqual(proj_alt.date, "2023")

if __name__ == '__main__':
    unittest.main()
