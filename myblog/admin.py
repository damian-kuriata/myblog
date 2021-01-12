from django.contrib import admin

# Register your models here.
from myblog.models import TestModel

admin.site.register(TestModel)