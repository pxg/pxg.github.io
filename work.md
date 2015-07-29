---
title: Work
permalink: work/
profile: true
---

<ul>
{% for album in site.work limit:3 %}
    <li>
        <p>{{ album.title }}</p>
    </li>
{% endfor %}
</ul>

{% include footer.html %}
