from django.urls import path

from . import views

urlpatterns = [
    path('login', views.login, name='users.login'),
    path('register', views.register, name='user.register'),
    path('password_reset', views.pass_reset, name='user.pass_reset'),
    path('logout', views.logout, name='user.logout'),
]
