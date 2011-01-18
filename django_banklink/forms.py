from django import forms 
from django.core.urlresolvers import reverse 
from django.contrib.sites.models import Site
from django.utils.safestring import SafeUnicode
from django_banklink import settings
from django_banklink.utils import create_signature
from django_banklink.models import Transaction
from warnings import warn
from django_banklink.signals import transaction_started



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
        transaction = Transaction()
        transaction.user = kwargs.get('user')
        transaction.description = kwargs.get('message')
        transaction.amount = initial['VK_AMOUNT'] = kwargs.get('amount')
        transaction.currency = initial['VK_CURR'] = kwargs.get('currency', 'LVL')
        transaction.message = initial['VK_MSG'] = kwargs.get('message')
        initial['VK_ENCODING'] = 'UTF-8'
        initial['VK_RETURN'] = "%s%s" % (Site.objects.get_current().domain, reverse('django_banklink.views.response'))
        initial['VK_SERVICE'] = '1002'
        initial['VK_VERSION'] = '008'
        initial['VK_LANG'] = kwargs.get('language', 'LAT')
        initial['VK_SND_ID'] = settings.SND_ID
        transaction.redirect_after_success = kwargs.get('redirect_to')
        transaction.redirect_on_failure = kwargs.get('redirect_on_failure', transaction.redirect_after_success)
        transaction.save()
        transaction_started.send(Transaction, transaction = transaction)
        self.transaction = transaction
        initial['VK_REF'] = transaction.pk 
        initial['VK_STAMP'] = transaction.pk
        super(PaymentRequest, self).__init__(initial, *args)
        if self.is_valid():
            mac = create_signature(self.cleaned_data)
            self.data['VK_MAC'] = mac
            if not self.is_valid():
                raise RuntimeError("signature is invalid")
        else:
            raise RuntimeError("invalid initial data")

    def redirect_html(self):
        """ Hanzanet redirection html"""
        html = u'<form action="%s" method="POST" id="banklink_redirect_url">' % (settings.BANKLINK_URL)
        for field in self:
            html += unicode(field) + u"\n"
        html += u'</form>'
        html += u'''<script type="text/javascript">
                    document.forms['banklink_redirect_url'].submit();
                    </script>'''
        return SafeUnicode(html)
    def submit_button(self, value = u"Apmaksāt"):
        html = u'<form action="%s" method="POST">' % (settings.BANKLINK_URL)
        for field in self:
            html += unicode(field) + u"\n"
        html += '<input type="submit" value="%s" />' % (value)
        html += '</form>'
        return SafeUnicode(html)
    def as_html(self, with_submit = False, id = "banklink_payment_form", submit_value = "submit" ):
        """ return transaction form for redirect to HanzaNet """
        warn("deprecated", DeprecationWarning)
        html = u'<form action="%s" method="POST" id="%s">' % (settings.BANKLINK_URL, id)
        for field in self:
            html += unicode(field) + u"\n"
        if with_submit:
            html += '<input type="submit" value="%s"/>' % (submit_value, )
        html += '</form>'
        return html 
