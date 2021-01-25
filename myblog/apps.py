import os

from django.apps import AppConfig
from django.template.loader import render_to_string


class MyblogConfig(AppConfig):
    name = 'myblog'

    def _update_entries_html(self):
        from myblog.models import Entry
        from django.conf import settings

        # For each entry, update it's html attribute
        for entry in Entry.objects.all():
            template_name = entry.slug + ".html"
            partial_path = os.path.join(self.name, "entries", template_name)
            entry.html = render_to_string(partial_path)
            entry.save()

    def ready(self):
        self._update_entries_html()