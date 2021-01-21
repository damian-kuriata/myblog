from django.urls import path, re_path
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView

from myblog.views import IndexView, CategoryView, SearchView, UserView, EntryView, AboutmeView, AddCommentView

app_name = "myblog"

urlpatterns = [
    path("", IndexView.as_view(), name="index"),
    path("category/<slug:slug>/",
            CategoryView.as_view(), name="category"),
    path("search/", SearchView.as_view(), name="search"),
    path("user/<slug:slug>/", UserView.as_view(), name="user"),
    path("entry/<slug:slug>/", EntryView.as_view(), name="entry"),
    path("entry/<slug:slug>/add-comment/", AddCommentView.as_view(), name="add_comment"),
    path("aboutme/", AboutmeView.as_view(), name="aboutme"),
]