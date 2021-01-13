from django import views
from django.http import Http404
from django.shortcuts import render
from django.views.generic import ListView

from myblog.models import Entry, Category


class IndexView(ListView):
    template_name = "myblog/index.html"
    # Get most popular entires
    queryset = Entry.objects.order_by("visits_count")
    context_object_name = "most_popular_entries"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        latest_entires = \
            Entry.objects.order_by("-creation_datetime")
        context["latest_entries"] = latest_entires


class CategoriesView(ListView):
    template_name = "myblog/categories.html"

    def get_queryset(self):
        cat_name = self.kwargs.get("name")
        if cat_name:
            try:
                Category.objects.get(name=cat_name)
            except Category.DoesNotExist:
                raise Http404
        else:
            return Category.objects.all()