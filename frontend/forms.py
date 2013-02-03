from django import forms
from redirects.models import LiveRedirect

class RedirectForm(forms.ModelForm):

	class Meta:
		model = LiveRedirect
		fields = ('url','duration')