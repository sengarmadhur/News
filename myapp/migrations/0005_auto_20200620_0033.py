# Generated by Django 3.0.6 on 2020-06-19 19:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0004_auto_20200619_2336'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='picname2',
            field=models.TextField(default=''),
        ),
        migrations.AddField(
            model_name='article',
            name='picurl2',
            field=models.TextField(default=''),
        ),
    ]