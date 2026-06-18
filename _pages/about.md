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
    <p>ul. Prof. S. Łojasiewicza 6</p>
    <p>30-348 Kraków, Poland</p>

selected_papers: true
scholar:
  sort_by: selected_order
  order: ascending
social: true

announcements:
  enabled: true
  scrollable: true
  limit: 5

latest_posts:
  enabled: false
---

Turhan Can Kargin is a PhD researcher at the [Group of Machine Learning Research (GMUM)](https://gmum.net/), Jagiellonian University, supervised by [Bartosz Zieliński](https://bartoszzielinski.github.io/). His research focuses on self-supervised learning, spatial intelligence in visual foundation models, and robotics — particularly continuum robot control with reinforcement learning.

He has published on spatial reasoning benchmarks, reinforcement learning for continuum robots, and energy-efficient computing. Previously, he worked as a data scientist at the Poznan Supercomputing and Networking Center (PSNC), contributing to the EU RENergetic project and applied machine learning for energy systems.

{::nomarkdown}

<script>
  document.addEventListener('DOMContentLoaded', function () {
    const news = document.querySelector('article .news');
    if (!news || document.getElementById('see-previous-news')) {
      return;
    }
    const link = document.createElement('p');
    link.id = 'see-previous-news';
    link.className = 'mt-2 mb-0';
    link.innerHTML = '<a href="{{ "/news/" | relative_url }}">See previous news</a>';
    news.insertAdjacentElement('afterend', link);
  });
</script>

{:/nomarkdown}
