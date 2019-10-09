% {{ title }}  
% {% for a in authors %}{{people[a]['name']}}; {%endfor%}  
% {{ date | strftime }}  
  
{{ title }}
=============================
{% for a in authors %}
- {{ people[a]['name'] }}
  {%- if people[a].get('credential') %}, {{ people[a]['credential'] }}{% endif %}
  {%- if people[a].get('affiliation') %}, {{ people[a]['affiliation'] }}{% endif %}
  {%- if people[a].get('email') %}, <mailto:{{ people[a]['email'] }}>{% endif %}
{%- endfor %}

{{ date | strftime }}