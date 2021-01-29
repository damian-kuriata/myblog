import json
import os

from django import views
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.db.models import Sum
from django.http import Http404, HttpResponse, JsonResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.template import TemplateDoesNotExist, Context
from django.urls import reverse
from django.views import View
from django.views.decorators.http import require_http_methods
from django.views.generic import ListView, DetailView, TemplateView
from django.core import serializers
from django.template import Engine
from django.conf import settings
import django.contrib.postgres

from myblog.forms import CommentForm
from myblog.models import Entry, Category, Comment


def _get_context_with_categories(context):
    context["categories"] = \
        Category.objects.all().order_by("-total_visits_count")
    for cat in Category.objects.all().order_by("-total_visits_count"):
        print(cat)
    return context


class IndexView(ListView):
    template_name = "myblog/index.html"
    model = Entry
    # Get 5 most popular entires
    queryset = Entry.objects.order_by("visits_count")[:5]
    context_object_name = "most_popular_entries"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Get 5 latest entries
        latest_entires = \
            Entry.objects.order_by("-creation_datetime")[:5]
        # To prevent the same entry from being both in latest and most popular,
        # Filter most popular and latest entries using filter function
        # self.queryset contains 5 most popular entries
        different_latest_entires = filter(lambda latest_entry:
                                            latest_entry not in self.queryset,
                                            latest_entires)
        # For now don't implement the above feature
        context["latest_entries"] = latest_entires
        context = _get_context_with_categories(context)
        return context



class CategoryView(View):
    template_name = "myblog/category.html"

    def get(self, request, *args, **kwargs):
        try:
            # Indicates by what sort returned entries in category
            entries_sort_by = request.GET.get("sort_by")
            slug = kwargs.get("slug").strip().lower()
            category = Category.objects.get(slug__iexact=slug)
            if entries_sort_by in ["title", "author__username",
                           "-creation_datetime", "-visits_count"]:
                entries = category.entries.order_by(entries_sort_by)

                print(entries)
            else:
                entries = category.entries.order_by("title")

            # Enable entries pagination
            ENTRIES_PER_PAGE = 10
            entries_paginator = Paginator(entries, ENTRIES_PER_PAGE)
            page_number = request.GET.get("page")
            page_obj = entries_paginator.get_page(page_number)
            context = {
                "category": category,
                "entries": entries,
                "page_obj": page_obj,
            }
            context = _get_context_with_categories(context)

            return render(request, self.template_name, context)
        except Category.DoesNotExist:
            return HttpResponse(status=404)


class SearchView(View):
    template_name = "myblog/search.html"

    def get(self, request, *args, **kwargs):
        search_query = request.GET.get("search", '')
        # Are we using Postgres?
        if settings.DATABASES["default"]["ENGINE"] \
            == "django.db.backends.postgresql_psycopg2":
            print("Using Postgre")
            categories = Category.objects.filter(name__search=
                                                 search_query)
            entries = Entry.objects.filter(title__search=
                                           search_query)
            users = User.objects.filter(username__search=
                                        search_query)
        else:
            categories = Category.objects.filter(
                name__icontains=search_query)
            entries = Entry.objects.filter(title__icontains=search_query)
            users = User.objects.filter(username__icontains=search_query)
        context = {
            "categories": categories,
            "entries": entries,
            "users": users
        }
        context["search_query"] = search_query
        #context = _get_context_with_categories(context)
        return render(request, self.template_name, context)


class UserView(View):
    def get(self, request, *args, **kwargs):
        return HttpResponseRedirect(reverse("myblog:aboutme"))

    '''
    model = User
    template_name = "myblog/user.html"
    slug_field = "username"
    context_object_name = "user"
    '''


class AboutmeView(TemplateView):
    template_name = "myblog/aboutme.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = _get_context_with_categories(context)
        return context


class EntryView(View):
    def get(self, request, *args, **kwargs):
        entry_slug = kwargs["slug"].lower()
        entry = get_object_or_404(Entry, slug__iexact=entry_slug)

        # Increment entry.visits_count each time this view is called
        entry.visits_count += 1
        entry.save()

        # Get comments written for a given entry
        comments = entry.comment_set.all()
        comment_form = CommentForm()

        context = {
            "entry": entry,
            "comments": comments,
            "comment_form": comment_form,
        }
        recently_key = "recently_visited_entries"
        context[recently_key] = list()

        # Process and save recently visited entries to request.session
        try:
            # request.session[recently_key] holds a list of recently
            # Visited entries' ids, e.g. [1, 2, 3]
            recently_visited_entries = request.session[recently_key]
            for id_ in recently_visited_entries:
                try:
                    context[recently_key].append(Entry.objects.get(id=id_))
                except Entry.DoesNotExist:
                    pass

            recently_visited_entries_limit = 5
            # Recently_visited_entries is a list where the first element
            # Holds the oldest entry id, and the last element holds the
            # Latest entry id
            if len(recently_visited_entries) >= recently_visited_entries_limit:
                # Remove the oldest entry id when a limit was exceeded
                del recently_visited_entries[0]
            # Prevent saving the same entry id one after another
            # (multiple times)
            if recently_visited_entries[-1] != entry.id:
                recently_visited_entries.append(entry.id)
            request.session[recently_key] = recently_visited_entries
        except KeyError:
            request.session[recently_key] = [entry.id]

        # Get suggested entries
        suggested_key = "suggested_entries"
        entry_categories = entry.category_set.all()
        if len(entry_categories) == 0:
            suggested_entries = Entry.objects.order_by("-creation_datetime",
                                                       "-visits_count")
            context[suggested_key] = suggested_entries

        elif len(entry_categories) == 1:
            entry_category = entry_categories.first()
            most_popular_entries_in_category = \
                entry_category.entries.order_by("-visits_count",
                                                "-creation_datetime",
                                                "-title")
            context[suggested_key] = most_popular_entries_in_category

        else:
            most_popular_entry_category = \
                entry_categories.order_by("-total_visits_count").first()
            most_popular_entries_in_category = \
                most_popular_entry_category.entries.order_by(
                    "-visits_count",
                    "-creation_datetime",
                    "-title")
            entries_limit = 5
            context[suggested_key] = \
                most_popular_entries_in_category.exclude(
                    id=entry.id)[:entries_limit]

        context = _get_context_with_categories(context)

        # Render HTML stored in entry.html as HttpResponse object
        rendered_html = Engine.get_default().from_string(template_code=entry.html).\
            render(Context(context))
        return HttpResponse(rendered_html)



# --- API ---
class AddCommentView(View):
    def post(self, request, *args, **kwargs):
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            entry_for_comment = Entry.objects.get(slug__iexact=kwargs["slug"])

            comment = Comment(**comment_form.cleaned_data)
            comment.entry = entry_for_comment
            comment.save()
            response = {
                "author_email": comment.author_email,
                "author_nickname": comment.author_nickname,
                "text": comment.text,
                "creation_datetime": comment.creation_datetime
            }
            return JsonResponse(response, status=201)
        else:
            # Serialize form errors to json
            errors = {"errors": comment_form.errors.as_json()}
            return JsonResponse(errors, status=400, safe=False)
