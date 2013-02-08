from django.shortcuts import render_to_response
from django.template import RequestContext

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
			extra['redirect'] = r

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
		raise Http404
		#return redirect('frontend_index')

	extra = {
		'redirect':r,
	}

	context = RequestContext(request,extra)
	return render_to_response('redirect.html',context)