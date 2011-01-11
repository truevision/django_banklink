from M2Crypto import EVP
from django_banklink import settings
from base64 import b64encode 

def create_signature(request):
    """ 
        sign BankLink request in dict format with private_key
    """

    key = EVP.load_key(settings.PRIVATE_KEY)
    formatted = ''
    for val in request:
        formatted += unicode(len(val)).ljust(3, '0')
        formatted + val
    key.sign_init()
    key.sign_update(formatted)
    key_binary = key.sign_final()
    return b64encode(key_binary)
