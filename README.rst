* Link to `Django Girls Tutorial <https://tutorial.djangogirls.org/en/>`_

v1.01
=====

* upgrade to Django 2.0.x
* I don't remember which Django version I used before.

Upgrade:
--------

* `a nice blog as a guide: <https://www.codingforentrepreneurs.com/blog/django-version-20-a-few-key-features/>`_
* change url to re_path urls.py (two)
    - from django.urls import re_path
* add namespace: app_name = "blog" to blog/urls.py
    - update in all templates, {% url "blog:xxxxx" %}
    - update views in views.py: redirect("blog:xxxx", ...)
* python manage.py makemigrations && python manage.py migrate
* add localhost to ALLOWED_HOSTS in settings.py
* add SECRET_KEY in setings.py
* python manage.py createsuperuser
    - username: jeremy
    - password: AiFee2oo
* web: http://127.0.0.1:8000/blog/


v1.02
=====

* pip install django-debug-toolbar
* adjust settings and urlpatterns
* remap url for login and logout redirecting pages


v.103

* Upgrade Bootstrap from 3 to 4.1