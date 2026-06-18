---
layout: page
title: projects
permalink: /projects/
description: Research, software, and engineering projects in machine learning, robotics, and computer vision.
nav: true
nav_order: 3
display_categories: [research, software, industry, coursework]
horizontal: false
---

<div class="projects">
{% if site.enable_project_categories and page.display_categories %}
  {% for category in page.display_categories %}
  <a id="{{ category }}" href=".#{{ category }}">
    <h2 class="category">{{ category }}</h2>
  </a>
  {% assign categorized_projects = site.projects | where: "category", category %}
  {% assign sorted_projects = categorized_projects | sort: "importance" %}
  <div class="projects-grid">
    {% for project in sorted_projects %}
    <div class="project-item">
      <article class="card hoverable">
        <a
          class="project-card-link"
          href="{% if project.redirect %}{{ project.redirect }}{% else %}{{ project.url | relative_url }}{% endif %}"
        >
          {% if project.img %}
          {%
            include figure.liquid
            loading="eager"
            path=project.img
            sizes="(min-width: 768px) 50vw, 100vw"
            alt="project thumbnail"
            class="card-img-top"
          %}
          {% endif %}
          <div class="card-body">
            <h2 class="card-title">{{ project.title }}</h2>
            <p class="card-text">{{ project.description }}</p>
          </div>
        </a>
        {% if project.github %}
        <div class="project-card-footer">
          <div class="github-icon">
            <div class="icon" data-toggle="tooltip" title="Code Repository">
              <a href="{{ project.github }}"><i class="fa-brands fa-github gh-icon"></i></a>
            </div>
            {% if project.github_stars %}
            <span class="stars" data-toggle="tooltip" title="GitHub Stars">
              <i class="fa-solid fa-star"></i>
              <span id="{{ project.github_stars }}-stars"></span>
            </span>
            {% endif %}
          </div>
        </div>
        {% endif %}
      </article>
    </div>
    {% endfor %}
  </div>
  {% endfor %}
{% else %}
  {% assign sorted_projects = site.projects | sort: "importance" %}
  <div class="projects-grid">
    {% for project in sorted_projects %}
    <div class="project-item">
      <article class="card hoverable">
        <a
          class="project-card-link"
          href="{% if project.redirect %}{{ project.redirect }}{% else %}{{ project.url | relative_url }}{% endif %}"
        >
          {% if project.img %}
          {%
            include figure.liquid
            loading="eager"
            path=project.img
            sizes="(min-width: 768px) 50vw, 100vw"
            alt="project thumbnail"
            class="card-img-top"
          %}
          {% endif %}
          <div class="card-body">
            <h2 class="card-title">{{ project.title }}</h2>
            <p class="card-text">{{ project.description }}</p>
          </div>
        </a>
        {% if project.github %}
        <div class="project-card-footer">
          <div class="github-icon">
            <div class="icon" data-toggle="tooltip" title="Code Repository">
              <a href="{{ project.github }}"><i class="fa-brands fa-github gh-icon"></i></a>
            </div>
            {% if project.github_stars %}
            <span class="stars" data-toggle="tooltip" title="GitHub Stars">
              <i class="fa-solid fa-star"></i>
              <span id="{{ project.github_stars }}-stars"></span>
            </span>
            {% endif %}
          </div>
        </div>
        {% endif %}
      </article>
    </div>
    {% endfor %}
  </div>
{% endif %}
</div>
