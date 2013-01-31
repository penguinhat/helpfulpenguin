from django.forms import widgets
from rest_framework import serializers
from redirects.models import LiveRedirect

class LiveRedirectSerializer(serializers.Serializer):
    pk = serializers.Field()  # Note: `Field` is an untyped read-only field.

    url = serializers.URLField()

    slug = serializers.Field()
    word_list = serializers.Field()

    duration = serializers.ChoiceField()

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