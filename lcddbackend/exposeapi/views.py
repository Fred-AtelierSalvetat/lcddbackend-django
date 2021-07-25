from django.db.models import query
from rest_framework import viewsets
from .serializers import ProfessionSerializer, TopicSerializer, RefLegifranceSerializer, UserProfileSerializer, WorkshopSerializer
from .models import RefLegifrance, Topic, Workshop, UserProfile, Profession

class TopicViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Topic.objects.all()
    serializer_class = TopicSerializer

class RefLegifranceViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = RefLegifrance.objects.all()
    serializer_class = RefLegifranceSerializer
    
class WorkshopViewSet(viewsets.ModelViewSet):
    queryset = Workshop.objects.all()
    serializer_class = WorkshopSerializer

class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    
class ProfessionViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Profession.objects.all()
    serializer_class = ProfessionSerializer
