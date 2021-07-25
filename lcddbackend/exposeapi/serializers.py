from django.conf import settings
from django.contrib.sites.models import Site
from rest_framework import serializers
from .models import RefLegifrance, Profession, Topic, Workshop, Keyword, UserProfile
from django.contrib.auth.models import User, Group


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

class GroupSerializer(serializers.ModelSerializer):    
    class Meta:
        model = Group
        fields = ('id', 'name')
        depth= 1

class UserSerializer(serializers.ModelSerializer):
    groups = GroupSerializer(many=True)
    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'email', 'is_active', 'groups')
        depth = 1

class UserProfileSerializer(serializers.ModelSerializer):    
    user  = UserSerializer()
    class Meta:
        model = UserProfile
        fields = ('user', 'city', 'interests',)
        depth = 1

class ProfessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profession
        fields= '__all__'

# class SpeakerSerializer(serializers.ModelSerializer):
#     user = UserSerializer()
#     class Meta:
#         model= SpeakerProfile
#         fields = ('user', 'profession', 'phone', 'pro_email', 'biography')
#         depth = 1


# TODO
# POST, PUT workshop nested manytomany  + foreign
# Manage files
# Normalized API response??
