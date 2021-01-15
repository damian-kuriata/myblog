from django.urls import path, re_path
from django.views.generic import TemplateView

from myblog.views import IndexView, CategoryView, SearchView

app_name = "myblog"

urlpatterns = [
    path("", IndexView.as_view(), name="index"),
    path("category/<name>/",
            CategoryView.as_view(), name="category"),
    path("search/", SearchView.as_view(), name="search")
]