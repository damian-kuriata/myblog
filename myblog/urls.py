from django.urls import path, re_path
from django.views.generic import TemplateView

from myblog.views import IndexView, CategoryView, SearchView, UserView, EntryView, AboutmeView, AddCommentView

app_name = "myblog"

urlpatterns = [
    path("", IndexView.as_view(), name="index"),
    path("category/<name>/",
            CategoryView.as_view(), name="category"),
    path("search/", SearchView.as_view(), name="search"),
    re_path(r"^user/(?P<slug>\w+)/$(?i)", UserView.as_view(), name="user"),
    re_path(r"^entry/(?P<slug>.+)/$(?i)", EntryView.as_view(), name="entry"),
    re_path(r"^entry/(?P<slug>.+)/add_comment/$(?i)", AddCommentView.as_view(),
            name="add_comment"),
    path("aboutme/", AboutmeView.as_view(), name="aboutme"),
]