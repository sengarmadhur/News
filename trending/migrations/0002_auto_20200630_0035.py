# Generated by Django 3.0.6 on 2020-06-29 19:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('trending', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='trending',
            old_name='heading',
            new_name='headline',
        ),
    ]