from django.contrib.auth.models import User
from django.core.validators import MinLengthValidator, MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _


def get_upload_path(instance, filename):
    return f"blog/{instance.title}/{filename}"


class Entry(models.Model):
    # Each time new entry is created in templates,
    # corresponding Entry object must be created as well
    title = models.CharField(_("title"), max_length=60, unique=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                                verbose_name=_("author"))
    creation_datetime = models.DateTimeField(_("creation datetime"),
                                             auto_now=True)
    visits_count = models.IntegerField(_("visits count"), default=0,
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

    # TODO: Implement get absolute url

    class Meta:
        ordering = ["-creation_datetime"]
        verbose_name = _("entry")
        verbose_name_plural = _("entries")


class Category(models.Model):
    name = models.CharField(_("name"), max_length=60, unique=True)
    entries = models.ManyToManyField(Entry, verbose_name=_("entries"))

    def __str__(self):
        return self.name
    # TODO: Implement get absolute url

    class Meta:
        ordering = ["name"]
        verbose_name = _("category")
        verbose_name_plural = _("categories")


class Comment(models.Model):
    author_email = models.EmailField(_("author email"))
    author_nickname = models.CharField(_("author nickname"),
                                       max_length=60,
                                       default="Anonymous",
                                       blank=True)
    text = models.TextField(_("text"), max_length=1000)
    creation_datetime = models.DateTimeField(_("creation_datetime"),
                                             auto_now_add=True)
    entry = models.ForeignKey(Entry, on_delete=models.CASCADE,
                              verbose_name=_("entry"))

    def __str__(self):
        return self.text

    class Meta:
        ordering = ["-creation_datetime"]
        verbose_name = _("comment")
        verbose_name_plural = _("comments")
