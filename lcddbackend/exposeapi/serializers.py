from django.conf import settings
from django.contrib.sites.models import Site
from rest_framework import serializers
from .models import RefLegifrance, Topic, Workshop, Keyword



class TopicSerializer(serializers.ModelSerializer):
    thumbnail  = serializers.SerializerMethodField()

    class Meta:
        model = Topic
        fields = '__all__'

    def get_thumbnail(self, obj):
        current_site = Site.objects.get_current()
        return current_site.domain + settings.STATIC_URL + obj.thumbnail


class RefLegifranceSerializer(serializers.ModelSerializer):
    class Meta:
        model = RefLegifrance
        fields = '__all__'

class KeywordSerializer(serializers.ModelSerializer):
    class Meta:
        model = Keyword
        fields = '__all__'

class WorkshopSerializer(serializers.ModelSerializer):

    keywords = KeywordSerializer( many= True, read_only=True)
    class Meta:
        model = Workshop
        fields = ('status', 'thumbnailUrl','videoUrl','title','startingdate' ,'topics', 'description', 'refsLegifrance', 'keywords' )
        depth = 1


# TODO
# POST, PUT workshop nested manytomany  + foreign
# Manage speakers
# Manage files

