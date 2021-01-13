from django.urls import path, re_path
from django.views.generic import TemplateView

from myblog.views import IndexView, CategoriesView

app_name = "myblog"

urlpatterns = [
    path("", IndexView.as_view(), name="index"),
    re_path(r"^categories/((?P<name>\w+)/)?$",
            CategoriesView.as_view(),
            name="aboutme")
]