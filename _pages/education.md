---
layout: page
permalink: /education/
title: education
description: Academic degrees, exchange programs, and online courses in machine learning, robotics, and engineering.
nav: true
nav_order: 5
---

## Formal Education

<div class="education-timeline">
{% for item in site.data.education.degrees %}
  <article class="education-entry">
    <div class="education-entry-marker" aria-hidden="true"></div>
    <div class="education-entry-card card hoverable">
      <div class="education-entry-media{% if item.logo_size == 'large' %} education-entry-media--large{% endif %}">
        <img src="{{ item.image | relative_url }}" alt="{{ item.institution }} logo" loading="lazy">
      </div>
      <div class="education-entry-body">
        <div class="education-entry-period">{{ item.period }}</div>
        <h3 class="education-entry-title">
          {% if item.institution_url %}
          <a href="{{ item.institution_url }}" target="_blank" rel="noopener noreferrer">{{ item.institution }}</a>
          {% else %}
          {{ item.institution }}
          {% endif %}
        </h3>
        <p class="education-entry-degree">{{ item.degree }}</p>
        <ul class="education-entry-list">
          {% for highlight in item.highlights %}
          <li>{{ highlight }}</li>
          {% endfor %}
        </ul>
      </div>
    </div>
  </article>
{% endfor %}
</div>

## Online Accreditations

<div class="mooc-grid">
{% for item in site.data.education.moocs %}
  <a class="mooc-card card hoverable" href="{{ item.url }}" target="_blank" rel="noopener noreferrer">
    <div class="mooc-card-media">
      <img src="{{ item.image | relative_url }}" alt="" loading="lazy">
    </div>
    <p class="mooc-card-title">{{ item.title }}</p>
  </a>
{% endfor %}
</div>
