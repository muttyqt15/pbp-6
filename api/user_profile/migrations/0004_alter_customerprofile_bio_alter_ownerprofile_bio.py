# Generated by Django 5.1.2 on 2024-10-27 16:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_profile', '0003_alter_ownerprofile_restaurant'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customerprofile',
            name='bio',
            field=models.TextField(blank=True, default='no bio', null=True, verbose_name='Biography'),
        ),
        migrations.AlterField(
            model_name='ownerprofile',
            name='bio',
            field=models.TextField(blank=True, default='no bio', null=True, verbose_name='Biography'),
        ),
    ]
