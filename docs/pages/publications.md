---
title: Publications
category: Publications
order: 1
layout: default
---

<!--- Make sure the publication are sorted -->
{% assign publications = site.data.publications | group_by_exp: "pub", "pub.year | append: pub.date | append: pub.bibcode" | sort: "name" | reverse | map: "items" %}



## Publications endorsed by the Initiative

{% assign current_year = "" %}
{% for pub_items in publications %}
{% assign pub = pub_items.first %}
{% if current_year != pub.year %}
{% assign current_year = pub.year %}
### {{ pub.year }}
{% endif %}
**{{ pub.title }}**, {{ pub.authors }}, [{{ pub.journal }}, {{ pub.volume }}, {{ pub.page }}](https://dx.doi.org/{{ pub.doi }}) ({{ pub.year }}) [[arXiv](https://arxiv.org/abs/{{ pub.arxiv | remove: "arXiv:" }})][[ADS](https://ui.adsabs.harvard.edu/abs/{{ pub.bibcode }})]
{% endfor %}
