# Generated by Django 3.0.6 on 2020-07-06 13:46

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Comments',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250)),
                ('email', models.CharField(max_length=250)),
                ('news_id', models.IntegerField(max_length=250)),
                ('comments', models.TextField()),
                ('date', models.CharField(max_length=250)),
                ('time', models.CharField(max_length=250)),
            ],
        ),
    ]
