from django.utils.decorators import method_decorator
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from drf_yasg.inspectors import CoreAPICompatInspector, FieldInspector, NotHandled
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


class DjangoFieldsInspector(FieldInspector):
    def process_result(self, result, method_name, obj, **kwargs):
        if isinstance(result, openapi.Schema.OR_REF):
            # traverse any references and alter the Schema object in place
            schema = openapi.resolve_ref(result, self.components)
            title = schema.get('title', None)
            type = schema.get('type', None)
            if title == 'Lcdd role':
                schema.__setattr__(
                    'enum', [choice[0] for choice in UserProfile.Roles.choices])
            elif title == 'Profession':
                schema.__setattr__(
                    'description', "An already defined Profession's label")
            elif title == 'File Content':
                schema.pop('description')
            elif type == 'array':  # Duno why this filed doesn't have title...
                schema.__setattr__(
                    'description', "A array of already defined Topic's title")
            # ex : scheme = Schema([('title', 'First name'), ('type', 'string'), ('maxLength', 150)])

            # no ``return schema`` here, because it would mean we always generate
            # an inline `object` instead of a definition reference

        # return back the same object that we got - i.e. a reference if we got a reference
        return result


@ method_decorator(name='list', decorator=swagger_auto_schema(
    filter_inspectors=[DjangoFilterDescriptionInspector],
    field_inspectors=[DjangoFieldsInspector]
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
