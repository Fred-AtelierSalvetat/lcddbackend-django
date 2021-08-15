from django.utils.decorators import method_decorator
from drf_yasg.utils import swagger_auto_schema
from drf_yasg.inspectors import CoreAPICompatInspector, FieldInspector, NotHandled, SwaggerAutoSchema
from django_filters import FilterSet, ChoiceFilter
from rest_framework import viewsets, mixins
from .serializers import (
    ProfessionSerializer,
    SpeakerProfileSerializers,
    TopicSerializer,
    RefLegifranceSerializer,
    UserProfileSerializer,
    WorkshopSerializer,
)
from .models import RefLegifrance, SpeakerProfile, Topic, Workshop, UserProfile, Profession
from django_filters.rest_framework import DjangoFilterBackend
from django_filters import FilterSet, MultipleChoiceFilter


class ListOnlyViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    pass


class TopicViewSet(ListOnlyViewSet):
    queryset = Topic.objects.all()
    serializer_class = TopicSerializer


class RefLegifranceViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = RefLegifrance.objects.all()
    serializer_class = RefLegifranceSerializer


class WorkshopViewSet(viewsets.ModelViewSet):
    queryset = Workshop.objects.all()
    serializer_class = WorkshopSerializer


class UserProfileFilter(FilterSet):
    lcdd_role = MultipleChoiceFilter(choices=UserProfile.Roles.choices)

    class Meta:
        model = UserProfile
        fields = ['lcdd_role']


class DjangoFilterDescriptionInspector(CoreAPICompatInspector):
    def get_filter_parameters(self, filter_backend):
        if isinstance(filter_backend, DjangoFilterBackend):
            result = super(DjangoFilterDescriptionInspector,
                           self).get_filter_parameters(filter_backend)
            for param in result:
                if not param.get('description', ''):
                    param.description = "Filter the returned list by {field_name}, multiple values are handles as OR : filter1 OR filter2".format(
                        field_name=param.name)
                    param.enum = [choice[0]
                                  for choice in UserProfile.Roles.choices]
            return result

        return NotHandled


@method_decorator(name='list', decorator=swagger_auto_schema(
    filter_inspectors=[DjangoFilterDescriptionInspector]
))
class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = UserProfileFilter

    def get_queryset(self):
        queryset = UserProfile.objects.all()
        role_params = self.request.query_params.getlist('lcdd_role')
        if role_params is not None:
            queryset = queryset.filter(
                lcdd_role__in=role_params)

        return queryset


class ProfessionViewSet(ListOnlyViewSet):
    queryset = Profession.objects.all()
    serializer_class = ProfessionSerializer


class SpeakerViewSet(ListOnlyViewSet):
    queryset = SpeakerProfile.objects.all()
    serializer_class = SpeakerProfileSerializers
