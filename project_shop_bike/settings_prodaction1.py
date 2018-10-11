DEBUG = False
ALLOWED_HOSTS = ['localhost']  # ip address or *


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
