# Generated by Django 3.2.7 on 2021-09-18 09:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_event_title'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='text',
            field=models.TextField(default='', max_length=1000),
        ),
    ]
