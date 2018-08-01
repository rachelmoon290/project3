from django.db import models
from django.contrib.auth.models import User


class Menu(models.Model):
    FOOD_CHOICES = (
        ('RegularPizza', 'Regular Pizza'),
        ('SicilianPizza', 'Sicilian Pizza'),
        ("Sub", 'Sub'),
        ("Salad", 'Salad'),
        ("Pasta", 'Pasta'),
        ("DinnerPlatter", 'Dinner Platter'),
        ("PizzaTopping", 'Pizza Topping'),
        ("SubTopping", 'Sub Topping')
    )
    SIZE_CHOICES = (
        ("Small", "Small"),
        ("Large", "Large")
    )
    category = models.CharField(max_length=20, choices=FOOD_CHOICES)
    name = models.CharField(max_length=200)
    size = models.CharField(max_length=6, choices=SIZE_CHOICES, null=True, blank=True)
    price = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        if self.size is not None:
            return f"{self.get_category_display()}: {self.name} ({self.size}) — ${self.price}"
        else:
            return f"{self.get_category_display()}: {self.name} — ${self.price}"



class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="carts")
    updated = models.DateTimeField(auto_now=True)
    count = models.PositiveIntegerField(default=0)
    total = models.DecimalField(max_digits=7, default=0, decimal_places=2)

    def __str__(self):
        return f"{self.user.username}'s cart: {self.count} items — ${self.total}"



class Order(models.Model):
    STATUS_CHOICES = (
        ("Pending", "Pending"),
        ("Complete", "Complete")
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name = "orders")
    created = models.DateTimeField(auto_now_add=True)
    count = models.PositiveIntegerField(default=0)
    total = models.DecimalField(max_digits=7, default=0, decimal_places=2)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="Pending")

    def __str__(self):
        return f"{self.user.username}'s order ({self.status}): {self.count} items — ${self.total}"



class CartEntry(models.Model):
    item = models.ForeignKey(Menu, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name = 'Cart Entry'
        verbose_name_plural = 'Cart Entries'

    def __str__(self):
        return f"{self.item.get_category_display()}: {self.item.name} (Qty={self.quantity}) added to {self.cart.user}'s Cart."



class OrderEntry(models.Model):
    item = models.ForeignKey(Menu, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name = 'Order Entry'
        verbose_name_plural = 'Order Entries'

    def __str__(self):
        return f"{self.order.user} ordered {self.item.get_category_display()}: {self.item.name} (Qty={self.quantity})."
