# Generated by Django 3.1.3 on 2020-12-04 12:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_auto_20201204_1214'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='date_registered',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
