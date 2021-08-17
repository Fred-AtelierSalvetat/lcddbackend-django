from django.db.models.fields import EmailField
from rest_framework import serializers
from .models import RefLegifrance, Profession, Topic, Workshop, Keyword, UserProfile
from django.contrib.auth.models import User
from drf_extra_fields.fields import Base64ImageField
import uuid


class EditableBase64ImageField(Base64ImageField):
    class Meta:
        swagger_schema_fields = {
            'type': 'string',
            'title': 'File Content',
            'description': 'Content of the file base64 encoded',
            'read_only': False  # <-- FIX
        }


class TopicSerializer(serializers.ModelSerializer):
    thumbnail = Base64ImageField()

    class Meta:
        model = Topic
        fields = '__all__'


class RefLegifranceSerializer(serializers.ModelSerializer):
    class Meta:
        model = RefLegifrance
        fields = '__all__'


class KeywordSerializer(serializers.ModelSerializer):
    class Meta:
        model = Keyword
        fields = '__all__'


class WorkshopSerializer(serializers.ModelSerializer):

    keywords = KeywordSerializer(many=True, read_only=True)

    class Meta:
        model = Workshop
        fields = ('status', 'thumbnailUrl', 'videoUrl', 'title',
                  'startingdate', 'topics', 'description', 'refsLegifrance',
                  'keywords')
        depth = 1


class UserSerializer(serializers.ModelSerializer):
    lcdd_role = serializers.CharField(source="userprofile.lcdd_role")
    city = serializers.CharField(source="userprofile.city")
    interests = serializers.StringRelatedField(
        many=True, source="userprofile.interests")
    profession = serializers.CharField(source="userprofile.profession")
    phone = serializers.CharField(source="userprofile.phone")
    pro_email = serializers.EmailField(source="userprofile.pro_email")
    bio_title = serializers.CharField(source="userprofile.bio_title")
    biography = serializers.CharField(source="userprofile.biography")
    avatar = EditableBase64ImageField(source="userprofile.avatar")

    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'email', 'is_active', 'lcdd_role', 'city',
                  'interests', 'profession', 'phone', 'pro_email', 'bio_title', 'biography', 'avatar')

    def to_internal_value(self, data):
        validated_data = {
            'userprofile': {}
        }
        if data.get('first_name'):
            validated_data['first_name'] = data.get('first_name')
        if data.get('last_name'):
            validated_data['last_name'] = data.get('last_name')
        if data.get('email'):
            validated_data['email'] = data.get('email')
        if data.get('is_active'):
            validated_data['is_active'] = data.get('is_active')
        if data.get('city'):
            validated_data['userprofile']['city'] = data.get('city')
        lcdd_role = data.get('lcdd_role')
        if lcdd_role:
            choices = [choice[0] for choice in UserProfile.Roles.choices]
            if not lcdd_role in choices:
                raise serializers.ValidationError({
                    'lcdd_role': 'Authorized values are ' + ", ".join(choices)
                })
            validated_data['userprofile']['lcdd_role'] = lcdd_role
        interests = data.get('interests')
        if interests:
            if not isinstance(interests, list):
                raise serializers.ValidationError({
                    'interests': 'This field must be a list.'
                })
            if len(set(interests)) != len(interests):
                raise serializers.ValidationError({
                    'interests': 'Duplicated element not allowed.'
                })
            if not set(Topic.objects.all().values_list('title', flat=True)).issuperset(set(interests)):
                raise serializers.ValidationError({
                    'interests': "All values must be defined Topic's title"
                })
            validated_data['userprofile']['interests'] = interests

        profession = data.get('profession')
        if profession:
            if not isinstance(profession, str):
                raise serializers.ValidationError({
                    'profession': 'This field must be a string.'
                })
            if not profession in Profession.objects.all().values_list('label', flat=True):
                raise serializers.ValidationError({
                    'profession': "Must be a defined Profession's label"
                })
            validated_data['userprofile']['profession'] = profession

        if data.get('phone'):
            validated_data['userprofile']['phone'] = data.get('phone')
        if data.get('pro_email'):
            validated_data['userprofile']['pro_email'] = data.get('pro_email')
        if data.get('bio_title'):
            validated_data['userprofile']['bio_title'] = data.get('bio_title')
        if data.get('bio_title'):
            validated_data['userprofile']['biography'] = data.get('biography')
        if data.get('avatar'):
            validated_data['userprofile']['avatar'] = data.get('avatar')

        return validated_data

    def updateUserProfile(_, userprofile, userprofile_data):
        # WTF! I want ES6 destructuring
        lcdd_role = userprofile_data.get('lcdd_role')
        city = userprofile_data.get('city')
        interests = userprofile_data.get('interests')
        profession = userprofile_data.get('profession')
        phone = userprofile_data.get('phone')
        pro_email = userprofile_data.get('pro_email')
        bio_title = userprofile_data.get('bio_title')
        biography = userprofile_data.get('biography')
        avatar = userprofile_data.get('avatar')

        if lcdd_role:
            userprofile.lcdd_role = lcdd_role
        if city:
            userprofile.city = city
        if interests:
            userprofile.interests.set(
                [Topic.objects.get(title=interest) for interest in interests])
        if profession:
            userprofile.profession = Profession.objects.get(
                label=profession)
        if phone:
            userprofile.phone = phone
        if pro_email:
            userprofile.pro_email = pro_email
        if bio_title:
            userprofile.bio_title = bio_title
        if biography:
            userprofile.biography = biography
        if avatar:
            userprofile.avatar = avatar
        return userprofile

    def create(self, validated_data):
        userprofile_data = validated_data.pop('userprofile')
        validated_data['username'] = uuid.uuid4().hex
        # No user name in lcdd? Strange... Anyway as it's a quick dev, I stay with default model
        user = User.objects.create(**validated_data)
        if userprofile_data:
            self.updateUserProfile(user.userprofile, userprofile_data)
        return user

    def update(self, instance, validated_data):
        instance.first_name = validated_data.get(
            'first_name', instance.first_name)
        instance.last_name = validated_data.get(
            'last_name', instance.last_name)
        instance.email = validated_data.get(
            'email', instance.email)
        instance.is_active = validated_data.get(
            'is_active', instance.is_active)
        instance.save()

        if 'userprofile' in validated_data:
            userprofile = self.updateUserProfile(
                instance.userprofile, validated_data.pop('userprofile'))
            userprofile.save()

        # TODOFSA
        # Fix avatar upload
        # Add data type desc to Profession, Topics

        return instance


class ProfessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profession
        fields = '__all__'


# TODOFSA TODO Manage Image files upload through rest API ( avatar)
