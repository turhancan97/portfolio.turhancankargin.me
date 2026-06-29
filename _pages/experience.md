---
layout: page
permalink: /experience/
title: experience
description: Professional experience, awards, and service in machine learning, robotics, and engineering.
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

## Awards & Honors {#awards}

<ul class="awards-list list-unstyled mt-3">
{% assign sorted_awards = site.data.awards | sort: "date_sort" | reverse %}
{% for award in sorted_awards %}
  <li class="mb-3">
    <div class="text-muted small">{{ award.date }}{% if award.location %} · {{ award.location }}{% endif %}</div>
    <div>
      <strong>{{ award.title }}</strong> —
      {% if award.issuer_url %}
      <a href="{{ award.issuer_url }}" target="_blank" rel="noopener noreferrer">{{ award.issuer }}</a>
      {% else %}
      {{ award.issuer }}
      {% endif %}
    </div>
    {% if award.note %}
    <div class="fst-italic mt-1 small">{{ award.note | markdownify | remove: '<p>' | remove: '</p>' | strip }}</div>
    {% endif %}
  </li>
{% endfor %}
</ul>

## Service & Leadership {#service}

### Event organizing

<ul class="service-list list-unstyled mt-3 mb-4">
{% assign sorted_organizing = site.data.experience.organizing | sort: "date_sort" | reverse %}
{% for item in sorted_organizing %}
  <li class="mb-3">
    <div class="text-muted small">{{ item.date }} · {{ item.location }}</div>
    <div>
      <strong>{{ item.role }}</strong> —
      <a href="{{ item.url }}" target="_blank" rel="noopener noreferrer">{{ item.title }}</a>
    </div>
    {% if item.note %}
    <div class="fst-italic mt-1 small">{{ item.note | markdownify | remove: '<p>' | remove: '</p>' | strip }}</div>
    {% endif %}
  </li>
{% endfor %}
</ul>

### Outreach & education

<div class="volunteer-grid">
{% for item in site.data.experience.volunteer %}
  {% if item.category == "outreach" %}
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
        {% if item.period %}<br><span class="volunteer-card-period">{{ item.period }}</span>{% endif %}
      </p>
      <p class="volunteer-card-text">{{ item.description }}</p>
    </div>
  </article>
  {% endif %}
{% endfor %}
</div>

### Student organizations

<div class="volunteer-grid">
{% for item in site.data.experience.volunteer %}
  {% if item.category == "student-organization" %}
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
        {% if item.period %}<br><span class="volunteer-card-period">{{ item.period }}</span>{% endif %}
      </p>
      <p class="volunteer-card-text">{{ item.description }}</p>
    </div>
  </article>
  {% endif %}
{% endfor %}
</div>

### Community & media

<div class="volunteer-grid">
{% for item in site.data.experience.volunteer %}
  {% if item.category == "community" %}
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
        {% if item.period %}<br><span class="volunteer-card-period">{{ item.period }}</span>{% endif %}
      </p>
      <p class="volunteer-card-text">{{ item.description }}</p>
    </div>
  </article>
  {% endif %}
{% endfor %}
</div>
