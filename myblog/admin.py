from django.contrib import admin

# Register your models here.
from django.contrib.auth.models import Group

from myblog.models import Entry, Comment, Category


class CategoryMembershipInline(admin.TabularInline):
    model = Category.entries.through
    max_num = 2


class CommentMembershipInline(admin.TabularInline):
    model = Comment
    max_num = 2


@admin.register(Entry)
class EntryAdmin(admin.ModelAdmin):
    exclude = ("slug",)
    inlines = [
        CategoryMembershipInline, CommentMembershipInline
    ]
    date_hierarchy = "creation_datetime"

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    inlines = [
        CategoryMembershipInline
    ]
    exclude = ("members", "slug")


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    date_hierarchy = "creation_datetime"