import re

from django.contrib.auth.models import User
from django.core.validators import MinLengthValidator, MinValueValidator
from django.db import models
from django.db.models import Sum
from django.db.models.signals import pre_save, pre_delete
from django.dispatch import receiver
from django.urls import reverse_lazy, reverse
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _


def get_upload_path(instance, filename):
    return f"blog/{instance.title}/{filename}"

class Entry(models.Model):
    title = models.CharField(_("title"), max_length=60, unique=True)
    slug = models.SlugField(max_length=60, blank=True, editable=False,
                            help_text=_("Should not be edited manually, "
                                        "it is automatically"
                                        "updated when save() is called on Entry"
                                        ))
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                                verbose_name=_("author"))
    creation_datetime = models.DateTimeField(_("creation datetime"),
                                             auto_now_add=True)
    visits_count = models.IntegerField(_("visits count"),
                                       default=0,
                                       editable=False,
                                       validators=[
                                           MinValueValidator(0)
                                       ])
    # Entry html code. Can be edited manually, although it's not
    # Recommended. It's automatically populated each time an app starts.
    html = models.TextField(blank=True, help_text=_("Editing manually is not "
                                                    "recommended, as it's "
                                                    "automatically populated "
                                                    "when an app starts."))
    # Image acting as an entry 'thumbnail'
    image = models.ImageField(_("image"), upload_to=get_upload_path,
                              null=True, blank=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("myblog:entry", kwargs={"slug": self.slug})

    def get_in_text_url(self):
        """
        Returns an url pointing to 'in_text' directory containing
        All images that will be used in Entry HTML template
        """

        try:
            return self.image.url + "/../in_text"
        except ValueError:
            # When Entry has no file associated with it, just return
            # Empty string
            return ''

    def get_image_url(self):
        """
        This function should be used instead of Entry.image.url,
        Otherwise ValueError will be Raised if Entry has no image
        Associated with it
        """

        try:
            return self.image.url
        except ValueError:
            # Ignore ValueError, just return empty string
            return ''

    def get_text_fragment(self):
        """
        Returns contents of first <p> tag (if it exists). For example
        when tag <p>Test</p> is present, it returns 'Test'
        """
        regex = r"<p(.*?)>(?P<text>.*?)</p>"
        result = re.search(regex, self.html, flags=re.DOTALL)
        if result:
            return result.group("text")
        else:
            return ''

    class Meta:
        ordering = ["-creation_datetime"]
        verbose_name = _("entry")
        verbose_name_plural = _("entries")


class Category(models.Model):
    name = models.CharField(_("name"), max_length=60, unique=True)
    slug = models.SlugField(max_length=60, blank=True, editable=False,
                            help_text=_("Should not be edited manually, "
                                        "it is automatically"
                                        "updated when save() is called on "
                                        "Category"
                                        ))
    entries = models.ManyToManyField(Entry, verbose_name=_("entries"),
                                     blank=True)
    # Sum of visits of all entries belonging to this category cannot be
    # Manually edited. It is automatically updated on 'pre_save' signal
    total_visits_count = models.IntegerField(editable=False, default=0)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("myblog:category", kwargs={"slug": self.slug})

    def get_total_visits_count(self):
        """
        DEPRECATED! Use total_visits_count property instead
        Returns summarized visits counts from all entries
        """

        return self.entries.all().\
            aggregate(Sum("visits_count"))["visits_count__sum"]

    class Meta:
        ordering = ("name",)
        verbose_name = _("category")
        verbose_name_plural = _("categories")


class Comment(models.Model):
    author_email = models.EmailField(_("author email"))
    author_nickname = models.CharField(_("author nickname"),
                                       max_length=60,
                                       default="Anonymous",
                                       validators=[MinLengthValidator(5)]
                                       )
    text = models.TextField(_("text"), max_length=1000)
    creation_datetime = models.DateTimeField(_("creation_datetime"),
                                             auto_now_add=True)
    entry = models.ForeignKey(Entry, on_delete=models.CASCADE,
                              verbose_name=_("entry"))

    def __str__(self):
        return self.text

    class Meta:
        ordering = ["creation_datetime"]
        verbose_name = _("comment")
        verbose_name_plural = _("comments")
