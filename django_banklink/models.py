from django.db import models 
from django.utils.translation import ugettext_lazy as _ 
from django.contrib.auth.models import User 

TRANSACTION_STATUS = (
    ('P', _('pending')),
    ('F', _('failed')),
    ('C', _('complete')),
)

class Transaction(models.Model):
    user = models.ForeignKey(User, blank = True, null = True, default = None,
                             verbose_name = _("user"), help_text = _("user who started transaction"))
    description = models.CharField(_("reference description"), max_length = 255, help_text = _("reference description"))
    amount = models.FloatField(_("amount"))
    currency = models.CharField(_("currency"), max_length = 3)
    details = models.CharField(_("details"), max_length = 255, help_text = _("payment details"))
    created = models.DateTimeField(auto_now_add = True)
    last_modified = models.DateTimeField(auto_now = True)
    status = models.CharField(_("status"), max_length = 1, default = 'P')
    redirect_after_success = models.CharField(max_length = 255, editable = False)
    redirect_on_failure = models.CharField(max_length = 255, editable = False)

    def __unicode__(self):
        return _("transaction %s " % self.pk)
    class Meta:
        verbose_name = _("transaction")
        ordering = ['-last_modified']


