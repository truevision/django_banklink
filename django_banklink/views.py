from django.template import RequestContext
from django.core.urlresolvers import reverse 
from django.http import HttpResponseRedirect
from django.http import HttpResponse 

from django.shortcuts import render_to_response
from django.shortcuts import get_object_or_404

from django.views.decorators.csrf import csrf_exempt

from django_banklink.forms import PaymentRequest
from django_banklink.utils import verify_signature
from django_banklink.models import Transaction

@csrf_exempt
def response(request):
    if request.method == 'POST':
        data = request.POST
    else: 
        data = request.GET
    if 'VK_MAC' not in data:
        raise Http404("VK_MAC not in request")
    signature_valid = verify_signature(data, data['VK_MAC'])
    if not signature_valid:
        raise Http404("Invalid signature. ")
    transaction = get_object_or_404(Transaction, pk = data['VK_REF'])  
    if data['VK_AUTO'] == 'Y':
        transaction.status = 'C'
        transaction.save()
        return HttResponse("request handled, swedbank")
    else:
        if data['VK_SERVICE'] == '1901':
            url = transaction.redirect_on_failure
            transaction.status = 'F'
            transaction.save()
        else:
            url = transaction.redirect_on_success 
        return HttpResponseRedirect(url)

def request(request, description, message, amount, currency, redirect_to):
    if 'HTTP_HOST' not in request.META:
        raise Http404("HTTP/1.1 protocol only, specify Host header")
    protocol = 'https' if request.is_secure() else 'http'
    url = '%s://%s%s' % (protocol, request.META['HTTP_HOST'], reverse(response))
    context = RequestContext(request)
    user = None if request.user.is_anonymous() else request.user 
    context['form'] = PaymentRequest(description = description,
                                     amount = amount,
                                     currency = currency,
                                     redirect_to = redirect_to,
                                     return_to = url,
                                     message = message,
                                     user = user)
    return render_to_response("django_banklink/request.html", context)
