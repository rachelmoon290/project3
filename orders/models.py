from django.db import models
from django.contrib.auth.models import User
#from picklefield.fields import PickledObjectField


class SizeCategory(models.Model):
    name = models.CharField(max_length=10)

    class Meta:
        verbose_name = 'Size'
        verbose_name_plural = 'Sizes'
    def __str__(self):
        return f"{self.name}"



class PizzaCategory(models.Model):
    name = models.CharField(max_length=20)

    class Meta:
        verbose_name = 'Pizza Type'
        verbose_name_plural = 'Pizza Types'
    def __str__(self):
        return f"{self.name}"



class PizzaTopping(models.Model):
    name = models.CharField(max_length=50)

    class Meta:
        verbose_name = "Pizza Topping"
        verbose_name_plural = "Pizza Toppings"
    def __str__(self):
        return f"{self.name}"



class SubTopping(models.Model):
    name = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=4, decimal_places=2)

    class Meta:
        verbose_name = "Sub Topping"
        verbose_name_plural = "Sub Toppings"
    def __str__(self):
        return f"{self.name}"



class Sub(models.Model):
    name = models.CharField(max_length=200)
    size = models.ForeignKey(SizeCategory, on_delete = models.PROTECT, related_name = "subs")
    price = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return f"{self.name} ({self.size}) — ${self.price}"



class Pizza(models.Model):
    name = models.CharField(max_length=200)
    type = models.ForeignKey(PizzaCategory, on_delete = models.PROTECT, related_name = "pizzas")
    size = models.ForeignKey(SizeCategory, on_delete = models.PROTECT, related_name = "pizzas")
    price = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return f"{self.type}, {self.name} ({self.size}) — ${self.price}"



class Salad(models.Model):
    name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return f"{self.name} — ${self.price}"



class Pasta(models.Model):
    name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return f"{self.name} — ${self.price}"



class DinnerPlatter(models.Model):
    name = models.CharField(max_length=200)
    size = models.ForeignKey(SizeCategory, null=True, on_delete = models.PROTECT, related_name = "dinnerplatters")
    price = models.DecimalField(max_digits=5, decimal_places=2)

    class Meta:
        verbose_name = 'Dinner Platter'
        verbose_name_plural = 'Dinner Platters'

    def __str__(self):
        return f"{self.name} ({self.size}) — ${self.price}"



class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="carts")

    #pasta = models.ManyToManyField(Pasta, blank=True, related_name="carts")
    #sub = models.ManyToManyField(Sub, blank=True, related_name="carts")
    #pizza = models.ManyToManyField(Pizza, blank=True, related_name="carts")
    #salad = models.ManyToManyField(Salad, blank=True, related_name="carts")
    #platter = models.ManyToManyField(DinnerPlatter, blank=True, related_name="carts")
    #subtopping = models.ManyToManyField(SubTopping, blank=True, related_name="carts")
    #pizzatopping = models.ManyToManyField(PizzaTopping, blank=True, related_name="carts")

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    count = models.PositiveIntegerField(default=0)
    total = models.DecimalField(max_digits=7, default=0, decimal_places=2)

    def __str__(self):
        return f"{self.user.username}'s cart: {self.count} items — ${self.total}"


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name = "orders")

    pasta = models.ManyToManyField(Pasta, blank=True, related_name="orders")
    sub = models.ManyToManyField(Sub, blank=True, related_name="orders")
    pizza = models.ManyToManyField(Pizza, blank=True, related_name="orders")
    salad = models.ManyToManyField(Salad, blank=True, related_name="orders")
    platter = models.ManyToManyField(DinnerPlatter, blank=True, related_name="orders")
    subtopping = models.ManyToManyField(SubTopping, blank=True, related_name="orders")
    pizzatopping = models.ManyToManyField(PizzaTopping, blank=True, related_name="orders")

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    count = models.PositiveIntegerField(default=0)
    total = models.DecimalField(max_digits=7, default=0, decimal_places=2)


    def __str__(self):
        return f"{self.user.username}'s order: {self.count} items — ${self.total}"




class Menu(models.Model):
    FOOD_CHOICES = (
        ('REG', 'Regular Pizza'),
        ('SIC', 'Sicilian Pizza'),
        ("SUB", 'Sub'),
        ("SAL", 'Salad'),
        ("PAS", 'Pasta'),
        ("PLA", 'Dinner Platter'),
        ("PT", 'Pizza Topping'),
        ("ST", 'Sub Topping')
    )
    SIZE_CHOICES = (
        ("SM", "Small"),
        ("LG", "Large")
    )
    category = models.CharField(max_length=5, choices=FOOD_CHOICES)
    name = models.CharField(max_length=200)
    size = models.CharField(max_length=2, choices=SIZE_CHOICES, null=True, blank=True)
    price = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        if self.size is not None:
            return f"{self.get_category_display()}: {self.name} ({self.get_size_display()}) — ${self.price}"
        else:
            return f"{self.get_category_display()}: {self.name} — ${self.price}"



class CartEntry(models.Model):
    item = models.ForeignKey(Menu, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    class Meta:
        verbose_name = 'Cart Entry'
        verbose_name_plural = 'Cart Entries'

    def __str__(self):
        return f"{self.item.get_category_display()}: {self.item.name} (Qty={self.quantity}) added to {self.cart.user}'s Cart."
