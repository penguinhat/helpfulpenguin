from django.conf.urls import patterns, url
from rest_framework.urlpatterns import format_suffix_patterns

from redirects import views

urlpatterns = patterns('redirects.views',
    url(r'^list/$',
        views.RedirectList.as_view(),
        name='live_redirect_api'),
    url(r'^$',
        views.RedirectDetails.as_view(),
        name='live_redirect_details'),
    url(r'^(?P<slug>\w+)$',
        views.RedirectDetails.as_view(),
        name='live_redirect_details'),
)

urlpatterns = format_suffix_patterns(urlpatterns)