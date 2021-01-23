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
    # Each time new entry is created in templates,
    # corresponding Entry object must be created as well
    title = models.CharField(_("title"), max_length=60,
                             unique=True)
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
    # Field containing first 100 letters of a corresponding article
    text_fragment = models.CharField(_("text fragment"), max_length=100,
                                     null=True)
    image = models.ImageField(_("image"), upload_to=get_upload_path,
                              null=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("myblog:entry", kwargs={"slug": self.slug})

    def get_in_text_url(self):
        return self.image.url + "/../in_text"

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
    # Sum of visits of all entries belonging to this category
    # Cannot be manually edited. It is automatically updated on
    # Pre_save signal (code below)
    total_visits_count = models.IntegerField(editable=False, default=0)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("myblog:category", kwargs={"slug": self.slug})

    def get_total_visits_count(self):
        '''
        DEPRECATED!
        Return summarized visits counts from all entries
        '''

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


# --- SIGNALS ---
@receiver(pre_save)
def entry_and_category_pre_save(sender, instance, **kwargs):
    '''
        Callback for pre_save signal
    '''
    if sender == Entry:
        instance.slug = slugify(instance.title)
        try:
            # Update total_visits_count field for each category
            for category in instance.category_set.all():
                category.total_visits_count += instance.visits_count
                category.save()
        except ValueError:
            # When Entry object is saved for the very first time,
            # it doesn't have an id.
            # So Value Error is raised by Django.
            # Just ignore it and don't update field
            pass
    elif sender == Category:
        instance.slug = slugify(instance.name)
