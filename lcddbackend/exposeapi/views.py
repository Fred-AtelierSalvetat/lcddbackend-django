from django.utils.decorators import method_decorator
from django_filters.utils import label_for_filter
from drf_yasg.utils import swagger_auto_schema
from drf_yasg.inspectors import CoreAPICompatInspector, FieldInspector, NotHandled, SwaggerAutoSchema
from django_filters import FilterSet, ChoiceFilter
from rest_framework import viewsets, mixins
from .serializers import (
    ProfessionSerializer,
    UserSerializer,
    TopicSerializer,
    RefLegifranceSerializer,
    WorkshopSerializer,
)
from .models import RefLegifrance, Topic, Workshop, Profession, User, UserProfile
from django_filters.rest_framework import DjangoFilterBackend
from django_filters import FilterSet, MultipleChoiceFilter, BooleanFilter


class ListOnlyViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    pass


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


class UserFilter(FilterSet):

    def __init__(self, data=None, *args, **kwargs):
        if data is not None:
            data = data.copy()
            data.setdefault("is_active", True)
        super(UserFilter, self).__init__(data, *args, **kwargs)

    lcdd_role = MultipleChoiceFilter(field_name="userprofile__lcdd_role",
                                     choices=UserProfile.Roles.choices)
    is_active = BooleanFilter(field_name='is_active')

    class Meta:
        model = User
        fields = ['is_active', 'lcdd_role']


class DjangoFilterDescriptionInspector(CoreAPICompatInspector):
    def get_filter_parameters(self, filter_backend):
        if isinstance(filter_backend, DjangoFilterBackend):
            result = super(DjangoFilterDescriptionInspector,
                           self).get_filter_parameters(filter_backend)
            for param in result:
                if not param.get('description', ''):
                    if param.name == 'lcdd_role':
                        param.description = "Filter the returned list by {field_name}.\nMultiple values are handles as OR :\n<pre>    lcdd_role=CITIZEN&lcdd_role=ADMIN => lcdd_role = CITIZEN OR ADMIN </pre>".format(
                            field_name=param.name)
                        param.enum = [choice[0]
                                      for choice in UserProfile.Roles.choices]
                    elif param.name == "is_active":
                        param.description = 'default value : True'
                        param.enum = ["All", "True", "False"]
                        pass
            return result

        return NotHandled


@method_decorator(name='list', decorator=swagger_auto_schema(
    filter_inspectors=[DjangoFilterDescriptionInspector]
))
class UserViewSet(mixins.ListModelMixin, mixins.CreateModelMixin, mixins.RetrieveModelMixin, mixins.UpdateModelMixin, viewsets.GenericViewSet):
    http_method_names = ['get', 'post', 'head', 'patch']
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = UserFilter


class ProfessionViewSet(ListOnlyViewSet):
    queryset = Profession.objects.all()
    serializer_class = ProfessionSerializer
