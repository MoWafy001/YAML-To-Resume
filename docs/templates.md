# Template Context Reference

## Global Variables
| Variable | Type | Description | Always Present |
| :--- | :--- | :--- | :--- |
| `name` | string | Full name from resume | Yes |
| `job_title` | string | Professional title | Yes |
| `primary_color` | string | Hex color (e.g., "008080") | No |
| `blocks` | list | List of all Block objects | Yes |
| `[key]` | any | Any other top-level key from the `resume` object (spaces -> `_`) | No |

## Block Reference (`block.block_type`)

> [!NOTE]
> While the YAML schema supports alternative field names (e.g., `role` for `job_title`), they are automatically mapped to the primary attributes listed below when passed to the template context.

### `header`
| Attribute | Type | Description | Always Present |
| :--- | :--- | :--- | :--- |
| `name` | string | Full name | Yes |
| `job_title` | string | Job title | Yes |
| `profile_picture` | string | Image path/URL | No |
| `extras` | list | List of unkeyed strings | Yes |
| `other_info` | dict | Dictionary of all key-value pairs | Yes |

### `summary`
| Attribute | Type | Description | Always Present |
| :--- | :--- | :--- | :--- |
| `summary` | string | The summary text | Yes |

### `skills`
| Attribute | Type | Description | Always Present |
| :--- | :--- | :--- | :--- |
| `skills` | list | List of skill strings | Yes |

### `experience`
| Attribute | Type | Description | Always Present |
| :--- | :--- | :--- | :--- |
| `job_title` | string | Role title | Yes |
| `company` | string | Company name | Yes |
| `location` | string | Location string | No |
| `date_range` | string | Duration string | Yes |
| `description` | string \| list | Bullet points or block text | Yes |

### `education`
| Attribute | Type | Description | Always Present |
| :--- | :--- | :--- | :--- |
| `degree` | string | Degree obtained | Yes |
| `institution` | string | School name | Yes |
| `field_of_study` | string | Major area | No |
| `date` | string | Graduation date | No |
| `description` | string \| list | Optional details | No |

### `projects`
| Attribute | Type | Description | Always Present |
| :--- | :--- | :--- | :--- |
| `title` | string | Project name | Yes |
| `date` | string | Completion date | No |
| `description` | string \| list | Project details | Yes |

## Custom Filters

### `format_text`
A custom filter is provided to automatically:
1.  **Linkify URLs**: Converts `https://...` into clickable `<a>` tags.
2.  **Preserve Line Breaks**: Converts `\n` into `<br>` tags.

**Usage:**
```html
<p>{{ block.description | format_text }}</p>
```

## Implementation Patterns

### Iterating Specific Blocks
```html
{% for block in blocks if block.block_type == 'experience' %}
  <div>{{ block.company }}</div>
{% endfor %}
```

### Handling String vs List (Description)
```html
{% if block.description is string %}
  <p>{{ block.description | format_text }}</p>
{% else %}
  <ul>
    {% for point in block.description %}
      <li>{{ point | format_text }}</li>
    {% endfor %}
  </ul>
{% endif %}
```

## CSS Styling
The following CSS variables are automatically injected:
- `var(--primary-color)`: The hex color from YAML.
- `var(--primary-color-light)`: Hex + "66" opacity.
- `var(--primary-color-very-light)`: Hex + "11" opacity.
