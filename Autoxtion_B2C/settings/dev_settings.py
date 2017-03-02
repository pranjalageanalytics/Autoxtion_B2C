from Autoxtion_B2C.settings.base import *
DB_PASSWORD = os.environ.get('DB_PASSWORD')
EMAIL_PASSWORD = os.environ.get('EMAIL_PASSWORD')

TEMPLATE_DEBUG=True

DEBUG = True

ALLOWED_HOSTS = []


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'auto',
        'USER':'root',
        'PASSWORD':DB_PASSWORD,
        'HOST': '127.0.0.1',
        'PORT':'3306'
    }
}

EMAIL_USE_TLS=True
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST='smtp.gmail.com'

EMAIL_HOST_USER='autoxtion.test1@gmail.com'
EMAIL_HOST_PASSWORD=EMAIL_PASSWORD
EMAIL_PORT=587
EMAIL_USE_TLS= True

