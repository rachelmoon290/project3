# Generated by Django 2.0.7 on 2018-08-01 20:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0033_auto_20180731_1400'),
    ]

    operations = [
        migrations.AddField(
            model_name='menu',
            name='topping',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
