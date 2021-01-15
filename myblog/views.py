from django import views
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.db.models import Sum
from django.http import Http404, HttpResponse
from django.shortcuts import render, get_object_or_404
from django.views import View
from django.views.generic import ListView, DetailView

from myblog.models import Entry, Category

def _get_context_with_categories(context):
    ''' Returns context with appended, ordered categories'''
    # TODO: Implement category ordering
    context["categories"] = Category.objects.all()
    return context


class IndexView(ListView):
    template_name = "myblog/index.html"
    model = Entry
    # Get 5 most popular entires
    queryset = Entry.objects.order_by("visits_count")[:5]
    context_object_name = "most_popular_entries"

    def get_context_data(self, **kwargs):
        import sys
        print(sys.path)
        context = super().get_context_data(**kwargs)
        latest_entires = \
            Entry.objects.order_by("-creation_datetime")[:5]
        context["latest_entries"] = latest_entires
        context = _get_context_with_categories(context)
        return context



class CategoryView(View):
    template_name = "myblog/category.html"

    def get(self, request, *args, **kwargs):
        try:
            # Indicates by what sort returned entries in category
            entries_sort_by = request.GET.get("sort_by")
            name = kwargs.get("name")
            category = Category.objects.get(name__iexact=name)
            if entries_sort_by in ["title", "author__username",
                           "creation_datetime", "visits_count"]:
                entries = category.entries.order_by(entries_sort_by)
            else:
                entries = category.entries.order_by("title")

            # Enable entries pagination
            ENTRIES_PER_PAGE = 1
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
        # Allowed search filters are: all, categories, entries, users
        #search_filter = request.GET.get("search")
        search_query = request.GET.get("search", '')
        categories = Category.objects.filter(
            name__icontains=search_query)
        entries = Entry.objects.filter(title__icontains=search_query)
        users = User.objects.filter(username__icontains=search_query)
        '''
        if search_filter == "categories":
            context = {
                "categories": categories
            }
        elif search_filter == "entries":
            context = {
                "entries": entries
            }
        elif search_filter == "users":
            context = {
                "users": users
            }
        # If search filter is unknown or set to 'all' treat it as 'all'
        else:
            context = {
                "categories": categories,
                "entries": entries,
                "users": users
            }
        '''
        context = {
            "categories": categories,
            "entries": entries,
            "users": users
        }
        context["search_query"] = search_query
        return render(request, self.template_name, context)


class UserView(DetailView):
    model = User
    template_name = "myblog/user.html"
    slug_field = "username"
    context_object_name = "user"


class EntryView(DetailView):
    model = Entry
    template_name = "myblog/entry.html"
    slug_field = "title"
    context_object_name = "entry"
