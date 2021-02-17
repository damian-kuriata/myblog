from django.contrib.auth.models import User, Group
from rest_framework import serializers
from rest_framework.reverse import reverse

from myblog.models import Entry, Category, Comment



class UserSerializer(serializers.HyperlinkedModelSerializer):
    entry_set = serializers.HyperlinkedRelatedField(many=True, view_name="myblog:entry-detail", queryset=Entry.objects.all())
    url = serializers.HyperlinkedIdentityField("myblog:user-detail")

    class Meta:
        model = User
        fields = ['pk', 'url', 'username', 'email', 'entry_set']


class CategorySerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField("myblog:category-detail")
    entries = serializers.HyperlinkedRelatedField("myblog:category-detail", many=True, queryset=Entry.objects.all())

    class Meta:
        model = Category
        fields = ["pk", "url", "name", "slug", "total_visits_count", "entries"]


class EntrySerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField("myblog:entry-detail", read_only=True)
    category_set = serializers.HyperlinkedRelatedField(many=True, view_name="myblog:category-detail", queryset=Category.objects.all())
    author = serializers.HyperlinkedRelatedField("myblog:user-detail", queryset=User.objects.all())
    comment_set = serializers.PrimaryKeyRelatedField(many=True, queryset=Comment.objects.all())
    # Base64-encoded image
    image = serializers.CharField()

    class Meta:
        model = Entry
        fields = ["pk", "url", "title", "slug", "creation_datetime",
                 "visits_count", "html", "image", "category_set", "author", "comment_set"]


class CommentSerializer(serializers.HyperlinkedModelSerializer):
    entry = serializers.StringRelatedField()

    class Meta:
        model = Comment
        fields = ["pk", "author_email", "author_nickname", "text", "creation_datetime", "entry"]

