# Generated by Django 3.2.9 on 2022-01-03 19:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_restaurantfeaturedmenu_restaurantfeaturedmenuforrestaurant_restauranttype_restauranttypeofrestaurant'),
    ]

    operations = [
        migrations.AddField(
            model_name='restauranttype',
            name='icon',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='restauranttype',
            name='name',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
