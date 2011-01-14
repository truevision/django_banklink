from django.shortcuts import render_to_response
from django_banklink.forms import PaymentRequest
from django.template import RequestContext
from django.core.urlresolvers import reverse 
from django_banklink.utils import verify_signature
from django.http import Http404
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def test_response(request):
    if request.method == 'POST':
        data = request.POST
    else: 
        data = request.GET
    if 'VK_MAC' not in data:
        raise Http404("VK_MAC not in request")
    context = RequestContext(request)
    context['signature_valid'] = verify_signature(data, data['VK_MAC'])
    context['data'] = data
    return render_to_response("django_banklink/test_response.html", context)

def test_request(request):
    context = RequestContext(request)
    url= "http://%s%s" % (request.META['HTTP_HOST'], reverse(test_response))
   
    context['form'] = PaymentRequest(description = 'test payment', 
                                      amount = '0.05', 
                                      reference = 'test',
                                      return_to = url, message = "testing payment").as_html(with_submit = True)
    return render_to_response("django_banklink/test_request.html", context)

