from django.contrib import admin

# Register your models here.
from django.contrib.auth.models import Group

from myblog.models import Entry, Comment, Category


class MembershipInline(admin.TabularInline):
    model = Category.entries.through

@admin.register(Entry)
class EntryAdmin(admin.ModelAdmin):
    exclude = ("slug",)
    inlines = [
        MembershipInline
    ]
    date_hierarchy = "creation_datetime"

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    inlines = [
        MembershipInline
    ]
    exclude = ("members","slug")


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    date_hierarchy = "creation_datetime"