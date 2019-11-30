from django.urls import path

from . import views

urlpatterns = [
    path('login', views.login, name='back_stage.login'),
    path('logout', views.logout, name='back_stage.logout'),
    path('home', views.home, name='back_stage.home'),
    path('get_excel', views.get_excel, name="back_stage.get_excel"),
]
