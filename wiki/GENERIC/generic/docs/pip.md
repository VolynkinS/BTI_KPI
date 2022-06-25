# Social network


## Django Version 
`Django==4.0.5`


## Setting Jupyter

[jupyter](https://jupyter.org/install)

`pip install notebook`

Add to settings.py:
```
os.environ['DJANGO_ALLOW_ASYNC_UNSAFE'] = 'true'
```


## Setting django-extensions

[django-extensions](https://django-extensions.readthedocs.io/en/latest/)

`pip install django-extensions==3.1.5`


## Setting django_debug_toolbar

[django-debug-toolbar](https://django-debug-toolbar.readthedocs.io/en/latest/installation.html)

`django-debug-toolbar==3.4.0`

```
if settings.DEBUG:
    urlpatterns += [path('__debug__/', include('debug_toolbar.urls'))]
```


## Setting crispy-forms

[crispy-forms](https://django-crispy-forms.readthedocs.io/en/latest/index.html)

`django-crispy-forms==1.14.0`


## Setting cleanup

[cleanup](https://github.com/un1t/django-cleanup)

`pip install django-cleanup==6.0.0`

```
# cleanup must be placed last in INSTALLED_APPS
'django_cleanup.apps.CleanupConfig'
```


## Setting ckeditor

[ckeditor](https://pypi.org/project/django-ckeditor/)

`pip install django-ckeditor==6.4.2`


## Setting channels

[channels](https://channels.readthedocs.io/en/stable/)

`python -m pip install -U channels==3.0.4`


**Add to setting.py:**

```
ASGI_APPLICATION = 'name_your_project.asgi.application'

CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels.layers.InMemoryChannelLayer'
    },
}
```

**Create routing.py next to settings.py and add:**

```
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack

application = ProtocolTypeRouter({
    'websocket': AuthMiddlewareStack(
        URLRouter(
            # chat.routing.websocket_urlpatterns
        )
    ),
})
```


## Setting django-allauth

[django-allauth](https://django-allauth.readthedocs.io/en/latest/installation.html)

`pip install django-allauth==0.50.0`



## Setting dotenv

[dotenv](https://pypi.org/project/python-dotenv/)

`pip install python-dotenv==0.20.0`

``` 
from dotenv import load_dotenv

# File .env at the root of the project
# Loading ENV
env_path = Path('.') / '.env'  # Instead of Path('.') you can use BASE_DIR
load_dotenv(dotenv_path=env_path)
```


## Setting braces

[braces](https://django-braces.readthedocs.io/en/latest/)

`pip install django-braces==1.15.0`


## Setting mkdocs

[mkdocs](https://www.mkdocs.org/)

`pip install mkdocs==1.3.0`


## Setting mkdocs-material

[mkdocs-material](https://squidfunk.github.io/mkdocs-material/getting-started/#with-docker)

`pip install mkdocs-material==8.3.3`


## Setting django.contrib.humanize

[humanize](https://docs.djangoproject.com/en/4.0/ref/contrib/humanize/)

**To activate these filters, add 'django.contrib.humanize' to your INSTALLED_APPS setting. Once you’ve done that, use {% load humanize %} in a template, and you’ll have access to the following filters.**


## Pillow

`pip install Pillow==9.1.1`