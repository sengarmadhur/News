# Generated by Django 3.0.6 on 2020-06-09 06:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('newss', '0002_news_author'),
    ]

    operations = [
        migrations.AddField(
            model_name='news',
            name='catid',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='news',
            name='catname',
            field=models.CharField(default='-', max_length=250),
        ),
        migrations.AddField(
            model_name='news',
            name='views',
            field=models.IntegerField(default=0),
        ),
    ]
