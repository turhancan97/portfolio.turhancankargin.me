---
layout: page
permalink: /events/
title: events
description: Conferences, summer schools, and workshops attended or contributed to.
nav: true
nav_order: 7
---

Conferences, summer schools, and workshops — listed newest first.

<ul class="list-unstyled mt-3">
{% assign sorted_events = site.data.events | sort: "date_sort" | reverse %}
{% for event in sorted_events %}
  <li class="mb-4">
    <div class="text-muted small">{{ event.date }} · {{ event.location }}</div>
    <div>
      <strong>{{ event.role }}</strong> —
      <a href="{{ event.url }}" target="_blank" rel="noopener noreferrer">{{ event.title }}</a>
    </div>
    {% if event.presentation %}
    <div class="fst-italic mt-1">{{ event.presentation }}</div>
    {% endif %}
    {% if event.note %}
    <div class="fst-italic mt-1">{{ event.note | markdownify | remove: '<p>' | remove: '</p>' | strip }}</div>
    {% endif %}
  </li>
{% endfor %}
</ul>
