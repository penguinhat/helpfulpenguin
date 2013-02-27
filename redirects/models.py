from django.db import models
import django.utils.timezone

from datetime import timedelta, datetime

from django.core.urlresolvers import reverse

ONE_HOUR = 2
HALF_DAY = 3
# ONE_DAY = 4
TWO_DAYS = 5
# THREE_DAYS = 6
# FIVE_DAYS = 7
ONE_WEEK = 8
# TWO_WEEKS = 9
# FOUR_WEEKS = 10


DURATION_CHOICES = (
    (ONE_HOUR,'Short Link for one hour'),
    (HALF_DAY,'Medium Link for 12 hours'),
    # (ONE_DAY,'One Day'),
    (TWO_DAYS,'Long Link for 2 days'),
    # (THREE_DAYS,'Three Days'),
    # (FIVE_DAYS,'Five Days'),
    (ONE_WEEK,'Very Long Link for One Week'),
    # (TWO_WEEKS,'Two Weeks'),
    # (FOUR_WEEKS,'Four Weeks'),
)

# timedelta for each duration
DURATION_DELTA = {
    ONE_HOUR:timedelta(hours=1),
    HALF_DAY:timedelta(hours=12),
    # ONE_DAY:timedelta(days=1),
    TWO_DAYS:timedelta(days=2),
    # THREE_DAYS:timedelta(days=3),
    # FIVE_DAYS:timedelta(days=5),
    ONE_WEEK:timedelta(days=7),
    # TWO_WEEKS:timedelta(days=14),
    # FOUR_WEEKS:timedelta(days=28),
}

# Default number of words to use in the slug
DURATION_WORD_COUNT = {
    ONE_HOUR:1,
    HALF_DAY:2,
    # ONE_DAY:3,
    TWO_DAYS:3,
    ONE_WEEK:4,
    # TWO_WEEKS:4,
    # FOUR_WEEKS:5,
}



class ArchivedRedirect(models.Model):
    """
    An archived redirect. This is a copy of a LiveRedirect that has expired.
    Is ReadOnly
    """

    created = models.DateTimeField(auto_now_add=True)
    url = models.URLField(blank=False,null=False,editable=False)
    slug = models.SlugField(blank=False,null=False,unique=False,editable=False)
    expiry = models.DateTimeField(null=True,blank=False,editable=False)

class LiveRedirect(models.Model):
    """
    A live redirect.
    """

    created = models.DateTimeField(auto_now_add=True)
    url = models.URLField(blank=False,null=False)

    # Actual slug used
    slug = models.SlugField(blank=False,null=False,unique=True,editable=False)

    # Comma seperated list of words used to generate the slug
    word_list = models.CharField(max_length=100,blank=False,null=False)

    expiry = models.DateTimeField(null=False,blank=False)
    duration = models.IntegerField(null=False,blank=False,choices=DURATION_CHOICES)

    def save(self,**kwargs):

        # If a new redirect
        if not self.pk:
            from redirects.utils import get_unused_slug

            self.full_clean(exclude=['slug','expiry','word_list'])

            self.slug, words = get_unused_slug(DURATION_WORD_COUNT[self.duration])
            self.word_list = ','.join(words)
            self.expiry = django.utils.timezone.now() + DURATION_DELTA[self.duration]

            self.full_clean()

            archive_kwargs = {
                'url':self.url,
                'slug':self.slug,
                'expiry':self.expiry,
            }

            archive = ArchivedRedirect(**archive_kwargs)
            archive.save()

        super(LiveRedirect,self).save(**kwargs)

    @property
    def words(self):
        return self.word_list.split(',')

    def __unicode__(self):
        return u'LiveRedirect %s -> %s Expires %s' % (self.slug,self.url,self.expiry)

    def get_absolute_url(self):
        return reverse('frontend_redirect',kwargs={'slug':self.slug})
