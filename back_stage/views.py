from django.http import HttpResponse


# Create your views here.

def login(request):
    return HttpResponse("this is back_stage login.")


def logout(request):
    return HttpResponse("this is back_stage logout.")


def home(request):
    return HttpResponse("this is back_stage home.")
