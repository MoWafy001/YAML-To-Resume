# YAML Resume Schema Reference

The resume file is written in YAML. The root object MUST be `resume`.

> [!TIP]
> You can find complete, functional examples for various scenarios in the [examples/](../examples/) directory.

## Top-Level Fields

| Key | Type | Description | Required |
| :--- | :--- | :--- | :--- |
| `name` | string | Full name of the person | Yes |
| `job_title` | string | Professional title | Yes |
| `template` | string | Name of the template to use (e.g., "Default") | No |
| `output` | string | Name of the output PDF file | No |
| `primary_color` | string | Hex color without # (e.g., "008080") | No |
| `inherit` | string \| list | Filename(s) to inherit data from | No |
| `content` | list | List of content blocks | Yes |

---

## Content Blocks (`resume.content`)

The `content` field is a list where each item is a dictionary with a single key identifying the block type.

### 1. `header`
A list containing key-value pairs (links/info) or single strings.
```yaml
- header:
    - email: "john@example.com"
    - LinkedIn: "https://linkedin.com/in/user"
    - "New York, NY"
    - "Willing to relocate"
```

### 2. `summary`
A simple string or a multi-line block.
```yaml
- summary: |
    Experienced developer with a focus on...
```

### 3. `skills`
A list of strings.
```yaml
- skills: ["Python", "Jinja2", "YAML"]
```

### 4. `experience`
A list of objects representing professional roles.
| Key | Description | Always Present |
| :--- | :--- | :--- |
| `company` | Organization name | Yes |
| `role` | Your job title | Yes |
| `duration` | Time period string | Yes |
| `location` | City/State or Remote | No |
| `description` | String or List of bullets | Yes |

```yaml
- experience:
    - company: "Tech Corp"
      role: "Senior Dev"
      duration: "2020 - Present"
      description:
        - Led a team of 5
        - Reduced latency by 20%
```

### 5. `education`
A list of objects representing academic background.
| Key | Description | Always Present |
| :--- | :--- | :--- |
| `institution` | School/University name | Yes |
| `degree` | Degree obtained | Yes |
| `study` | Field of study | No |
| `duration` | Graduation date or range | No |
| `description` | Extra details | No |

```yaml
- education:
    - institution: "University of Tech"
      degree: "B.S. Computer Science"
      study: "Software Engineering"
      duration: "2019"
```

### 6. `projects`
A list of objects representing personal or work projects.
| Key | Description | Always Present |
| :--- | :--- | :--- |
| `name` | Project title | Yes |
| `duration` | Date or time range | No |
| `description` | Project details | Yes |

```yaml
- projects:
    - name: "Resume Tool"
      duration: "2024"
      description: "A tool to build resumes from YAML."
```

---

## Full Example

```yaml
resume:
  name: "Jane Smith"
  job_title: "Backend Engineer"
  primary_color: "2c3e50"
  content:
    - header:
        - email: "jane@example.com"
        - "San Francisco, CA"
    - summary: "Specializing in Python and distributed systems."
    - skills: ["Python", "Go", "Kubernetes"]
    - experience:
        - company: "ScaleUp"
          role: "Software Engineer"
          duration: "2021 - Present"
          description: "Implemented high-performance APIs."
    - education:
        - institution: "Tech Institute"
          degree: "B.S. Software Engineering"
          duration: "2020"
```
