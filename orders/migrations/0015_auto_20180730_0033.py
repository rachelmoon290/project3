# Generated by Django 2.0.7 on 2018-07-30 00:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0014_auto_20180729_2354'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='totalprice',
            new_name='total',
        ),
    ]
