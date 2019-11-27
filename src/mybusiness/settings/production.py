from .base import *

DEBUG = False
ALLOWED_HOSTS = ['ip-address', 'mysite.com']

INSTALLED_APPS += [

]

MIDDLEWARE += [

]

AUTH_PASSWORD_VALIDATORS = [
    {'NAME':'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',},
    {'NAME':'django.contrib.auth.password_validation.MinimumLengthValidator',},
    {'NAME':'django.contrib.auth.password_validation.CommonPasswordValidator',},
    {'NAME':'django.contrib.auth.password_validation.NumericPasswordValidator',},
]

# SECURITY
CSRF_COOKIE_SECURE = True
CSRF_COOKIE_SAMESITE = 'Strict'
SESSION_COOKIE_SECURE = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_SSL_REDIRECT = True
X_FRAME_OPTIONS = 'DENY'
SECURE_HSTS_SECONDS = 300  # set low, but when site is ready for deployment, set to at least 15768000 (6 months)
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
