from django.urls import path
from .views import *
urlpatterns = [
    path("",auth_home),
    path("register/",register),
    path("login/",login),
    path("logout/",logout),
    path("get-user/",get_user),
    path("protectedAPI/",protectedView.as_view()),

]

