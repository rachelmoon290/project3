# Generated by Django 2.0.7 on 2018-07-31 01:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0028_auto_20180730_2139'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cartentry',
            name='quantity',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
