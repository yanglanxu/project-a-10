from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import logout
from django.urls import reverse
from django.shortcuts import get_object_or_404, render, redirect
from django.views.generic.edit import FormView
from .forms import ReportForm
from .models import User, Report, ReportFile


def index(request):
    # print("why am I in here booo")
    return render(request, "index.html")

def logout_view(request):
    logout(request)
    return redirect("/")

class ReportFormView(FormView):
    form_class = ReportForm
    template_name = "report.html"  # Replace with your template.
    success_url = "welcome"  # Replace with your URL or reverse().

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        report = Report()
        report.title = form.cleaned_data["title"]
        report.text = form.cleaned_data["text"]
        report.save()
        files = form.cleaned_data["files"]
        for f in files:
            new_upload = ReportFile(report=report, file=f)
            new_upload.save()
        return super().form_valid(form)


def submit(request):
    return render(request, "name.html", {"form": form})

