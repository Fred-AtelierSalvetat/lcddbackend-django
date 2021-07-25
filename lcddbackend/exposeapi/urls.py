from django.urls import path,  include
from rest_framework import routers
from .views import TopicViewSet, RefLegifranceViewSet, UserProfileViewSet, WorkshopViewSet, ProfessionViewSet

 
# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'topics', TopicViewSet, basename='Topic')
router.register(r'refsLegifrance', RefLegifranceViewSet, basename='RefLegifrance')
router.register(r'workshops', WorkshopViewSet, basename='Workshop')
router.register(r'professions', ProfessionViewSet, basename='Profession')
router.register(r'users', UserProfileViewSet, basename='UserProfile')

urlpatterns =  [
    path('', include(router.urls)),
]