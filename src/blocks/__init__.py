class Block:
    def __init__(self, block_type):
        self.block_type = block_type


class HeaderBlock(Block):
    def __init__(
        self, 
        name=None, 
        job_title=None,
        profile_picture = None,
        extras = None,
        **kwargs
    ):
        super().__init__('header')
        self.name = name
        self.job_title = job_title
        self.profile_picture = profile_picture
        self.extras = extras or []
        self.other_info = kwargs


class SummaryBlock(Block):
    def __init__(self, summary=None, content=None):
        super().__init__('summary')
        self.summary = summary or content


class SkillsBlock(Block):
    def __init__(self, skills=None, content=None):
        super().__init__('skills')
        self.skills = skills or content


class EducationBlock(Block):
    def __init__(self, degree=None, date=None, field_of_study=None, institution=None, description=None, name=None, duration=None, study=None):
        super().__init__('education')
        self.degree = degree or name
        self.field_of_study = field_of_study or study
        self.institution = institution
        self.date = date or duration
        self.description = description


class ExperienceBlock(Block):
    def __init__(self, company=None, description=None, job_title=None, role=None, location=None, date_range=None, duration=None, name=None):
        super().__init__('experience')
        self.job_title = job_title or role
        self.company = company or name
        self.location = location
        self.date_range = date_range or duration
        self.description = description


class ProjectsBlock(Block):
    def __init__(self, title=None, description=None, date=None, name=None, duration=None):
        super().__init__('projects')
        self.title = title or name
        self.description = description
        self.date = date or duration
