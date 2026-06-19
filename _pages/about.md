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

Turhan Can Kargın is a PhD Researcher at the [Group of Machine Learning Research (GMUM)](https://gmum.net/) at Jagiellonian University, supervised by [Prof. Bartosz Zieliński](https://bartoszzielinski.github.io/). He drives research at the intersection of self-supervised learning, spatial intelligence in visual foundation models, and robotics.

He has authored multiple publications advancing spatial reasoning benchmarks, reinforcement learning for robotics, and energy-efficient computing methodologies.

Previously, as a Data Scientist at the [Poznań Supercomputing and Networking Center (PSNC)](https://www.psnc.pl/), he developed applied machine learning solutions for energy systems within the EU-funded [RENergetic](https://www.renergetic.eu/) project. He further broadened his research scope by executing two Erasmus+ internships: engineering AI models for robotic object picking at the [University of Catania](https://www.unict.it/en) (supervised by [Prof. Giovanni Muscato](https://sites.google.com/site/muscatopersonalpage/robotics) and [Prof. Dario Calogero Guastella](https://scholar.google.com/citations?user=TojZzR8AAAAJ&hl=it)), and clustering single-cell RNA sequencing data at the [Silesian University of Technology](https://www.polsl.pl/en) (supervised by [Prof. Michal Marczyk](https://scholar.google.com/citations?user=mL-nyRAAAAAJ&hl=en)).

Selected open-source repositories are highlighted on the [repository overview](/repositories/) page.

{::nomarkdown}

{% assign loc = site.data.current_location %}
{% if loc.city and loc.country %}

<script>
  document.addEventListener('DOMContentLoaded', function () {
    const profile = document.querySelector('article .profile');
    if (!profile || profile.querySelector('.current-location')) {
      return;
    }
    const block = document.createElement('div');
    block.className = 'current-location';
    block.innerHTML =
      '<p><i class="fa-solid fa-location-dot" aria-hidden="true"></i>' +
      '<span class="current-location-label">{{ loc.label | default: "Currently in" }} </span>' +
      '<span class="current-location-place">{{ loc.city }}, {{ loc.country }}</span></p>';
    const moreInfo = profile.querySelector('.more-info');
    if (moreInfo) {
      profile.insertBefore(block, moreInfo);
    } else {
      profile.appendChild(block);
    }
  });
</script>

{% endif %}

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
