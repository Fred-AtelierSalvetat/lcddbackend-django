from django.conf import settings
from rest_framework import serializers
from .models import Topic

from django.contrib.sites.models import Site



class TopicSerializer(serializers.ModelSerializer):
    thumbnail  = serializers.SerializerMethodField()

    class Meta:
        model = Topic
        fields = '__all__'

    def get_thumbnail(self, obj):
        current_site = Site.objects.get_current()
        return current_site.domain + settings.STATIC_URL + obj.thumbnail
