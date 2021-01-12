from django.contrib.auth.models import User
from django.core.validators import MinLengthValidator
from django.db import models
from django.utils.translation import gettext_lazy as _



class Entry(models.Model):
    # Content isn't defined in this model as it's already defined
    # In it's template
    title = models.CharField(_("title"), max_length=60, unique=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                                verbose_name=_("author"))
    creation_datetime = models.DateTimeField(_("creation datetime"),
                                             auto_now=True)
    visits_count = models.IntegerField(_("visits count"), default=0,
                                       validators=[
                                           MinLengthValidator(0)
                                       ])

    def __str__(self):
        return self.title

    # TODO: Implement get absolute url

    class Meta:
        ordering = ["-creation_datetime"]
        verbose_name = _("entry")
        verbose_name_plural = _("entries")


class Category(models.Model):
    name = models.CharField(_("name"), max_length=60)
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
