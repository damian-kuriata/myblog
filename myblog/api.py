import base64
import binascii

from django.contrib.auth.models import User
from django.core import serializers
from django.http import HttpResponse, JsonResponse
from django.views import View

from myblog.models import Entry


def authentication_required(view_class_method):
    def wrapper(self, request, *args, **kwargs):
        try:
            authorization = request.headers["Authorization"]
            auth_type, credentials = authorization.split()[:2]
            credentials = credentials.encode("utf-8")
            if auth_type != "Basic":
                response = JsonResponse({"error:" "Authentication must be basic!"}, status=401)
                header = 'Basic "Access to write API", charset="utf-8"'
                response["WWW-Authenticate"] = header
                return response
            try:
                decoded_credentials = base64.b64decode(credentials).\
                    decode("utf-8")
                username, password = decoded_credentials.split(":")[:2]
                user = User.objects.filter(username=username).first()
                if user and user.check_password(password):
                    return view_class_method(self, request, *args, **kwargs)
                else:
                    response = JsonResponse({"error:" "Forbidden"}, status=403)
                    return response

            except binascii.Error as err:
                response = JsonResponse({"error": str(err)}, status=401, safe=False)
                header = 'Basic "Access to write API", charset="utf-8"'
                response["WWW-Authenticate"] = header
                return response
        except KeyError:
            response = JsonResponse({"error": "Unauthorized"}, status=401)
            header = 'Basic "Access to write API", charset="utf-8"'
            response["WWW-Authenticate"] = header
            return response
    return wrapper


class Entries(View):
    def get(self, request, *args, **kwargs):
        entry_pk = kwargs.get("pk")
        if not entry_pk:
            return JsonResponse(serializers.serialize("json",
                                                      Entry.objects.all()), safe=False)
        else:
            entry = Entry.objects.filter(pk=entry_pk).first()
            if not entry:
                reason = f"Entry {entry_pk} not found"
                return JsonResponse({"error": reason}, status=404)
            return JsonResponse(serializers.serialize("json", [entry]), safe=False)

