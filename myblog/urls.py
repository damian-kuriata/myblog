from django.urls import path
from django.views.generic import TemplateView

app_name = "myblog"

urlpatterns = [
    path("", IndexView.as_view(), name="index")
]