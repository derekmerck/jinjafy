{# Basic project template with boilerplate #}
{% include "sections/front_matter.md" %}

{% if blocks['preamble'] is defined %}{{ blocks['preamble'] | render_block(level=2) }}{% endif %}
{% if blocks['summary'] is defined %}{{ blocks['summary'] | render_block(level=2) }}{% endif %}
{% if blocks['aims'] is defined %}{{ blocks['aims'] | render_block(level=2) }}{% endif %}

{{ blocks.background | render_block(level=2) }}

{# blocks.approach   | boilerplate('deidentified', 'data-collection', deidentified) | render_block(level=2) #}

{% if blocks['preliminary-results'] is defined %}{{ blocks['preliminary-results'] | render_block(level=3) }}{% endif %}

{{ blocks['expected-results']  | render_block(level=2) }}

{#{% if risk is defined -%}#}
{#Risk#}
{#----------------#}
{#{{ boilerplate(risk) }}{{ risk_addendum }}#}
{#{%- else %}#}
{#{{ blocks.risk | render_block(2) }}#}
{#{%- endif %}#}


{% include "sections/bibliography.md" %}