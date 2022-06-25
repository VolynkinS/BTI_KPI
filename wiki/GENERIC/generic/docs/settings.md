## Setting STATIC

```
STATIC_URL = 'static/'

# https://docs.djangoproject.com/en/4.0/ref/settings/#static-files

STATIC_ROOT = BASE_DIR / 'static'
STATICFILES_DIRS = [
    BASE_DIR / 'name_your_app/static',
]
```


## Setting MEDIA

```
# https://docs.djangoproject.com/en/4.0/ref/settings/#media-root

MEDIA_ROOT = BASE_DIR / 'media'
MEDIA_URL = 'media/'
```


## Setting email

```
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = os.getenv('EMAIL_PORT')
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')
EMAIL_USE_TLS = True
EMAIL_USE_SSL = False
```