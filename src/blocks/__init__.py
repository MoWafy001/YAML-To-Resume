class Block:
    def __init__(self, block_type):
        self.block_type = block_type


class HeaderBlock(Block):
    def __init__(
        self, 
        name, 
        job_title,
        profile_picture = None,
        **kwargs
    ):
        super().__init__('header')
        self.name = name
        self.job_title = job_title
        self.profile_picture = profile_picture
        self.other_info = kwargs


class SummaryBlock(Block):
    def __init__(self, summary):
        super().__init__('summary')
        self.summary = summary


class SkillsBlock(Block):
    def __init__(self, skills):
        super().__init__('skills')
        self.skills = skills


class EducationBlock(Block):
    def __init__(self, degree=None, date=None, field_of_study=None, institution=None, description=None, name=None):
        super().__init__('education')
        self.degree = degree or name
        self.field_of_study = field_of_study
        self.institution = institution
        self.date = date
        self.description = description


class ExperienceBlock(Block):
    def __init__(self, company, description, job_title=None, role=None, location=None, date_range=None, duration=None):
        super().__init__('experience')
        self.job_title = job_title or role
        self.company = company
        self.location = location
        self.date_range = date_range or duration
        self.description = description


class ProjectsBlock(Block):
    def __init__(self, title, description, date=None):
        super().__init__('projects')
        self.title = title
        self.description = description
        self.date = date
