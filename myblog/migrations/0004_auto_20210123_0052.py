# Generated by Django 3.1.3 on 2021-01-22 23:52

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myblog', '0003_auto_20210123_0044'),
    ]

    operations = [
        migrations.AlterField(
            model_name='entry',
            name='visits_count',
            field=models.IntegerField(default=0, editable=False, validators=[django.core.validators.MinValueValidator(0)], verbose_name='visits count'),
        ),
    ]
