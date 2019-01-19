import os

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(PROJECT_ROOT, 'django_inlines_tests.db'),
    }
}

ROOT_URLCONF = 'django_inlines.admin_urls'

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'core',
    'django_inlines',
]

# TEMPLATE_LOADERS = (
#   'django.template.loaders.filesystem.load_template_source',
#     'django.template.loaders.app_directories.load_template_source',
# )

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(PROJECT_ROOT, 'templates'),],
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
            'loaders': [
                ('django.template.loaders.cached.Loader', (
                    'django.template.loaders.filesystem.Loader',
                    'django.template.loaders.app_directories.Loader',
                )),
            ],
        },
    },
]

SECRET_KEY = 'foo'
