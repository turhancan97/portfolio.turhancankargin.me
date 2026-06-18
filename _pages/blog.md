---
layout: default
permalink: /blog/
title: blog
description: Articles published here and syndicated from turhancankargin.com and Medium.
nav: true
nav_order: 6
pagination:
  enabled: true
  collection: posts
  permalink: /page/:num/
  per_page: 5
  sort_field: date
  sort_reverse: true
  trail:
    before: 1
    after: 3
---

<div class="post">

{% assign blog_name_size = site.blog_name | size %}
{% assign blog_description_size = site.blog_description | size %}

{% if blog_name_size > 0 or blog_description_size > 0 %}

  <div class="header-bar">
    <h1>{{ site.blog_name }}</h1>
    <h2>{{ site.blog_description }}</h2>
  </div>
{% endif %}

{% if site.display_tags and site.display_tags.size > 0 or site.display_categories and site.display_categories.size > 0 %}

  <div class="tag-category-list">
    <ul class="p-0 m-0">
      {% for tag in site.display_tags %}
        <li>
          <i class="fa-solid fa-hashtag fa-sm"></i> {{ tag }}
        </li>
        {% unless forloop.last %}
          <p>&bull;</p>
        {% endunless %}
      {% endfor %}
      {% if site.display_categories.size > 0 and site.display_tags.size > 0 %}
        <p>&bull;</p>
      {% endif %}
      {% for category in site.display_categories %}
        <li>
          <i class="fa-solid fa-tag fa-sm"></i> {{ category }}
        </li>
        {% unless forloop.last %}
          <p>&bull;</p>
        {% endunless %}
      {% endfor %}
    </ul>
  </div>
{% endif %}

{% assign featured_posts = site.posts | where: "featured", "true" %}
{% if featured_posts.size > 0 %}
  <br>

  <div class="container featured-posts">
    {% assign is_even = featured_posts.size | modulo: 2 %}
    <div class="row row-cols-{% if featured_posts.size <= 2 or is_even == 0 %}2{% else %}3{% endif %}">
      {% for post in featured_posts %}
        <div class="col mb-4">
          <a href="{{ post.url | relative_url }}">
            <div class="card hoverable">
              <div class="row g-0">
                <div class="col-md-12">
                  <div class="card-body">
                    <h3 class="card-title">{{ post.title }}</h3>
                    <p>{{ post.description }}</p>

                    {% if post.external_source == blank %}
                      {% assign read_time = post.content | number_of_words | divided_by: 180 | plus: 1 %}
                    {% else %}
                      {% assign read_time = post.feed_content | strip_html | number_of_words | divided_by: 180 | plus: 1 %}
                    {% endif %}
                    {% assign year = post.date | date: "%Y" %}

                    <p class="post-meta">
                      {{ read_time }} min read &nbsp; &middot; &nbsp;
                      <a href="{{ blog.url | relative_url }}/{{ year }}">
                        <i class="fa-solid fa-calendar fa-sm"></i> {{ year }} </a>
                    </p>
                  </div>
                </div>
              </div>
            </div>
          </a>
        </div>
      {% endfor %}
    </div>
  </div>
{% endif %}

  <ul class="post-list">

    {% if page.pagination.enabled %}
      {% assign postlist = paginator.posts %}
    {% else %}
      {% assign postlist = site.posts %}
    {% endif %}

    {% for post in postlist %}

    {% if post.external_source == blank %}
      {% assign read_time = post.content | number_of_words | divided_by: 180 | plus: 1 %}
    {% else %}
      {% assign read_time = post.feed_content | strip_html | number_of_words | divided_by: 180 | plus: 1 %}
    {% endif %}
    {% assign year = post.date | date: "%Y" %}
    {% assign tags = post.tags | join: "" %}
    {% assign categories = post.categories | join: "" %}

    <li>

{% if post.thumbnail %}

<div class="row">
  <div class="col-sm-9">
{% endif %}
      <h3>
        {% if post.redirect == blank %}
          <a class="post-title" href="{{ post.url | relative_url }}">{{ post.title }}</a>
        {% elsif post.redirect contains '://' %}
          <a class="post-title" href="{{ post.redirect }}" target="_blank">{{ post.title }}</a>
          <svg width="2rem" height="2rem" viewBox="0 0 40 40" xmlns="http://www.w3.org/2000/svg">
            <path d="M17 8.5L26.5 8L26.5 17" stroke="#999999" stroke-width="2"/>
            <path fill="currentColor" d="M14 9.5C14 8.67157 14.6716 8 15.5 8L24.5 8C25.3284 8 26 8.67157 26 9.5V18.5C26 19.3284 25.3284 20 24.5 20H23.2071C22.7616 20 22.5 19.5523 22.5 19.1071V12.5H15.8929C15.4477 12.5 15 12.2384 15 11.7929V9.5C15 8.67157 15.6716 8 16.5 8H14Z"></path>
            <path fill="currentColor" d="M14.5 29.5L25.5 18.5L28.3284 21.3284C28.7189 21.7189 28.7189 22.3521 28.3284 22.7426L18.3284 32.7426C17.9379 33.1331 17.3047 33.1331 16.9142 32.7426L14.0858 29.9142C13.6953 29.5237 13.6953 28.8905 14.0858 28.5L14.5 29.5ZM18.3284 32.7426L19.7426 31.3284L18.3284 32.7426Z"></path>
          </svg>
        {% else %}
          <a class="post-title" href="{{ post.redirect | relative_url }}">{{ post.title }}</a>
        {% endif %}
      </h3>
      <p>{{ post.description }}</p>
      <p class="post-meta">
        {{ read_time }} min read &nbsp; &middot; &nbsp;
        {{ post.date | date: '%B %d, %Y' }}
        {% if post.external_source %}
        &nbsp; &middot; &nbsp; {{ post.external_source }}
        {% endif %}
        {% if post.redirect contains '://' %}
        &nbsp; &middot; &nbsp; <i class="fa-solid fa-link"></i> <a href="{{ post.redirect }}">external link</a>
        {% endif %}
      </p>
      <p class="post-tags">
        <a href="{{ blog.url | relative_url }}/{{ year }}">
          <i class="fa-solid fa-calendar fa-sm"></i> {{ year }} </a>

      {% if tags != "" %}
      &nbsp; &middot; &nbsp;
        {% for tag in post.tags %}
        <a href="{{ blog.url | relative_url }}/tag/{{ tag | downcase | replace: ' ', '-' }}">
          <i class="fa-solid fa-hashtag fa-sm"></i> {{ tag }}</a>
          {% unless forloop.last %}
            &nbsp;
          {% endunless %}
        {% endfor %}
      {% endif %}

      {% if categories != "" %}
      &nbsp; &middot; &nbsp;
        {% for category in post.categories %}
        <a href="{{ blog.url | relative_url }}/category/{{ category | downcase | replace: ' ', '-' }}">
          <i class="fa-solid fa-tag fa-sm"></i> {{ category }}</a>
          {% unless forloop.last %}
            &nbsp;
          {% endunless %}
        {% endfor %}
      {% endif %}
    </p>

{% if post.thumbnail %}

  </div>
  <div class="col-sm-3">
    <img class="card-img" src="{{ post.thumbnail | relative_url }}" style="object-fit: cover; max-width: 100%;" alt="image">
  </div>
</div>
{% endif %}
    </li>

    {% endfor %}

  </ul>

{% if page.pagination.enabled %}
{% include pagination.liquid %}
{% endif %}

</div>
