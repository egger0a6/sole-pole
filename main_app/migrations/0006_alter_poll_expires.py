# Generated by Django 4.1 on 2024-06-24 20:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0005_alter_poll_expires'),
    ]

    operations = [
        migrations.AlterField(
            model_name='poll',
            name='expires',
            field=models.DateTimeField(blank=True, default='2024-06-24 20:24', null=True),
        ),
    ]
