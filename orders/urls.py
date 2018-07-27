from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("loggedin", views.loggedin_view, name="loggedin"),
    path("logout", views.logout_view, name="logout"),
    path("signup", views.signup_view, name="signup"),
    path("signupsuccess", views.signupsuccess_view, name="signupsuccess")
]
