# Generated by Django 3.2.9 on 2022-04-02 02:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0012_userrestaurant'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userrestaurant',
            old_name='course',
            new_name='restaurant',
        ),
    ]
