# Generated by Django 2.0.7 on 2018-07-30 21:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0027_auto_20180730_2136'),
    ]

    operations = [
        migrations.AlterField(
            model_name='menu',
            name='category',
            field=models.CharField(choices=[('RegularPizza', 'Regular Pizza'), ('SicilianPizza', 'Sicilian Pizza'), ('Sub', 'Sub'), ('Salad', 'Salad'), ('Pasta', 'Pasta'), ('DinnerPlatter', 'Dinner Platter'), ('PizzaTopping', 'Pizza Topping'), ('SubTopping', 'Sub Topping')], max_length=20),
        ),
    ]
