from django import forms 
from django_banklink import settings
from django_banklink.utils import create_signature

class PaymentRequest(forms.Form):
    VK_SERVICE = forms.CharField(widget = forms.HiddenInput())
    VK_VERSION = forms.CharField(widget = forms.HiddenInput())
    VK_SND_ID = forms.CharField(widget = forms.HiddenInput())
    VK_STAMP = forms.CharField(widget = forms.HiddenInput())
    VK_AMOUNT = forms.CharField(widget = forms.HiddenInput())
    VK_CURR = forms.CharField(widget = forms.HiddenInput())
    VK_REF = forms.CharField(widget = forms.HiddenInput())
    VK_MSG = forms.CharField(widget = forms.HiddenInput())
    VK_MAC = forms.CharField(widget = forms.HiddenInput(), required = False)
    VK_RETURN = forms.CharField(widget = forms.HiddenInput())
    VK_LANG = forms.CharField(widget = forms.HiddenInput())
    VK_ENCODING = forms.CharField(widget = forms.HiddenInput())
    def __init__(self, *args, **kwargs):
        initial = {} 
        initial['VK_STAMP'] = kwargs.get('description')
        initial['VK_MSG'] = kwargs.get('message')
        initial['VK_AMOUNT'] = kwargs.get('amount')
        initial['VK_CURR'] = kwargs.get('currency', 'LVL')
        initial['VK_REF'] = kwargs.get('reference')
        initial['VK_MSG'] = kwargs.get('message')
        initial['VK_ENCODING'] = 'UTF-8'
        initial['VK_RETURN'] = kwargs.get('return_to')
        initial['VK_SERVICE'] = '1002'
        initial['VK_VERSION'] = '008'
        initial['VK_LANG'] = kwargs.get('language', 'LAT')
        initial['VK_SND_ID'] = settings.SND_ID
        super(PaymentRequest, self).__init__(initial, *args)
        if self.is_valid():
            mac = create_signature(self.cleaned_data)
            self.data['VK_MAC'] = mac
            if not self.is_valid():
                raise RuntimeError("signature is invalid")
        else:
            print self.errors
            raise RuntimeError("invalid initial data")
    def as_html(self, with_submit = False, id = "banklink_payment_form"):
        html = u'<form action="%s" method="POST" id="%s">' % (settings.BANKLINK_URL, id)
        for field in self:
            html += unicode(field) + u"\n"
        if with_submit:
            html += '<input type="submit" />'
        html += '</form>'
        return html 
