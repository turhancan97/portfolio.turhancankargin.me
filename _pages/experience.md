---
layout: page
permalink: /experience/
title: experience
description: Professional experience, internships, and volunteer work in machine learning, robotics, and engineering.
nav: true
nav_order: 4
---

## Work Experience

<div class="experience-grid">
{% for item in site.data.experience.work %}
  <article class="experience-card card hoverable">
    <div class="experience-card-media">
      <img src="{{ item.image | relative_url }}" alt="{{ item.organization }}" loading="lazy">
    </div>
    <div class="experience-card-body">
      <h3 class="experience-card-title">{{ item.title }}</h3>
      <p class="experience-card-meta">
        {% if item.org_url %}
        <a href="{{ item.org_url }}" target="_blank" rel="noopener noreferrer">{{ item.organization }}</a>
        {% else %}
        {{ item.organization }}
        {% endif %}
        {% if item.location %}<br><span class="text-muted">{{ item.location }}</span>{% endif %}
        <br><span class="experience-card-period">{{ item.period }}</span>
      </p>
      <ul class="experience-card-list">
        {% for highlight in item.highlights %}
        <li>{{ highlight }}</li>
        {% endfor %}
      </ul>
    </div>
  </article>
{% endfor %}
</div>

## Volunteer Work

<div class="volunteer-grid">
{% for item in site.data.experience.volunteer %}
  <article class="volunteer-card card hoverable">
    <div class="volunteer-card-media">
      <img src="{{ item.image | relative_url }}" alt="{{ item.organization }}" loading="lazy">
    </div>
    <div class="volunteer-card-body">
      <h3 class="volunteer-card-title">{{ item.title }}</h3>
      <p class="volunteer-card-org">
        {% if item.org_url %}
        <a href="{{ item.org_url }}" target="_blank" rel="noopener noreferrer">{{ item.organization }}</a>
        {% else %}
        {{ item.organization }}
        {% endif %}
      </p>
      <p class="volunteer-card-text">{{ item.description }}</p>
    </div>
  </article>
{% endfor %}
</div>
