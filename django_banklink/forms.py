from django import forms 
from django_banklink import settings
from django_banklink.utils import create_signature

class PaymentRequest(forms.Form):
    VK_SERVICE = forms.CharField(widget = forms.HiddenInput())
    VK_VERSION = forms.CharField(widget = forms.HiddenInput())
    VK_SND_ID = forms.CharField(widget = forms.HiddenInput())
    VK_STAMP = forms.CharField(widget = forms.HiddenInput())
    VK_AMOUNT = forms.CharField(widget = forms.HiddenInput())
    VK_REF = forms.CharField(widget = forms.HiddenInput())
    VK_MSG = forms.CharField(widget = forms.HiddenInput())
    VK_MAC = forms.CharField(widget = forms.HiddenInput())
    VK_RETURN = forms.CharField(widget = forms.HiddenInput())
    VK_LANG = forms.CharField(widget = forms.HiddenInput())
    VK_ENCODING = forms.CharField(widget = forms.HiddenInput())
    def __init__(self, *args, **kwargs):
        initial = {} 
        initial['VK_STAMP'] = kwargs.get('description')
        initial['VK_AMOUNT'] = kwargs.get('amount')
        initial['VK_CURR'] = kwargs.get('currency', 'LVL')
        initial['VK_REF'] = kwargs.get('reference')
        initial['VK_MSG'] = kwargs.get('message')
        initial['VK_ENCODING'] = 'UTF-8'
        initial['VK_RETURN'] = kwargs.get('return_to')
        initial['VK_SERVICE'] = '1002'
        initial['VK_VERSION'] = '008'
        initial['VK_SND_ID'] = settings.SND_ID
        initial['VK_MAC'] = create_signature(initial)
        super(PaymentRequest, self).__init__(initial, *args)
    def as_html(self):
        html = u'<form action="%s" method="POST" enctype="multipart/form-data">' % (settings.BANKLINK_URL)
        for field in self:
            html += unicode(field)
        html += '</form>'
        return html 

    
    
    

