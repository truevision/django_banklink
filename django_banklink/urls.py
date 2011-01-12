from django.conf.urls.defaults import *

urlpatterns = patterns('django_banklink.views', 
    (r'^$', 'test_request'),
    (r'^response/$', 'test_response'),
)
