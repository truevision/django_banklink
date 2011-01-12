from django.conf import settings 
from django.core.exceptions import ImproperlyConfigured

PRIVATE_KEY =  getattr(settings, 'BANKLINK_PRIVATE_KEY', None)
if not PRIVATE_KEY:
    raise ImproperlyConfigured(u"BANKLINK_PRIVATE_KEY not found in settings")

SND_ID = getattr(settings, 'BANKLINK_SND_ID', None)
if not SND_ID:
    raise ImproperlyConfigured(u"BANKLINK_SND_ID not found in settings")

PUBLIC_KEY = getattr(settings, 'BANKLINK_PUBLIC_KEY', None)
if not PUBLIC_KEY:
    raise ImproperlyConfigured(u"BANKLINK_PUBLIC_KEY not found in settings")

BANKLINK_URL = getattr(settings, 'BANKLINK_REQUEST_URL',
                                'https://ib.swedbank.lv/banklink')


