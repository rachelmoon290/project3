from django.db import models
from django.contrib.auth.models import User

# Create your models here.
'''
class Pizza(models.Model):


'''

class Salad(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=7, decimal_places=2)
    #carts = models.ManyToManyField(Cart, blank=True, related_name="salads")

    def __str__(self):
        return f"{self.name} — ${self.price}"

class Pasta(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=7, decimal_places=2)

    #carts = models.ManyToManyField(Cart, blank=True, related_name="pastas")
    def __str__(self):
        return f"{self.name} — ${self.price}"



'''class Cart(models.Model):
    user = models.ForeignKey(User)
    item =
    totalprice =
'''
