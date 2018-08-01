from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("loggedin", views.loggedin_view, name="loggedin"),
    path("logout", views.logout_view, name="logout"),
    path("signup", views.signup_view, name="signup"),
    path("signupsuccess", views.signupsuccess_view, name="signupsuccess"),
    path("menu", views.menu_view, name="menu"),
    path("addtocart", views.add_to_cart_view, name="addtocart"),
    path("cart", views.cart_view, name="cart"),
    path("orderconfirm", views.order_confirm_view, name="orderconfirm"),
    path("orderplaced", views.order_placed_view, name="orderplaced"),
    path("myorder", views.my_order_view, name="myorder"),
    path("manageorders", views.manage_orders_view, name="manageorders")
    #path("orderstatus_change", views.orderstatus_change_view, name="orderstatus_change")
]
