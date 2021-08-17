from django.conf import settings


def versioning(request):
    return {'API_VERSION': settings.API_VERSION}
