# Generated by Django 3.1.2 on 2021-06-03 11:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('advertisements', '0006_auto_20210603_1431'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='advertisementsusers',
            unique_together={('person', 'advertisement', 'is_favorite')},
        ),
    ]
