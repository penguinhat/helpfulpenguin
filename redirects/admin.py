from redirects.models import LiveRedirect, ArchivedRedirect
from django.contrib import admin

admin.site.register(LiveRedirect)

admin.site.register(ArchivedRedirect)