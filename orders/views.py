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
                for i in range(qty):
                    cart_entry = CartEntry.objects.create(cart = cart, item = item, quantity = 1)

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
        pztoppingentry = PizzaToppingEntry.objects.filter(cartentry__in = cartentry)
        subtoppingentry = SubToppingEntry.objects.filter(cartentry__in = cartentry)

        context = {
            "user": user,
            "cart": cart,
            "cartentry": cartentry,
            "pztoppingentry": pztoppingentry,
            "subtoppingentry": subtoppingentry
        }
        return render(request, "orders/cart.html", context)


def addtoppings_view(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("index"))
    elif request.user.is_superuser:
        return HttpResponseRedirect(reverse("index"))
    else:

        user = request.user
        cart = Cart.objects.get(user = user)
        cartentry = CartEntry.objects.filter(cart = cart)
        pizzatoppings = PizzaTopping.objects.all()
        subtoppings = SubTopping.objects.all()

        context = {
            "user": user,
            "cart": cart,
            "cartentry": cartentry,
            "pizzatoppings": pizzatoppings,
            "subtoppings": subtoppings
        }
        return render(request, "orders/addtoppings.html", context)


def added_toppings_view(request):

    if request.method =="POST":

        user = request.user
        cart = Cart.objects.get(user=user)
        cartentry = CartEntry.objects.filter(cart=cart)


        for entry in cartentry:

            # if item in the cart is pizza with toppings
            if (entry.item.topping > 0):
                if str(entry.id) in request.POST:
                    updates_list = request.POST.getlist(str(entry.id))
                    if (len(updates_list) != entry.item.topping):
                        return render(request, "orders/error.html", {"message": "Please choose the correct number of toppings for your pizza."})

                    for topping in updates_list:
                        pztoppingentry = PizzaToppingEntry(cartentry=entry)
                        pztoppingentry.topping = PizzaTopping.objects.get(name=topping)
                        pztoppingentry.save()
            # if item in the cart is sub
            elif entry.item.category == "Sub":
                if str(entry.id) in request.POST:
                    updates_list = request.POST.getlist(str(entry.id))
                    for topping in updates_list:
                        subtoppingentry = SubToppingEntry(cartentry=entry)
                        subtoppingentry.topping = SubTopping.objects.get(name=topping)
                        subtoppingentry.save()
                        cart.total += SubTopping.objects.get(name=topping).price

        cart.save()
        return render(request, "orders/toppingsadded.html")

    else:
        return HttpResponseRedirect(reverse('addtoppings'))



def order_confirm_view(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("index"))
    elif request.user.is_superuser:
        return HttpResponseRedirect(reverse("index"))
    else:
        user = request.user
        cart = Cart.objects.get(user = user)
        cartentry = CartEntry.objects.filter(cart = cart)
        pztoppingentry = PizzaToppingEntry.objects.filter(cartentry__in = cartentry)
        subtoppingentry = SubToppingEntry.objects.filter(cartentry__in = cartentry)


        context = {
            "user": user,
            "cart": cart,
            "cartentry": cartentry,
            "pztoppingentry": pztoppingentry,
            "subtoppingentry": subtoppingentry
        }
        return render(request, "orders/orderconfirm.html", context)


def order_placed_view(request):

    if request.method == "POST":
        user = request.user
        cart = Cart.objects.get(user = user)
        cartentry = CartEntry.objects.filter(cart = cart)
        pztoppingentry = PizzaToppingEntry.objects.filter(cartentry = cartentry)
        subtoppingentry = SubToppingEntry.objects.filter(cartentry = cartentry)

        order = Order.objects.create(user = user, total = cart.total, count = cart.count)

        for entry in cartentry:

            item = entry.item
            qty = entry.quantity
            orderentry = OrderEntry.objects.create(item = item, order = order, quantity = qty)

            if (entry.item.topping > 0):
                toppingentries = PizzaToppingEntry.objects.filter(cartentry = entry)
                for t_entry in toppingentries:
                    topping = PizzaTopping.objects.get(name=t_entry.topping)
                    pztopping_orderentry = PizzaTopping_OrderEntry.objects.create(orderentry = orderentry, topping = topping)

            # if item in the cart is sub
            elif entry.item.category == "Sub":
                toppingentries = SubToppingEntry.objects.filter(cartentry = entry)
                for t_entry in toppingentries:
                    topping = SubTopping.objects.get(name=t_entry.topping)
                    subtopping_orderentry = SubTopping_OrderEntry.objects.create(orderentry = orderentry, topping = topping)




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
            pztoppingentry = PizzaTopping_OrderEntry.objects.filter(orderentry__in = orderentry)
            subtoppingentry = SubTopping_OrderEntry.objects.filter(orderentry__in = orderentry)

            context = {
                "user": user,
                "orders": orders,
                "orderentry": orderentry,
                "pztoppingentry": pztoppingentry,
                "subtoppingentry": subtoppingentry
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
        pztoppingentry = PizzaTopping_OrderEntry.objects.filter(orderentry__in = orderentry)
        subtoppingentry = SubTopping_OrderEntry.objects.filter(orderentry__in = orderentry)


        context = {
            "orders": orders,
            "orderentry": orderentry,
            "pztoppingentry": pztoppingentry,
            "subtoppingentry": subtoppingentry
        }
        return render(request, "orders/manageorders.html", context)

def orderstatus_change_view(request):

    if request.method == "POST":
        order_id = request.POST["complete"]


        order = Order.objects.get(pk = order_id)
        order.status = "Complete"
        order.save()

        context = {
        "order": order
        }


        return render(request, "orders/orderstatus_change.html", context)


    else:
        return HttpResponseRedirect(reverse("manageorders"))
