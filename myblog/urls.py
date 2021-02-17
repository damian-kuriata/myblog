from django.contrib.auth.models import User
from django.urls import path, re_path, include
from rest_framework import routers, serializers, viewsets
from rest_framework.urlpatterns import format_suffix_patterns

from myblog import views
from myblog.views import IndexView, CategoryView, SearchView, UserView, EntryView, AboutmeView, AddCommentView, \
     UserViewSet, UserDetail, UserList, CategoryList, CategoryDetail, EntryDetail, EntryList, api_root, \
    CommentList, CommentDetail
from myblog.api import Entries

app_name = "myblog"
router = routers.DefaultRouter()
router.register(r"users", UserViewSet)

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
    #re_path(r"api/entries/((?P<pk>\d+))?", Entries.as_view(), name="entries"),
    #path('', include((router.urls, "myblog"))),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('api/categories/', CategoryList.as_view(), name="category-list"),
    path('api/categories/<int:pk>/', CategoryDetail.as_view(), name='category-detail'),
    path('api/users/', UserList.as_view(), name="user-list"),
    path('api/users/<int:pk>/', UserDetail.as_view(), name="user-detail"),
    path('api/entries/', EntryList.as_view(), name="entry-list"),
    path('api/entries/<int:pk>/', EntryDetail.as_view(), name="entry-detail"),
    path('api/comments/', CommentList.as_view(), name="comment-list"),
    path("api/comments/<int:pk>/", CommentDetail.as_view(), name="comment-detail"),
    path('api/', api_root, name="api-root")
]
