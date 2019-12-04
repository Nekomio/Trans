from django.urls import path

from . import views

urlpatterns = [

    path('register', views.register, name='user.register'),
    path('logout', views.logout, name='user.logout'),

    path('get_excel', views.get_excel, name="back_stage.get_excel"),
    path('register/get_passcode', views.register, name='get_passcode'),
    path('register/create', views.register, name='create'),
    path('login', views.login, name='user.login'),
    path('submit', views.information_filling, name='user.information'),
]
