# Generated by Django 5.0.2 on 2024-10-24 19:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('thread', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='thread',
            name='title',
        ),
        migrations.AlterField(
            model_name='comment',
            name='content',
            field=models.TextField(max_length=345),
        ),
        migrations.AlterField(
            model_name='thread',
            name='content',
            field=models.TextField(max_length=456),
        ),
    ]
