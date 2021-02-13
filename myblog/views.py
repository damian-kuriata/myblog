import os

from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.template import RequestContext
from django.urls import reverse
from django.utils.dateparse import parse_datetime
from django.views import View
from django.views.generic import ListView, TemplateView
from django.template import Engine
from django.conf import settings

from myblog.forms import CommentForm
from myblog.models import Entry, Category, Comment


def _get_context_with_categories(context):
    """ Adds QuerySet of categories ordered by -total_visits_count to
    Context. Should be called in each view that isn't an API.
    """

    context["categories"] = \
        Category.objects.all().order_by("-total_visits_count")
    return context


class IndexView(View):
    template_name = "myblog/index.html"

    def get(self, request, *args, **kwargs):
        context = {}
        page_number = request.GET.get("page", '')
        if page_number == '':
            page_number = '1'
        all_entries = Entry.objects.all()
        # Get 5 most popular entries.
        most_popular_entries = all_entries.order_by("visits_count")[:5]
        most_popular_entries_ids = most_popular_entries.values_list("id")
        # Get 5 latest entries, order by -creation_datetime as defined
        # In Entry.Meta class.
        latest_entries = Entry.objects.all()[:5]
        latest_entries_ids = latest_entries.values_list("id")
        # Other entries are entries that DO NOT belong to most popular
        # And latest entries, order by -creation_datetime as defined in
        # Entry.Meta class
        other_entries = \
            all_entries.exclude(Q(id__in=most_popular_entries_ids)
                              | Q(id__in=latest_entries_ids))
        if page_number == '1':
            context["most_popular_entries"] = most_popular_entries
            context["latest_entries"] = latest_entries

        # TODO: Change to 10
        entries_per_page = 1
        paginator = Paginator(other_entries, entries_per_page)
        page_obj = paginator.get_page(page_number)
        context["page_obj"] = page_obj
        context = _get_context_with_categories(context)

        return render(request, self.template_name, context)

class CategoryView(View):
    template_name = "myblog/category.html"

    def get(self, request, *args, **kwargs):
        try:
            # Indicates by what sort returned entries in category.
            entries_sort_by = request.GET.get("sort_by")
            slug = kwargs.get("slug")
            category = Category.objects.get(slug__iexact=slug)
            if entries_sort_by in ["title", "author__username",
                           "-creation_datetime", "-visits_count"]:
                entries = category.entries.order_by(entries_sort_by)
            else:
                # Sort by title if sorting option is not present or invalid.
                entries = category.entries.order_by("title")

            # Enable entries pagination
            entries_per_page = 10
            entries_paginator = Paginator(entries, entries_per_page)
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
        return render(request, self.template_name, context)


class UserView(View):
    """ Temporarily rediects to aboutme page. """

    def get(self, request, *args, **kwargs):
        return HttpResponseRedirect(reverse("myblog:aboutme"))


class AboutmeView(TemplateView):
    template_name = "myblog/aboutme.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = _get_context_with_categories(context)
        return context


class EntryView(View):
    def get(self, request, *args, **kwargs):
        entry_slug = kwargs["slug"]
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
        entry_categories_len = len(entry_categories)
        # When entry has no categories (rare case)
        if entry_categories_len == 0:
            suggested_entries = Entry.objects.order_by("-creation_datetime",
                                                       "-visits_count")
            context[suggested_key] = suggested_entries

        # When entry is in 1 category (the most frequent case)
        elif entry_categories_len == 1:
            entry_category = entry_categories.first()
            most_popular_entries_in_category = \
                entry_category.entries.order_by("-visits_count",
                                                "-creation_datetime",
                                                "-title")
            context[suggested_key] = most_popular_entries_in_category

        # When entry is in multiple categories
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

        if settings.DEBUG:
            # When debug is enabled, update entry HTML each time new
            # Request is made
            template_name = entry.slug.lower().strip() + ".html"
            template_path = os.path.join(settings.BASE_DIR.parent,
                                         "myblog",
                                         "templates",
                                         "myblog",
                                         "entries",
                                         template_name)
            try:
                with open(template_path, encoding="utf-8") as template:
                    # Write template contents to Entry.html
                    entry.html = template.read()
            except FileNotFoundError:
                print(f"Error: template {template_path} not found.")
                entry.html = ''
            finally:
                entry.save()

        # Render HTML stored in entry.html as HttpResponse object
        rendered_html = Engine.get_default().from_string(template_code=entry.html).\
            render(RequestContext(request, context))
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
