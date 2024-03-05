---
layout: default
title: CADD Vault Homepage
---

# Welcome to the CADD Vault

This vault is a curated collection of resources, tools, and tutorials dedicated to Computer-Aided Drug Design (CADD). It is aimed at researchers, students, and professionals interested in the intersection of computational methods and pharmaceutical development.

<h2>Table of Contents</h2>

{% assign sorted_pages = site.pages | sort: 'path' %}
{% for page in sorted_pages %}
  {% if page.path contains 'subdirectory1/' or page.path contains 'subdirectory2/' %}
    <details>
      <summary>{{ page.dir | remove_first: '/' }}</summary>
      <a href="{{ site.baseurl }}{{ page.url }}">{{ page.title }}</a>
    </details>
  {% endif %}
{% endfor %}

## Contributing

This vault is an open-source project, and contributions are welcome. If you have resources, tools, or tutorials relevant to computer-aided drug design that you'd like to add, please see our contribution guidelines.

---

Thank you for visiting the CADD Vault. We hope you find these resources helpful in your research and development efforts.
