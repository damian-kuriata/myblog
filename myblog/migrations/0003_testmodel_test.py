# Generated by Django 3.1.3 on 2021-01-12 01:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myblog', '0002_remove_testmodel_test'),
    ]

    operations = [
        migrations.AddField(
            model_name='testmodel',
            name='test',
            field=models.TextField(default='x', max_length=100),
        ),
    ]
