{# Revealjs template with vertical sections #}

{% macro render_slide(item, level=1, bread_crumbs='') %}

{{ '#'*level }} {{ bread_crumbs }}{{ item.title }}{{ ' - ' if item.get('title_modifier') }}{{ item.title_modifier }}

{%- if item.get('image') %}

::: columns
:::: {.column width={{ '60%' if not item.get("wide_image") else '40%'}} }
{{ item.content }}
::::
:::: {.column width={{ '40%' if not item.get("wide_image") else '60%'}}}

::::: {.fig}
![{{ item.im_caption }}]({{ "images/" + item.image if not item.image.startswith("http") else item.image }})
:::::

::::
:::

{%- elif item.get('content2') %}

::: columns
:::: {.column width=50% }
{{ item.content }}
::::
:::: {.column width=50% }
{{ item.content2 }}
::::
:::

{%- else %}

{{ item.content }}

{%- endif %}

{% for subitem in item.children -%}
{{ render_slide(subitem, level=level+1, bread_crumbs=item.title+" - ") }}
{% endfor %}

{%- endmacro -%}

---
author: {{ author }}
title: {{ title }}
date: {{ date }}

{%- if theme and theme.background %}
{%- if theme.background.color %}
BackgroundColor: {{  theme.background.color }}
{% endif %}

{%- if theme.background.parallax %}
parallaxBackgroundImage: images/{{ theme.background.file }}
parallaxBackgroundSize: {{ theme.background.im_size[0] }}px {{ theme.background.im_size[1] }}px
parallaxBackgroundHorizontal: {{ (theme.background.im_size[0] / (children | length)) | int }}
parallaxBackgroundVertical:  {{ (theme.background.im_size[1] / 10) | int }}
{%- endif %}
{%- endif %}

suppress-bibliography: true
...

{% for item in children -%}
{{ render_slide(item, level=2) }}
{% endfor %}
