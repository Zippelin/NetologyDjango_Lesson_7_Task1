# Generated by Django 3.1.2 on 2021-06-03 10:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('advertisements', '0004_auto_20210603_1332'),
    ]

    operations = [
        migrations.AlterField(
            model_name='advertisement',
            name='creator',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='advertisements.person'),
        ),
    ]
