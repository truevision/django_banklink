from M2Crypto import EVP
from M2Crypto import RSA
from M2Crypto import X509

from django_banklink import settings
from base64 import b64encode
from base64 import b64decode 

def get_ordered_request(request):
    def append_if_exists(target, source, value):
        if value in source:
            target.append(source[value])
        return target
    expected_values = ('VK_SERVICE',
                        'VK_VERSION',
                        'VK_SND_ID',
                        'VK_REC_ID',
                        'VK_STAMP',
                        'VK_T_NO',
                        'VK_AMOUNT',
                        'VK_CURR',
                        'VK_REC_ACC',
                        'VK_REC_NAME',
                        'VK_SND_ACC',
                        'VK_SND_NAME',
                        'VK_REF',
                        'VK_MSG',
                        'VK_T_DATE',)

    ordered_request = []
    for value in expected_values:
        ordered_request = append_if_exists(ordered_request, request, value)
    return ordered_request
def request_digest(request):
    """ 
        return request digest in Banklink signature form (see docs for format)
    """
    request = get_ordered_request(request)
    digest = r''
    for value in request:
        
        digest += unicode(len(value)).rjust(3, u'0')
        digest += unicode(value)
    return digest

def create_signature(request):
    """ 
        sign BankLink request in dict format with private_key
    """

    key = EVP.load_key(settings.PRIVATE_KEY)
    digest = request_digest(request)
    key.reset_context(md = 'sha1')
    key.sign_init()
    key.sign_update(digest)
    key_binary = key.sign_final()
    b21 = b64encode(key_binary)
    return b21 

def verify_signature(request, signature):
    """
        verify BankLink reply signature
    """
    signature = unicode(signature)
    cert = X509.load_cert(settings.PUBLIC_KEY)
    pubkey = cert.get_pubkey()
    pubkey.verify_init()
    pubkey.verify_update(request_digest(request))
    if pubkey.verify_final(b64decode(signature)) == 1:
        return True
    else:
        return False
