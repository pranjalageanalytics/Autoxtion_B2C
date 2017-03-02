from Autoxtion_B2C.settings.base import *
import re
IGNORABLE_404_URLS = [
    re.compile(r'\.(php|cgi)$'),
    re.compile(r'^/phpmyadmin/'),
]
DB_PASSWORD = os.environ['DB_PASSWORD']
EMAIL_PASSWORD = os.environ['EMAIL_PASSWORD']

DEBUG=True
SERVER_EMAIL= 'info@autoxtion.com.au'
ADMINS = (
    ('akshay', 'akshay@citadelsolutions.co'),
    ('sachin', 'sachin.gera@citadelsolutions.co'),
    ('onsite', 'guggs24@gmail.com'),
    ('Nikita', 'nikita.j@ageanalytics.co'),
)
MANAGERS = ADMINS
ALLOWED_HOSTS = ['198.15.126.59:8010']
CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
            'LOCATION': '127.0.0.1:11211',
            'TIMEOUT':'1800',
            }
	}
CACHE_MIDDLEWARE_SECONDS = 1800,

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

EMAIL_HOST_USER='citadel.test.auto@gmail.com'
EMAIL_HOST_PASSWORD=EMAIL_PASSWORD
EMAIL_PORT=587
EMAIL_USE_TLS= True



#twiliio settings
TWILIO_ACCOUNT_SID = 'AC2efe2d17085e84170d6a1e136ec6a45b'
TWILIO_AUTH_TOKEN = 'af2fc42bf3f4946efa6193d3e293b409'
TWILIO_NUMBER='+61427423289'



#CELERY SETTINGS

BROKER_URL = 'redis://127.0.0.1:6380'
CELERY_RESULT_BACKEND = 'redis://127.0.0.1:6380'
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'




#Push Notification Settings

PUSH_NOTIFICATIONS_SETTINGS = {
         # "GCM_API_KEY": "AIzaSyB55-Zl8XFGmTQRZpuhs9iCX0wu0iM-hbI",
         # "GCM_API_KEY": "AIzaSyBQMaBv_IchWU8moAzQOer6VVyIO-URiTc",
         "APNS_CERTIFICATE": "/home/administrator/autoxtionnew/Autoxtion_B2C/Certificates/AutoConnect.pem",
 }

FCM_DJANGO_SETTINGS = {
        "FCM_SERVER_KEY": "AIzaSyAdoJT7AX-SP9aULw4CbpFHw-zohUQfhm4"
}

#AWS Mail setting


#Recaptcha Key

RECAPTCHA_PUBLIC_KEY = '6LeIxAcTAAAAAJcZVRqyHh71UMIEGNQ_MXjiZKhI'
RECAPTCHA_PRIVATE_KEY = '6LeIxAcTAAAAAGG-vFI1TnRWxMZNFuojJ4WifJWe'
NOCAPTCHA = True
