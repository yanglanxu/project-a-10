from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import logout
from django.urls import reverse
from django.shortcuts import get_object_or_404, render, redirect
from django.views.generic.edit import FormView
from .forms import ReportForm
from .models import User, Report, ReportFile
from django.views.decorators.http import require_POST


def index(request):
    # print("why am I in here booo")

    return render(request, "index.html")

def main_page(request):
    return render(request, "main_page.html", {"reports": Report.objects.all()})

def logout_view(request):
    logout(request)
    return redirect("/")

def redirect_to_report(request):
    return redirect('/report')

class ReportFormView(FormView):
    form_class = ReportForm
    template_name = "report.html"  # Replace with your template.
    success_url = "/"  # Replace with your URL or reverse().

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        if form.is_valid():
            return self.form_valid(form, request)
        else:
            return self.form_invalid(form)

    def form_valid(self, form, request):
        report = Report()
        report.title = form.cleaned_data["title"]
        report.user=User.objects.get(id=request.user.id)
        report.text = form.cleaned_data["text"]
        report.urgency = form.cleaned_data["urgency"]
        # report.reviewed = False
        report.save()
        files = form.cleaned_data["files"]
        for f in files:
            new_upload = ReportFile(report=report, file=f)
            new_upload.save()
        return super().form_valid(form)

def report_list(request):
    reports = Report.objects.all()
    print(reports)
    return render(request, "report_list.html", {"reports" : reports})

def view_report(request, report_id):
    report = Report.objects.get(id=report_id)
    print(report.reviewed)
    files = ReportFile.objects.filter(report=report)
    return render(request, "view_report.html", {"report" : report, "files" : files})

def review_report(request, report_id):
    report = Report.objects.get(id=report_id)
    files = ReportFile.objects.filter(report=report)
    return render(request, "view_report.html", {"report" : report, "files" : files})

def mark_report_as_reviewed(request, report_id):
    report = Report.objects.get(id=report_id)
    report.reviewed = True

    report.save()

    
    return render(request, "report_list.html", {"reports" : Report.objects.all()})
