from django.core.management.base import NoArgsCommand
import django.utils.timezone

from redirects.models import LiveRedirect

class Command(NoArgsCommand):

    def handle_noargs(self,*args,**kwargs):
        now = django.utils.timezone.now()
        queryset = LiveRedirect.objects.filter(expiry__lte=now)
        if queryset.exists():
            count = queryset.count()
            queryset.delete()
            self.stdout.write('Purged %s out of date LiveRedirects!\n' % count)