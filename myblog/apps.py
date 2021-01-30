import os

from django.apps import AppConfig
from django.db.models.signals import pre_save, post_save
from django.template import TemplateDoesNotExist
from django.template.loader import render_to_string

from myblog.signals import update_entry_category_visits_count


class MyblogConfig(AppConfig):
    name = 'myblog'

    def update_entries_html(self):
        from myblog.models import Entry
        from django.conf import settings

        # For each entry, update it's html attribute
        for entry in Entry.objects.all():
            # Not empty html attribute means that it was edited
            # Manually, so don't override it.
            if entry.html:
                continue
            template_name = entry.title.lower().strip() + ".html"
            template_path = os.path.join(settings.BASE_DIR.parent,
                                         self.name,
                                         "templates",
                                         self.name,
                                         "entries",
                                         template_name)
            try:
                with open(template_path) as template:
                    # Write template contents to Entry.html
                    entry.html = template.read()
            except FileNotFoundError:
                print(f"Error: template {template_path} not found.")
                entry.html = ''
            finally:
                entry.save()

    def register_signals(self):
        from myblog.models import Entry, Category
        from myblog.signals import populate_category_slug_field, \
            populate_entry_slug_field

        pre_save.connect(populate_category_slug_field, sender=Category)
        pre_save.connect(populate_entry_slug_field,
                         sender=Entry)
        post_save.connect(update_entry_category_visits_count, sender=Entry)

    def ready(self):
        self.update_entries_html()
        self.register_signals()