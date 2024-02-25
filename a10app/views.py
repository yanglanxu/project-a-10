from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import logout
from django.urls import reverse

def index(request):
    return render(request, "index.html")


def welcome(request, username):
    return render(request, "welcome.html", {"user": username})


def logout(request):
    logout(request)
    return redirect("/")
