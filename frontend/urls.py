from django.conf.urls import patterns, url

from frontend import views

urlpatterns = patterns('redirects.views',
    url(r'^$',
        views.index,
        name='index'),
    url(r'^(?P<slug>\w+)$',
        views.view_redirect,
        name='redirect'),
)