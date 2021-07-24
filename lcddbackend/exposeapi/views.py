from rest_framework import viewsets
from .serializers import TopicSerializer, RefLegifranceSerializer, WorkshopSerializer
from .models import RefLegifrance, Topic, Workshop


class TopicViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Topic.objects.all()
    serializer_class = TopicSerializer

class RefLegifranceViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = RefLegifrance.objects.all()
    serializer_class = RefLegifranceSerializer
    
class WorkshopViewSet(viewsets.ModelViewSet):
    queryset = Workshop.objects.all()
    serializer_class = WorkshopSerializer
    