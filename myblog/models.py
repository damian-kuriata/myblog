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
    # Entry html code. Cannot be edited manually, it's populated
    # Programically
    html = models.TextField(editable=False, blank=True)
    image = models.ImageField(_("image"), upload_to=get_upload_path,
                              null=True, blank=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("myblog:entry", kwargs={"slug": self.slug})

    def get_in_text_url(self):
        print("get")
        try:
            return self.image.url + "/../in_text"
        except ValueError:
            # When Entry has no file associated with it,
            # just return empty string
            return ''

    def get_image_url(self):
        '''
            Use this function instead of Entry.image.url,
            Otherwise ValueError will be
            Raised if Entry has no image associated with it
        '''
        try:
            return self.image.url
        except ValueError:
            return ''

    def get_text_fragment(self):
        # Text fragment is a content of first paragraph tag
        # (text between <p> and </p>)
        paragraph_tag_part = "<p"
        paragraph_tag_part_index = self.html.find(paragraph_tag_part)
        if paragraph_tag_part_index == -1:
            return ''
        paragraph_tag_closing_index = self.html.find('>', paragraph_tag_part_index)
        if paragraph_tag_closing_index == -1:
            return ''
        paragraph_tag_end_index = self.html.find('</p>')
        from_ = paragraph_tag_closing_index + 1
        to = paragraph_tag_end_index
        text_fragment = self.html[from_:to]
        return text_fragment


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
