import unittest
import os
import pathlib
from jinja2 import Environment, FileSystemLoader
from utils.pdf import format_text
from blocks import HeaderBlock, SummaryBlock, SkillsBlock, ExperienceBlock, EducationBlock, ProjectsBlock

class TestTemplates(unittest.TestCase):

    def setUp(self):
        self.templates_dir = pathlib.Path(__file__).parent.parent / "src" / "assets" / "templates"

    def test_builtin_templates_exist(self):
        expected_templates = ["LaTeX", "Standard", "Unnamed"]
        for t in expected_templates:
            template_path = self.templates_dir / t
            self.assertTrue(template_path.exists(), f"Template '{t}' not found at {template_path}")
            layout_file = template_path / "layout" / "layout.html"
            self.assertTrue(layout_file.exists(), f"layout.html missing for template '{t}'")
            style_file = template_path / "css" / "style.css"
            self.assertTrue(style_file.exists(), f"style.css missing for template '{t}'")

    def test_latex_template_structure(self):
        latex_path = self.templates_dir / "LaTeX"
        expected_files = [
            "layout/layout.html",
            "layout/header.html",
            "layout/summary.html",
            "layout/skills.html",
            "layout/experience.html",
            "layout/education.html",
            "layout/projects.html",
            "css/style.css",
            "README.md"
        ]
        for rel_file in expected_files:
            file_path = latex_path / rel_file
            self.assertTrue(file_path.exists(), f"LaTeX template file missing: {rel_file}")

    def test_latex_template_rendering(self):
        latex_dir = self.templates_dir / "LaTeX"
        file_loader = FileSystemLoader(str(latex_dir.absolute()))
        env = Environment(loader=file_loader, autoescape=True)
        env.filters['format_text'] = format_text
        template = env.get_template('layout/layout.html')

        # Create sample blocks
        blocks = [
            HeaderBlock(
                name="Jane Doe",
                job_title="Lead Architect",
                email="jane@example.com",
                phone="+1-555-0199",
                location="San Francisco, CA"
            ),
            SummaryBlock(summary="Experienced architect building resilient systems."),
            SkillsBlock(skills=["Languages: Python, Go", "Cloud: GCP, AWS"]),
            ExperienceBlock(
                company="Acme Corp",
                job_title="Senior Engineer",
                location="Remote",
                date_range="2021 - Present",
                description=["Built scalable APIs", "Improved reliability to 99.99%"]
            ),
            EducationBlock(
                institution="Stanford University",
                degree="B.S.",
                field_of_study="Computer Science",
                date="2017 - 2021"
            ),
            ProjectsBlock(
                title="SuperCLI",
                date="2023",
                description=["Created a popular CLI utility"]
            )
        ]

        rendered_html = template.render(
            name="Jane Doe",
            job_title="Lead Architect",
            blocks=blocks
        )

        self.assertIn("Jane Doe", rendered_html)
        self.assertIn("Lead Architect", rendered_html)
        self.assertIn("jane@example.com", rendered_html)
        self.assertIn("Experienced architect", rendered_html)
        self.assertIn("Acme Corp", rendered_html)
        self.assertIn("Stanford University", rendered_html)
        self.assertIn("SuperCLI", rendered_html)
        self.assertIn("latex-content", rendered_html)

    def test_format_text_filter(self):
        # 1. URL linkification
        text_with_url = "Visit https://github.com/MoWafy001 for details."
        res = format_text(text_with_url)
        self.assertIn('<a href="https://github.com/MoWafy001">https://github.com/MoWafy001</a>', str(res))

        # 2. Newline conversion to <br>
        text_with_newlines = "Line 1\nLine 2\nLine 3"
        res_nl = format_text(text_with_newlines)
        self.assertIn('Line 1<br>Line 2<br>Line 3', str(res_nl))

        # 3. Non-string passthrough
        self.assertEqual(format_text(12345), 12345)

if __name__ == '__main__':
    unittest.main()
