from django.http import HttpResponse


# Create your views here.

def register(request):
    return HttpResponse("this is user register.")


def login(request):
    return HttpResponse("this is user loggin.")


def pass_reset(request):
    return HttpResponse("this is password reset")


def logout(request):
    return HttpResponse("this is user logout.")
