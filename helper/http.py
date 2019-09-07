from django.http import HttpResponse
from django.core import serializers

def json_response(data):
    """
    custom json response for models
    """
    return HttpResponse(
        serializers.serialize('json', data),
        content_type="application/json"
    )