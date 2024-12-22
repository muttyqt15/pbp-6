# Generated by Django 5.0.2 on 2024-12-21 18:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_profile', '0007_alter_customerprofile_user_alter_ownerprofile_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='customerprofile',
            name='profile_pic_url',
            field=models.URLField(blank=True, default='https://cdn.pixabay.com/photo/2015/10/05/22/37/blank-profile-picture-973460_640.png', null=True),
        ),
        migrations.AddField(
            model_name='ownerprofile',
            name='profile_pic_url',
            field=models.URLField(blank=True, default='https://cdn.pixabay.com/photo/2015/10/05/22/37/blank-profile-picture-973460_640.png', null=True),
        ),
        migrations.AlterField(
            model_name='customerprofile',
            name='profile_pic',
            field=models.ImageField(blank=True, default='profile_pics/default.png', null=True, upload_to='profile_pics/'),
        ),
        migrations.AlterField(
            model_name='ownerprofile',
            name='profile_pic',
            field=models.ImageField(blank=True, default='profile_pics/default.png', null=True, upload_to='profile_pics/'),
        ),
    ]