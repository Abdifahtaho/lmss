# Generated by Django 5.2.1 on 2025-07-13 18:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('land_management', '0017_landregistration_land_direction_north'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='landmapping',
            name='map_document',
        ),
    ]
