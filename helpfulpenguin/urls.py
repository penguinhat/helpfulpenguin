from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'helpfulpenguin.views.home', name='home'),
    # url(r'^helpfulpenguin/', include('helpfulpenguin.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^redirects/',include('redirects.urls')),

	# ! WARNING ! frontend.urls MUST be the last urlconf to be loaded
	# as it will match pretty much anything
    url(r'^',include('frontend.urls')),
)