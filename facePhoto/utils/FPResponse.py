import json
from django.http import HttpResponse
from django.core.serializers.json import DjangoJSONEncoder


class FPResponse:
    @classmethod
    def success(cls, data):
        return HttpResponse(json.dumps({"success": True, "data": data}, sort_keys=True, cls=DjangoJSONEncoder))

    @classmethod
    def failure(cls, message):
        return HttpResponse(json.dumps({"success": False, "message": message}, sort_keys=True, cls=DjangoJSONEncoder))
