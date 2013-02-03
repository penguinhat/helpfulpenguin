from django.conf.urls import patterns, url
from rest_framework.urlpatterns import format_suffix_patterns

from redirects import views

urlpatterns = patterns('redirects.views',
    url(r'^list/$',
        views.RedirectList.as_view(),
        name='live_redirect_list'),
)

urlpatterns = format_suffix_patterns(urlpatterns)