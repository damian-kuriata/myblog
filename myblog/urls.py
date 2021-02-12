from django.urls import path, re_path
from rest_framework import routers

from myblog import views
from myblog.views import IndexView, CategoryView, SearchView, UserView, EntryView, AboutmeView, AddCommentView
from myblog.api import Entries

app_name = "myblog"
urlpatterns = [
    path("", IndexView.as_view(), name="index"),
    path("category/<slug:slug>/",
            CategoryView.as_view(), name="category"),
    path("search/", SearchView.as_view(), name="search"),
    path("user/<slug:slug>/", UserView.as_view(), name="user"),
    path("entry/<slug:slug>/", EntryView.as_view(), name="entry"),
    path("aboutme/", AboutmeView.as_view(), name="aboutme"),
    # --- API ---
    path("entry/<slug:slug>/add-comment/", AddCommentView.as_view(),
         name="add_comment"),
    re_path(r"api/entries/((?P<pk>\d+))?", Entries.as_view(), name="entries"),
]