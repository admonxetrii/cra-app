# Generated by Django 3.2.9 on 2022-04-03 14:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0028_tablereservationdates_cancelled'),
    ]

    operations = [
        migrations.AddField(
            model_name='tablereservationdates',
            name='success',
            field=models.BooleanField(default=0),
        ),
    ]
