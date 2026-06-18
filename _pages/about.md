---
layout: about
title: about
permalink: /
subtitle: PhD Researcher at <a href="https://gmum.net/" target="_blank" rel="noopener">GMUM</a> (Group of Machine Learning Research), Jagiellonian University.

profile:
  align: right
  image: prof_pic.jpg
  image_circular: true
  more_info: >
    <p>Faculty of Mathematics and Computer Science</p>
    <p>Jagiellonian University</p>
    <p>Kraków, Poland</p>

selected_papers: true
social: true

announcements:
  enabled: true
  scrollable: true
  limit: 5

latest_posts:
  enabled: false
---

Turhan Can Kargin is a PhD researcher at the [Group of Machine Learning Research (GMUM)](https://gmum.net/), Jagiellonian University. His research focuses on self-supervised learning, spatial intelligence in visual foundation models, and robotics — particularly continuum robot control with reinforcement learning.

He has published on spatial reasoning benchmarks, reinforcement learning for continuum robots, and energy-efficient computing. Previously, he worked as a data scientist at the Poznan Supercomputing and Networking Center (PSNC), contributing to the EU RENergetic project and applied machine learning for energy systems.

## selected projects

<div class="projects">
<div class="row row-cols-1 row-cols-md-3">
{% assign sorted_projects = site.projects | sort: "importance" %}
{% for project in sorted_projects limit: 6 %}
  {% include projects.liquid %}
{% endfor %}
</div>
</div>

More projects are available on the [projects page](/projects/).
