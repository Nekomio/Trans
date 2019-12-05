"""AIR_System URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.shortcuts import render
from django.urls import path, include
from django.views import static

from AIR_System.settings import STATIC_ROOT

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('home.urls')),
    url('^static/(?P<path>.*)$', static.serve, {'document_root': STATIC_ROOT}, name='static')
]


def page_not_found_404(request, status):
    print(status)
    return render(request, "my_404.html", status=404)


def page_not_found_403(request, status):
    print(status)
    return render(request, "my_403.html", status=403)


def page_not_found_500(request):
    # print(status)
    return render(request, "my_404.html", status=500)


handler404 = page_not_found_404
handler500 = page_not_found_500
handler403 = page_not_found_403
