from django.db import models
import django.utils.timezone

from datetime import timedelta, datetime

from django.core.urlresolvers import reverse

HALF_DAY = 3
ONE_DAY = 4
TWO_DAYS = 5
THREE_DAYS = 6
FIVE_DAYS = 7
ONE_WEEK = 8
TWO_WEEKS = 9
FOUR_WEEKS = 10


DURATION_CHOICES = (
    (HALF_DAY,'12 Hours'),
    (ONE_DAY,'One Day'),
    (TWO_DAYS,'Two Days'),
    (THREE_DAYS,'Three Days'),
    (FIVE_DAYS,'Five Days'),
    (ONE_WEEK,'One Week'),
    (TWO_WEEKS,'Two Weeks'),
    (FOUR_WEEKS,'Four Weeks'),
)

# timedelta for each duration
DURATION_DELTA = {
    HALF_DAY:timedelta(hours=12),
    ONE_DAY:timedelta(days=1),
    TWO_DAYS:timedelta(days=2),
    THREE_DAYS:timedelta(days=3),
    FIVE_DAYS:timedelta(days=5),
    ONE_WEEK:timedelta(days=7),
    TWO_WEEKS:timedelta(days=14),
    FOUR_WEEKS:timedelta(days=28),
}

# Default number of words to use in the slug
DURATION_WORD_COUNT = {
    HALF_DAY:1,
    ONE_DAY:1,
    TWO_DAYS:2,
    THREE_DAYS:2,
    FIVE_DAYS:3,
    ONE_WEEK:3,
    TWO_WEEKS:4,
    FOUR_WEEKS:5,
}



class ArchivedRedirect(models.Model):
    """
    An archived redirect. This is a copy of a LiveRedirect that has expired.
    Is ReadOnly
    """

    created = models.DateTimeField(auto_now_add=True)
    url = models.URLField(blank=False,null=False)
    slug = models.SlugField(blank=False,null=False,unique=False)
    expiry = models.DateTimeField(null=True,blank=False)

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

    def archive(self):
        """
        Creates an ArchivedRedirect and then deletes self.
        """

        kwargs = {
            'url':self.url,
            'slug':self.slug,
            'expiry':self.expiry,
        }

        archive = ArchivedRedirect(**kwargs)

        archive.save()

        self.delete()

    def save(self,**kwargs):

        # If a new redirect
        if not self.pk:
            from redirects.utils import get_unused_slug

            self.full_clean(exclude=['slug','expiry','word_list'])

            self.slug, words = get_unused_slug(DURATION_WORD_COUNT[self.duration])
            self.word_list = ','.join(words)
            self.expiry = django.utils.timezone.now() + DURATION_DELTA[self.duration]

            self.full_clean()

        super(LiveRedirect,self).save(**kwargs)

    @property
    def words(self):
        return self.word_list.split(',')

    def __unicode__(self):
        return u'LiveRedirect %s -> %s Expires %s' % (self.slug,self.url,self.expiry)

    def get_absolute_url(self):
        return reverse('live_redirect',kwargs={'slug':self.slug})
