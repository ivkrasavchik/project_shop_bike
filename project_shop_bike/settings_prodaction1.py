DEBUG = False
ALLOWED_HOSTS = ['192.168.0.200']  # ip address or *


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'db1',
        'USER': 'chipadmin',
        'PASSWORD': '1qsx2wdc',
        'HOST': 'localhost',
        'PORT': '',                 # Set to empty string for default.
    }
}
