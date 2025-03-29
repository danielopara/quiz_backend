from django.urls import path

from .views import get_auth_user, get_user, login, register

urlpatterns = [
    path('register', register),
    path('get-user', get_user),
    path('login', login),
    path('', get_auth_user)
]
