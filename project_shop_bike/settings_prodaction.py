DEBUG = False
AllOWED_HOSTS = ['*']  # ip address or *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'db1',
        'USER': 'chipmotors',
        'PASSWORD': 'django_shop_db',
        'HOST': 'localhost',
        'PORT': '',                 # Set to empty string for default.
    }
}
