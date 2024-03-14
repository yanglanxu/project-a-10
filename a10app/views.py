from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import logout
from django.urls import reverse
from django.shortcuts import get_object_or_404, render, redirect
from .models import User


def index(request):
    # print("why am I in here booo")
    return render(request, "index.html")


def welcome(request, username):
    # user = get_object_or_404(Users, userName=username)
    # print(user.email)
    if request.user.is_superuser:
        # print("got in here woo")
        return render(request, "admin-welcome.html", {"username": request.user.username})
    else:
        return render(request, "welcome.html", {"username": request.user.username})
    # return render(request, "welcome.html", {"username": username})

def check(request):
    if request.user.is_superuser:
        # print("got in here woo")
        return render(request, "admin-welcome.html", {"username": request.user.username})
    else:
        return render(request, "welcome.html", {"username": request.user.username})

def logout_view(request):
    logout(request)
    return redirect("/")

def isAdmin(request):
    # user = get_object_or_404(Users, userName=username)
    # if user.is_superuser:
    #     print("got in here woo")
    #     return render(request, "admin-welcome.html", {"username": user.username})
    # else:
    #     return render(request, "welcome.html", {"username": user.username})
    return render(request, "welcome.html")
