from django import forms
from redirects.models import LiveRedirect, DURATION_CHOICES

class RedirectForm(forms.ModelForm):

    duration = forms.ChoiceField(DURATION_CHOICES)

    class Meta:
        model = LiveRedirect
        fields = ('url','duration')