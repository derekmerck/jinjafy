{# CV template #}
---
title: {{ contact.name }}{%- if contact.credentials %}{{ contact.credentials }}{% endif %}
...

{######### MACROS ##########}
{% macro pubs_section(header, pubs) %}
{% if pubs %}
## {{ header | title  }}

{% for item in pubs | sortcsl(bibliography, reverse=True) %}
#. [@{{ item }}]
{% endfor %}
{% endif %}

{% endmacro %}

{%- macro rulify() %}
{%- for width in widths %}
{{- '-' * (width - 1) + ' ' -}}
{%- endfor %}
{% endmacro -%}

{%- macro rowify(things) %}
{%- for thing, width in zip(things, widths) %}
{{- '{:<{width}}'.format(thing, width=width) -}}
{%- endfor %}
{% endmacro -%}

{%- macro daterange(start, end) %}
{%- if start -%}
{{- '{}-{}'.format(start.year, end.year or 'present') -}}
{%- else -%}
{{- '{}'.format(end.year or end) -}}
{%- endif -%}
{% endmacro -%}

{######### CONTENT ##########}

email: {{contact.email.work}}

# Education
{% set widths=[14,59] %}
{{ rulify() -}}
{% for item in education -%}

{{ rowify( [daterange(item.startdate, item.enddate),
            '{deg:<5}{inst}, {place}'.format( 
            deg=item.degree, 
            inst=item.institution, 
            place=item.place ) ] ) }}
{%  endfor  %}
{{- rulify() }}

# Academic Appointments
{{ rulify() -}}
{% for item in (academic + affiliations) | bystart(true) -%}

{{ rowify(  [daterange(item.startdate, item.enddate), 
             "{pos}{com0}{dept}, {inst}, {place}".format(
                pos=item.position,
                com0=', ' if item.department else '',
                dept=item.department or '',
                inst=item.institution,
                place=item.place) ] ) }}
{%  endfor  %}
{{- rulify() }}

# Professional Positions
{{ rulify() -}}
{% for item in professional | bystart(true) -%}

{{ rowify(  [daterange(item.startdate, item.enddate),
             '{pos}{com0}{dept}, {comp}, {place}'.format(
                pos=item.position,
                com0=', ' if item.department else '',
                dept=item.department or '',
                comp=item.company,
                place=item.place ) ] ) }}
{%  endfor  %}
{{- rulify() }}

# Publications
{% if contact.get("orcid") %}
ORCID: [{{ contact.orcid }}](https://orcid.org/{{ contact.orcid }})
{% endif %}

{{ pubs_section("Manuscripts", publications.manuscripts) }}

{{ pubs_section("Conferences", publications.conferences) }}

{{ pubs_section("Seminars", publications.seminars) }}


# Awards
{{ rulify() -}}
{% for item in awards | bystart(true) -%}

{{- rowify( [daterange(item.startdate, item.enddate), 
   '{title}{com0}{source} {mechanism}{com1}{pi_}{pl} {pi}{com2}{amount}'.format(
                        title=item.title or '',
                        com0=', ' if item.title and item.source else '',
                        source=item.source,
                        mechanism=item.mechanism,
                        com1=', ' if item.pi else '',
                        pi_='PI' if item.pi,
                        pl='s' if item.pi and item.pi.find(',')>-1,
                        pi=item.pi or '',
                        com2=', ' if item.amount else '',
                        amount=item.amount or '') ] ) }}
{% endfor %}
{{- rulify() }}

{### IRB Approved Research Protocols#}
{#{{ rulify() -}}#}
{#{% for item in irb_studies -%}#}
{##}
{#{{- rowify( [item.effective_date[-4:] or "pending", #}
{#            '[RIH {id}] {title}, PI {pi}'.format(title=item.title,#}
{#                                            id=item.irbnet_id,#}
{#                                            pi=item.pi) ] ) }}#}
{#{% endfor %}#}
{#{{- rulify() }}#}

# Teaching

## Course Curricula
{{ rulify() -}}
{% for item in teaching -%}

{{ rowify( [daterange(item.startdate, item.enddate),
            item.name + ' (' + item.number + '), ' + item.institution ] ) }}
{% endfor %}
{{- rulify() }}

## Advisees
{{ rulify() -}}
{% for item in advisees | bystart(true) -%}

{{ rowify( [daterange(item.startdate, item.enddate),
            item.name + ', ' + item.institution + ' ' + item.role ] ) }}
{% endfor %}
{{- rulify() }}

{{ pubs_section("Hosted Talks", hosted_talks) }}

# Service
{{ rulify() -}}
{% for item in service | bystart(true) -%}

{{ rowify( [daterange(item.startdate, item.enddate),
            item.organization + ', ' + item.role ] ) }}
{% endfor %}
{{- rulify() }}

## Professional Memberships
{{ rulify() -}}
{% for item in memberships | bystart(true) -%}

{{ rowify( [daterange(item.startdate, item.enddate),
            item.organization + ', ' + ' ' + item.role ] ) }}
{% endfor %}
{{- rulify() }}

{{ pubs_section("Press", press) }}

{### Interests#}
{#{{ rulify() -}}#}
{#{% for item in interests -%}#}
{##}
{#{{ rowify( [item.keys()[0], #}
{#            item.values()[0]])}}#}
{#{% endfor %}#}
{#{{- rulify() }}#}

# Technical Proficiencies
{{ rulify() -}}
{% for item in technical_proficiencies -%}

{{ rowify( [list(item.keys())[0], 
           ', '.join(list(item.values())[0])])}}
{% endfor %}
{{- rulify() }}


---
suppress-bibliography: true
...
