# Generated by Django 4.1 on 2022-08-12 03:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0004_merge_0003_alter_option_count_0003_alter_poll_public'),
    ]

    operations = [
        migrations.AlterField(
            model_name='poll',
            name='expires',
            field=models.DateTimeField(blank=True, default='2022-08-12 03:04', null=True),
        ),
    ]