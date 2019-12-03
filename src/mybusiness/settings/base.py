import os
from django.contrib.messages import constants as messages


BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SECRET_KEY = os.environ.get('SECRET_KEY_MIHAI_SITE')
SITE_ID = 1

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # own apps
    'blog.apps.BlogConfig',
    'core.apps.CoreConfig',
    'users.apps.UsersConfig',
    'cv.apps.CvConfig',

    # third-party apps
    'crispy_forms',
    'taggit',
    'django.contrib.sites',
    'django.contrib.sitemaps',
    'storages',
    'admin_honeypot',

    'pagedown.apps.PagedownConfig',
    'widget_tweaks',
    'markdown_deux',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    # my own
    'mybusiness.middleware.SetResponseHeader',
]

ROOT_URLCONF = 'mybusiness.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'mybusiness.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Europe/Bucharest'
USE_I18N = True
USE_L10N = True
USE_TZ = True

STATIC_ROOT = os.path.join(BASE_DIR, 'static_root')
STATIC_URL = '/static/'

CRISPY_TEMPLATE_PACK = 'bootstrap4'

LOGIN_REDIRECT_URL = 'blog:post_list' # change to post.get_absolute_url()?
LOGIN_URL = 'login'

# I'm changing just the tag of the error so that bootstrap4 alert and messages tags to be the same (danger).
# so messages.error -> tags == danger
MESSAGE_TAGS = {
    messages.ERROR: 'danger',
}

# EMAIL CONFIGURATION
# EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = os.environ.get('EMAIL_USER')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_PASS')
EMAIL_PORT = 587
EMAIL_USE_TLS = True


# django-storages & AWS settings
AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID_MIHAI_BUSINESS')
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY_MIHAI_BUSINESS')
AWS_STORAGE_BUCKET_NAME = os.environ.get('AWS_STORAGE_BUCKET_NAME_MIHAI_BUSINESS')
# If a user uploads a file with the same name as another user's filename .. don't overwrite the file... just add it with a different name
AWS_S3_FILE_OVERWRITE = False
AWS_DEFAULT_ACL = None
AWS_S3_SIGNATURE_VERSION = 's3v4'
AWS_S3_REGION_NAME = 'eu-central-1'
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
# To allow django-admin.py collectstatic to automatically put your static files in your bucket set the following in your settings.py:
# STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
