# Generated by Django 2.0.7 on 2018-07-28 00:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0005_auto_20180728_0034'),
    ]

    operations = [
        migrations.RenameField(
            model_name='dinnerplatter',
            old_name='size_category',
            new_name='category',
        ),
    ]
