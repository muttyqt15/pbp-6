# Generated by Django 5.1.2 on 2024-10-26 16:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('restaurant', '0008_remove_food_category_remove_food_restaurant_menu_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='food',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]
