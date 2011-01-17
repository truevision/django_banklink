from django.conf.urls.defaults import *

urlpatterns = patterns('django_banklink.views', 
    (r'^$', 'request', {'description': 'test_payment',
                        'message' : 'tests', 
                        'amount' : '0.05',
                        'currency' : 'LVL',
                        'redirect_to' : 'http://www.done.com/',
                        }),
    (r'^response/$', 'response'),
)
