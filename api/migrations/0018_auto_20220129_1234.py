# Generated by Django 3.2.9 on 2022-01-29 06:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0017_alter_restauranttable_floorlevel'),
    ]

    operations = [
        migrations.CreateModel(
            name='TableReservationDates',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(blank=True, null=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='restauranttable',
            name='reserved',
        ),
        migrations.AddField(
            model_name='restauranttable',
            name='reservationDate',
            field=models.ManyToManyField(blank=True, null=True, to='api.TableReservationDates'),
        ),
    ]
