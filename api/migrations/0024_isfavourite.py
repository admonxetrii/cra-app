# Generated by Django 3.2.9 on 2022-03-22 01:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0023_favourites'),
    ]

    operations = [
        migrations.CreateModel(
            name='IsFavourite',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_favourite', models.BooleanField()),
            ],
        ),
    ]