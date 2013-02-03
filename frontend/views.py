from django.shortcuts import render_to_response, redirect
from django.template import RequestContext

from redirects.models import LiveRedirect

from frontend.forms import RedirectForm

def index(request):
	"""
	This view renders the index template. If there is a slug then
	it tries to find a LiveRedirect with the same slug.
	"""

	extra = {}

	if request.method == 'POST':
		# Redirects should be created using the API, this violates DRY
		form = RedirectForm(request.POST)
		if form.is_valid():
			r = form.save()
			return redirect('live_redirect',r.slug)

	else:
		form = RedirectForm()

	extra['form'] = form

	context = RequestContext(request,extra)
	return render_to_response('index.html',context)

def view_redirect(request,slug):
	"""
	This view displays a redirect to the user
	"""

	try:
		r = LiveRedirect.objects.get(slug=slug)
	except LiveRedirect.DoesNotExist:
		return redirect('index')

	extra = {
		'redirect':r,
	}

	context = RequestContext(request,extra)
	return render_to_response('redirect.html',context)
