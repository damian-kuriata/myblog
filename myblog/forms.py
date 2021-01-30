from django.forms import ModelForm, Textarea
from django.utils.translation import gettext_lazy as _

from myblog.models import Comment


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ("author_email", "author_nickname", "text")
        widgets = {
            "text": Textarea()
        }
        labels = {
            "author_email": _("Your email"),
            "author_nickname": _("Your nickname")
        }

    class Media:
        css = {
            "all": ("myblog/css/comment-form.css",)
        }
        js = ("myblog/scripts/comment-form.js",)