# Generated by Django 3.1.3 on 2021-01-25 16:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myblog', '0007_auto_20210124_0101'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='entry',
            name='text_fragment',
        ),
        migrations.AddField(
            model_name='entry',
            name='html',
            field=models.TextField(blank=True, editable=False),
        ),
    ]