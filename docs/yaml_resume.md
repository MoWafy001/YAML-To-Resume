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
| `inherit_strategy` | string | Strategy for merging inherited data (`deep`, `shallow`, `override`) | No |
| `content` | list | List of content blocks | Yes |

---

## Inheritance Strategies

When using the `inherit` field, you can specify how the data should be merged using `inherit_strategy`.

| Strategy | Description |
| :--- | :--- |
| `extend` (Default) | Deep recursive merge. Merges dictionaries, appends items to lists, and overrides scalars (strings, etc.). For the `content` block, it matches by type and merges block contents. |
| `overwrite` | Deep recursive merge for dictionaries, but replacement for lists and scalars. For the `content` block, it matches by type and replaces the entire block value. |

### Keyed List Merging (Content Block)
Both strategies use "Keyed List Merging" for the `content` field. This matches blocks by their type (e.g., `header`, `summary`, `experience`).

- **In `extend` mode**: If a block type matches, its contents are merged recursively. For example, if both files have a `skills` block, the lists of skills will be combined.
- **In `overwrite` mode**: If a block type matches, the new block completely replaces the old one. For example, if both files have a `header` block, only the information from the latest file will be kept.

In both modes, any block types present in only one file are preserved in the final output.

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
| Key | Description | Alternatives | Always Present |
| :--- | :--- | :--- | :--- |
| `company` | Organization name | `name` | Yes |
| `job_title` | Your job title | `role` | Yes |
| `date_range` | Time period string | `duration` | Yes |
| `location` | City/State or Remote | - | No |
| `description` | String or List of bullets | - | Yes |

```yaml
- experience:
    - company: "Tech Corp"
      job_title: "Senior Dev"
      date_range: "2020 - Present"
      description:
        - Led a team of 5
        - Reduced latency by 20%
```

### 5. `education`
A list of objects representing academic background.
| Key | Description | Alternatives | Always Present |
| :--- | :--- | :--- | :--- |
| `institution` | School/University name | - | Yes |
| `degree` | Degree obtained | `name` | Yes |
| `field_of_study` | Field of study | `study` | No |
| `date` | Graduation date or range | `duration` | No |
| `description` | Extra details | - | No |

```yaml
- education:
    - institution: "University of Tech"
      degree: "B.S. Computer Science"
      field_of_study: "Software Engineering"
      date: "2019"
```

### 6. `projects`
A list of objects representing personal or work projects.
| Key | Description | Alternatives | Always Present |
| :--- | :--- | :--- | :--- |
| `title` | Project title | `name` | Yes |
| `date` | Date or time range | `duration` | No |
| `description` | Project details | - | Yes |

```yaml
- projects:
    - title: "Resume Tool"
      date: "2024"
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
          job_title: "Software Engineer"
          date_range: "2021 - Present"
          description: "Implemented high-performance APIs."
    - education:
        - institution: "Tech Institute"
          degree: "B.S. Software Engineering"
          date: "2020"
```
