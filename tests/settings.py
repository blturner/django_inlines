DATABASE_ENGINE = 'sqlite3'
DATABASE_NAME = 'django_inlines_tests.db'

ROOT_URLCONF = 'django_inlines.admin_urls'

INSTALLED_APPS = [
	'django.contrib.admin',
	'django.contrib.auth',
	'django.contrib.contenttypes',
	'django.contrib.sessions',
    'core',
    'django_inlines',
]
TEMPLATE_LOADERS = (
	'django.template.loaders.filesystem.load_template_source',
    'django.template.loaders.app_directories.load_template_source',
)
