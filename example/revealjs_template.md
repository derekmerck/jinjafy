{% macro render_slide(item, level=1, bread_crumbs='') -%}

{{ '#'*level }} {{ bread_crumbs }}{{ item.title }}{{ ' - ' if item.get('title_modifier') }}{{ item.title_modifier }}

{% if item.get('image') -%}

::: columns
:::: {.column width={{ '60%' if not item.get("wide_image") else '40%'}} }
{{ item.content }}
::::
:::: {.column width={{ '40%' if not item.get("wide_image") else '60%'}}}

::::: {.fig}
![{{ item.im_caption }}](images/{{ item.image }})
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

{%- else -%}

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

{% if background.get("file") | default(None) %}
parallaxBackgroundImage: images/{{ background.file }}
parallaxBackgroundSize: {{ background.im_size[0] }}px {{ background.im_size[1] }}px
parallaxBackgroundHorizontal: {{ background.im_size[0] / (content | length) }}
parallaxBackgroundVertical:  {{ background.im_size[1] / 10 }}
{% endif %}
---

<style>
div.column {
  font-size: smaller;
  vertical-align: middle;
}
div.fig {
  width: 100%;
  height: 80%;
  font-size: smaller;
}
.reveal figure {
  height: 100%;
  width: 100%;
}
.reveal figure img {
  max-height: 80%;
  width: auto;
}

</style>

{{ render_slide(intro, level=3) }}

{{ render_slide(agenda, level=3) }}

{% for item in content -%}
{{ render_slide(item, level=2) }}
{% endfor %}

##
{{ render_slide(follow_up, level=3) }}
