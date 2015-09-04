from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from gatekeeper.models import Badges
from gatekeeper.serializers import BadgeSerializer

# Create your views here.

class JSONResponse(HttpResponse):
    """
    An HttpResponse that renders its content into JSON.
    """
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)


def badges_list(request):
    """
    List all code snippets, or create a new snippet.
    """
    if request.method == 'GET':
        badges = Badges.objects.all()
        serializer = BadgeSerializer(badges, many=True)
        return JSONResponse(serializer.data)

