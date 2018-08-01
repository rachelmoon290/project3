from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .models import *
from django.db.models import Q


def index(request):
    if not request.user.is_authenticated:
        return render(request, "orders/index.html")
    context = {
        "user": request.user
    }
    if request.user.is_superuser:
        return render(request, "orders/superuser.html", context)
    else:
        return render(request, "orders/user.html", context)



def login_view(request):
    logout(request)
    return render(request, "orders/login.html")


def loggedin_view(request):

    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "orders/login.html", {"message": "Invalid credentials. Please try again."})
    else:
        return HttpResponseRedirect(reverse("index"))


def logout_view(request):
    logout(request)
    return render(request, "orders/login.html", {"message": "You are now logged out."})



def signup_view(request):
    return render(request, "orders/signup.html")


def signupsuccess_view(request):

    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        first_name = request.POST["first_name"]
        last_name = request.POST["last_name"]
        email = request.POST["email"]

        if (username == '') or (password == '') or (first_name == '') or (last_name == '') or (email == ''):
            return render(request, "orders/signup.html", {"message": "Please fill out every form to sign up."})

        if User.objects.filter(username=username).exists():
            return render(request, "orders/signup.html", {"message": "ID already taken. Please try a different ID."})
        else:
            user = User.objects.create_user(username, password=password, email=email)
            user.last_name = last_name
            user.first_name = first_name
            user.save()

            cart = Cart.objects.create(user = user)

            return render(request, "orders/signupsuccess.html")
    else:
        return HttpResponseRedirect(reverse("signup"))


def menu_view(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("index"))
    elif request.user.is_superuser:
        return HttpResponseRedirect(reverse("index"))
    else:
        context = {
            "user": request.user,
            "menu": Menu.objects.all()
        }
        return render(request, "orders/menu.html", context)


def add_to_cart_view(request):

    if request.method == "POST":
        user = request.user
        cart = Cart.objects.get(user = user)

        menulist = Menu.objects.exclude(Q(category = "PizzaTopping") | Q(category = "SubTopping")).values('id')
        for menu_id in menulist:

            qty = request.POST[str(menu_id['id'])]
            if (qty == '') or (qty is None):
                qty = 0
            qty = int(qty)

            if (qty > 0):
                item = Menu.objects.get(pk = menu_id['id'])

                if (CartEntry.objects.filter(Q(cart = cart), Q(item = item)).count() == 0):
                    cart_entry = CartEntry(cart = cart, item = item)
                else:
                    cart_entry = CartEntry.objects.get(Q(cart = cart), Q(item = item))

                cart_entry.quantity += qty
                cart_entry.save()
                cart.count += qty
                cart.total += item.price * qty

        cart.save()
        return render(request, "orders/addtocart.html")
    else:
        return HttpResponseRedirect(reverse("menu"))


def cart_view(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("index"))
    elif request.user.is_superuser:
        return HttpResponseRedirect(reverse("index"))
    else:

        user = request.user
        cart = Cart.objects.get(user = user)
        cartentry = CartEntry.objects.filter(cart = cart)

        context = {
            "user": user,
            "cart": cart,
            "cartentry": cartentry
        }
        return render(request, "orders/cart.html", context)


def order_confirm_view(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("index"))
    elif request.user.is_superuser:
        return HttpResponseRedirect(reverse("index"))
    else:
        user = request.user
        cart = Cart.objects.get(user = user)
        cartentry = CartEntry.objects.filter(cart = cart)

        context = {
            "user": user,
            "cart": cart,
            "cartentry": cartentry
        }
        return render(request, "orders/orderconfirm.html", context)


def order_placed_view(request):

    if request.method == "POST":
        user = request.user
        cart = Cart.objects.get(user = user)
        cartentry = CartEntry.objects.filter(cart = cart)
        order = Order.objects.create(user = user, total = cart.total, count = cart.count)

        for entry in cartentry:

            item = entry.item
            qty = entry.quantity
            orderentry = OrderEntry.objects.create(item = item, order = order, quantity = qty)

        # delete current cart and recreate an empty cart
        cart.delete()
        cart = Cart.objects.create(user = user)

        return render(request, "orders/orderplaced.html")
    else:
        return HttpResponseRedirect(reverse("orderconfirm"))

def my_order_view(request):

    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("index"))
    elif request.user.is_superuser:
        return HttpResponseRedirect(reverse("index"))
    else:
        user = request.user

        if(Order.objects.filter(user = user).exists()):
            orders = Order.objects.filter(user = user)
            orderentry = OrderEntry.objects.filter(order__in = orders)

            context = {
                "user": user,
                "orders": orders,
                "orderentry": orderentry
            }
            return render(request, "orders/myorder.html", context)
        else:
            return render(request, "orders/error.html", {"message": "You did not order anything from our restaurant yet!"})

def manage_orders_view(request):

    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("index"))
    elif not request.user.is_superuser:
        return render(request, "orders/error.html", {"message": "Only admins can access this page."})
    else:
        orders = Order.objects.all()
        orderentry = OrderEntry.objects.filter(order__in = orders)

        context = {
            "orders": orders,
            "orderentry": orderentry
        }
        return render(request, "orders/manageorders.html", context)

'''
def orderstatus_change_view(request):

    if request.method == "POST":
        order_id = request.

        orders = Order.objects.all()
        orderentry = OrderEntry.objects.filter(order__in = orders)

        context = {
            "orders": orders,
            "orderentry": orderentry
        }
        return render(request, "orders/manageorders.html", context)


    else:
        return HttpResponseRedirect(reverse("manageorders"))
'''
