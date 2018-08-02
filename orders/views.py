from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .models import *
from django.db.models import Q




def index(request):

    # if user is not logged in, send to main home page
    if not request.user.is_authenticated:
        return render(request, "orders/index.html")

    # if user is logged in, retrieve user information
    context = {
        "user": request.user
    }

    # if user is admin, take to superuser home page
    if request.user.is_superuser:
        return render(request, "orders/superuser.html", context)

    # if user is customer, take to user home page
    else:
        return render(request, "orders/user.html", context)




def login_view(request):

    # log user out if logged in user visits login page
    logout(request)
    return render(request, "orders/login.html")




def loggedin_view(request):

    # check if request method is POST (which is the correct method)
    if request.method == "POST":

        # check if username and password matches
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # if user with matching ID and password exists, log in and take to user home page
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))

        # if ID and password doesn't match, give error
        else:
            return render(request, "orders/login.html", {"message": "Invalid credentials. Please try again."})

    # if request method is GET, take to main page
    else:
        return HttpResponseRedirect(reverse("index"))




def logout_view(request):

    #log out user
    logout(request)
    return render(request, "orders/login.html", {"message": "You are now logged out."})




def signup_view(request):
    return render(request, "orders/signup.html")




def signupsuccess_view(request):

    # if request method is POST (which is the correct method)
    if request.method == "POST":

        # get signup form information
        username = request.POST["username"]
        password = request.POST["password"]
        first_name = request.POST["first_name"]
        last_name = request.POST["last_name"]
        email = request.POST["email"]

        # if any part of the form is empty, return error
        if (username == '') or (password == '') or (first_name == '') or (last_name == '') or (email == ''):
            return render(request, "orders/signup.html", {"message": "Please fill out every form to sign up."})

        # if username already exists, return error
        if User.objects.filter(username=username).exists():
            return render(request, "orders/signup.html", {"message": "ID already taken. Please try a different ID."})

        # add new user information to database
        else:
            user = User.objects.create_user(username, password=password, email=email)
            user.last_name = last_name
            user.first_name = first_name
            user.save()

            # create empty cart for this user
            cart = Cart.objects.create(user = user)

            return render(request, "orders/signupsuccess.html")

    # if request method is not POST, take to signup page
    else:
        return HttpResponseRedirect(reverse("signup"))




def menu_view(request):

    # if user is not logged in, take to main home page
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("index"))

    # if user is superuser, take to superuser home page
    elif request.user.is_superuser:
        return HttpResponseRedirect(reverse("index"))

    # retrieve user and menu information
    else:
        context = {
            "user": request.user,
            "menu": Menu.objects.all()
        }
        return render(request, "orders/menu.html", context)




def add_to_cart_view(request):

    # if request method is post (which is the correct method)
    if request.method == "POST":

        # retrieve user and cart information
        user = request.user
        cart = Cart.objects.get(user = user)

        # get all menu ids
        menulist = Menu.objects.values('id')

        for menu_id in menulist:

            # get quantity values of the menu item in the form user submitted
            qty = request.POST[str(menu_id['id'])]

            # if quantity value is blank, set qty to 0
            if (qty == '') or (qty is None):
                qty = 0
            qty = int(qty)

            # if quantity is bigger than 0
            if (qty > 0):

                # retrieve menu item information
                item = Menu.objects.get(pk = menu_id['id'])

                # create cart entry for each item quantity
                for i in range(qty):
                    cart_entry = CartEntry.objects.create(cart = cart, item = item, quantity = 1)

                # update cart count and total price information
                cart.count += qty
                cart.total += item.price * qty

        cart.save()
        return render(request, "orders/addtocart.html")

    # if request method is not POST, take user to menu page
    else:
        return HttpResponseRedirect(reverse("menu"))




def cart_view(request):

    # if user is not logged in, take to main home page
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("index"))

    # if user is superuser, take to superuser page
    elif request.user.is_superuser:
        return HttpResponseRedirect(reverse("index"))

    # if user is customer
    else:

        # get user and user's cart information
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
    # if user is not logged in, take to main home page
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("index"))

    # if user is admin, take to superuser home page
    elif request.user.is_superuser:
        return HttpResponseRedirect(reverse("index"))

    # if user is customer,
    else:

        # get user, cart, toppings information
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

    # if request method is POST (this is the correct method)
    if request.method =="POST":

        # get user, cart, and cart entry information
        user = request.user
        cart = Cart.objects.get(user=user)
        cartentry = CartEntry.objects.filter(cart=cart)

        # for each entry in the cart entries (for each item in the cart)
        for entry in cartentry:

            # if item in the cart is pizza that requires toppings
            if (entry.item.topping > 0):
                # if user added toppings for this pizza in the form
                if str(entry.id) in request.POST:
                    # if user previously already selected toppings for this pizza, throw error
                    if (PizzaToppingEntry.objects.filter(cartentry=entry).count() == entry.item.topping):
                        return render(request, "orders/error.html", {"message": "Pizza toppings for your pizza items have already been selected."})

                    # retrieve topping list information the user submitted in the form
                    updates_list = request.POST.getlist(str(entry.id))

                    # if number of toppings selected do not match this pizza's appropriate number of topping, throw error
                    if (len(updates_list) != entry.item.topping):
                        return render(request, "orders/error.html", {"message": "Please choose the correct number of toppings for your pizza."})

                    # for each topping in the topping list information
                    for topping in updates_list:

                        # create pizza topping entry
                        pztoppingentry = PizzaToppingEntry(cartentry=entry)
                        pztoppingentry.topping = PizzaTopping.objects.get(name=topping)
                        pztoppingentry.save()

            # if item in the cart is sub
            elif entry.item.category == "Sub":

                # if user updated toppings for this sub in the form
                if str(entry.id) in request.POST:

                    # get list of toppings user updated in the form
                    updates_list = request.POST.getlist(str(entry.id))

                    # for each topping in the topping list, create sub topping entry
                    for topping in updates_list:
                        subtoppingentry = SubToppingEntry(cartentry=entry)
                        subtoppingentry.topping = SubTopping.objects.get(name=topping)
                        subtoppingentry.save()

                        # since sub toppings have additional price, add price to cart accordingly
                        cart.total += SubTopping.objects.get(name=topping).price

        cart.save()
        return render(request, "orders/toppingsadded.html")

    else:
        return HttpResponseRedirect(reverse('addtoppings'))




def order_confirm_view(request):

    # if user is not authenticated, take user to main home page
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("index"))

    # if user is superuser, take to superuser home page
    elif request.user.is_superuser:
        return HttpResponseRedirect(reverse("index"))

    # if user is customer, retrieve user and user's cart information
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

    # if get request method is POST (this is the correct method)
    if request.method == "POST":

        user = request.user
        cart = Cart.objects.get(user = user)
        cartentry = CartEntry.objects.filter(cart = cart)
        pztoppingentry = PizzaToppingEntry.objects.filter(cartentry = cartentry)
        subtoppingentry = SubToppingEntry.objects.filter(cartentry = cartentry)

        # create user's order database
        order = Order.objects.create(user = user, total = cart.total, count = cart.count)

        # for each item in the cart
        for entry in cartentry:

            # add each item in the order
            item = entry.item
            qty = entry.quantity
            orderentry = OrderEntry.objects.create(item = item, order = order, quantity = qty)

            # if item is pizza item that requires topping
            if (entry.item.topping > 0):

                # retrieve its toppings information
                toppingentries = PizzaToppingEntry.objects.filter(cartentry = entry)

                # for each topping of this item, add to order (more specifically, topping entry for order database)
                for t_entry in toppingentries:
                    topping = PizzaTopping.objects.get(name=t_entry.topping)
                    pztopping_orderentry = PizzaTopping_OrderEntry.objects.create(orderentry = orderentry, topping = topping)

            # if item in the cart is sub that may have toppings
            elif entry.item.category == "Sub":

                # retrieve its toppings information
                toppingentries = SubToppingEntry.objects.filter(cartentry = entry)

                # for each topping of this item, add to order
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

    # if user is not logged in, bring to main home page
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("index"))

    # if user is superuser, bring to superuser home page
    elif request.user.is_superuser:
        return HttpResponseRedirect(reverse("index"))

    # if user is customer
    else:
        user = request.user

        # if user's order exists, get order information (order, orderentry, pizza topping entry, sub topping entry)
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

    # if user is not logged in, bring to main home page
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("index"))

    # if user is not superuser, throw error
    elif not request.user.is_superuser:
        return render(request, "orders/error.html", {"message": "Only admins can access this page."})

    # if user is superuser
    else:

        # retrieve order information from all customers
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

    # if request method is POST (which is the correct method)
    if request.method == "POST":

        # get the order id that the status was changed to complete
        order_id = request.POST["complete"]

        # retrieve that specific order and change status as complete
        order = Order.objects.get(pk = order_id)
        order.status = "Complete"
        order.save()

        context = {
        "order": order
        }

        return render(request, "orders/orderstatus_change.html", context)

    # if request method is not POST, take to manage order page
    else:
        return HttpResponseRedirect(reverse("manageorders"))
