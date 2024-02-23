from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import logout

def index(request):
    return render(request, "index.html")

def logout(request):
    logout(request)
    return redirect("/")
