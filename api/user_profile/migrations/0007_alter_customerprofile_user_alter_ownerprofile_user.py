# Generated by Django 5.1.2 on 2024-10-27 20:07

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0002_restaurantowner_restaurant'),
        ('user_profile', '0006_alter_customerprofile_bio_alter_ownerprofile_bio'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customerprofile',
            name='user',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='authentication.customer'),
        ),
        migrations.AlterField(
            model_name='ownerprofile',
            name='user',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='authentication.restaurantowner'),
        ),
    ]
