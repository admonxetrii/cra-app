# Generated by Django 3.2.9 on 2022-01-27 17:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0013_mergetable_restauranttable'),
    ]

    operations = [
        migrations.CreateModel(
            name='RestaurantFloorLevel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('floorName', models.CharField(blank=True, max_length=65, null=True)),
                ('restaurant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.restaurant')),
            ],
            options={
                'db_table': 'RESTAURANT_FLOOR_MASTER',
            },
        ),
    ]
