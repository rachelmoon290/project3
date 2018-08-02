# Generated by Django 2.0.7 on 2018-08-01 23:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0042_auto_20180801_1931'),
    ]

    operations = [
        migrations.CreateModel(
            name='PizzaToppingEntry',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cartentry', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='orders.CartEntry')),
                ('topping', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='topping', to='orders.PizzaTopping')),
            ],
            options={
                'verbose_name': 'Pizza Topping Entry',
                'verbose_name_plural': 'Pizza Topping Entries',
            },
        ),
        migrations.CreateModel(
            name='SubToppingEntry',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cartentry', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='orders.CartEntry')),
                ('topping', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='topping', to='orders.SubTopping')),
            ],
            options={
                'verbose_name': 'Sub Topping Entry',
                'verbose_name_plural': 'Sub Topping Entries',
            },
        ),
        migrations.RemoveField(
            model_name='pizzatopping_entry',
            name='cartentry',
        ),
        migrations.RemoveField(
            model_name='pizzatopping_entry',
            name='topping',
        ),
        migrations.RemoveField(
            model_name='subtopping_entry',
            name='cartentry',
        ),
        migrations.RemoveField(
            model_name='subtopping_entry',
            name='topping',
        ),
        migrations.DeleteModel(
            name='PizzaTopping_Entry',
        ),
        migrations.DeleteModel(
            name='SubTopping_Entry',
        ),
    ]
