from django.urls import path
from . import views

urlpatterns = [
    path('',views.home,name="index_page"),
    path('login',views.login,name="login_page"),
    path('signup',views.Signup,name="signup_page"),
    path('logout',views.Logout,name="logout_page"),

]