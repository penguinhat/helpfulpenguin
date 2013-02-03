from django.forms import widgets
from rest_framework import serializers
from redirects.models import LiveRedirect

class LiveRedirectSerializer(serializers.ModelSerializer):

    class Meta:
        model = LiveRedirect
        exclude = ('id',)
        read_only_fields = ('slug','word_list','expiry')

    def restore_object(self, attrs, instance=None):
        """
        Create or update a new snippet instance.
        """
        if instance:
            # Update existing instance (Should you be able to do this?)
            instance.url = attrs.get('url', instance.url)
            instance.duration = attrs.get('duration', instance.duration)
            return instance

        # Create new instance
        return LiveRedirect(**attrs)