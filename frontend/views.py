from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.http import Http404

from redirects.models import LiveRedirect

from frontend.forms import RedirectForm

def index(request):
    """
    This view renders the index template.
    """

    extra = {}

    if request.method == 'POST':
        # Redirects should be created using the API, this violates DRY
        form = RedirectForm(request.POST)
        if form.is_valid():
            r = form.save()
            response = redirect('frontend_success')

            # Add GET param to response
            response['Location'] += '?slug=%s' % r.slug

            return response
    else:
        form = RedirectForm()

    extra['form'] = form

    context = RequestContext(request,extra)
    return render_to_response('index.html',context)

def success(request):
    """
    View that user is taken to on successful creation of a redirect

    Seperate page for Google Analytics
    """

    slug = request.GET.get('slug')

    try:
        redirect = LiveRedirect.objects.get(slug=slug)
    except LiveRedirect.DoesNotExist:
        raise Http404 #Don't want to pollute the GAG

    extra = {
        'redirect':redirect
    }

    context = RequestContext(request,extra)

    return render_to_response('success.html',context)

def view_redirect(request,slug):
    """
    This view displays a redirect to the user
    """

    try:
        r = LiveRedirect.objects.get(slug=slug)
    except LiveRedirect.DoesNotExist:
        raise Http404
        #return redirect('frontend_index')

    extra = {
        'redirect':r,
    }

    context = RequestContext(request,extra)
    return render_to_response('redirect.html',context)
