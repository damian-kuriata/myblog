# Generated by Django 3.1.3 on 2021-01-29 01:10

from django.db import migrations, models
import myblog.models


class Migration(migrations.Migration):

    dependencies = [
        ('myblog', '0002_auto_20210127_2252'),
    ]

    operations = [
        migrations.AlterField(
            model_name='entry',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to=myblog.models.get_upload_path, verbose_name='image'),
        ),
    ]
