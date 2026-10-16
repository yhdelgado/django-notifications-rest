``django-notifications-rest`` Documentation
=======================================

[django-notifications-rest](https://github.com/yhdelgado/django-notifications-rest) provides rest endpoints for ``django-notifications-hq``.

Requirements
============

- Python 3.11 - 3.14
- Django 5.2 - 6.1
- [django-notifications-community](https://github.com/django-notifications-community/django-notifications-community) latest version.
  It is a drop-in fork of ``django-notifications-hq``, whose last PyPI release (1.8.3) does not run on Django 5.1+ or Python 3.12+.
- djangorestframework latest version

Installation
============

Installation using ``pip``. You need to manually install the required ``django-notifications-community`` and ``djangorestframework`` packages.
    
    $ pip install django-notifications-rest

or get it from source

    $ git clone https://github.com/yhdelgado/django-notifications-rest.git
    $ cd django-notifications-rest
    $ python setup.py sdist
    $ pip install dist/django-notifications-rest*

Then to add the Django Notifications Rest to your project add the app ``notifications_rest`` to your ``INSTALLED_APPS`` and urlconf.

The app should go somewhere after all the apps that are going to be generating notifications like ``django.contrib.auth``

    INSTALLED_APPS = (
        'django.contrib.auth',
        'rest_framework',
        'notifications'.
        ...
        'notifications_rest',
        ...
    )

Add the notifications urls to your urlconf::

    urlpatterns = [
        ...
        url('^notifications/', include('notifications_rest.urls')),
        ...
    ]
If the installed version of django>=3.1, then::

    from django.urls import path, include
    urlpatterns = [
        ...
        path('^notifications/', include('notifications_rest.urls')),
        ...
    ]
 
To run schema migration, execute ``python manage.py migrate``.

-------------------
Additional options:
-------------------

There is also ``/add/`` API endpoint to add new notifications. Such endpoint might be considered security risk, as any user can add any notifications. For that reason, it must be manually enabled by setting ``NOTIFICATIONS_API_ALLOW_ADD=True``

The ``recipient`` must be an existing user. ``actor``, ``target`` and ``action_object`` are given as ``{"content_type_id": ..., "pk": ...}``; each must be the requesting user, or an object of a model the requesting user has Django's ``view`` permission for (superusers have all permissions). Anything else is rejected with 400, the same as an object that does not exist.

## `django-notifications-rest` Team

Core contributors (in alphabetical order):

-   [Petr Dlouhý](https://github.com/PetrDlouhy)
-   [Yusniel Hidalgo Delgado](https://github.com/yhdelgado)
