from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import logout
from django.urls import reverse
from django.shortcuts import get_object_or_404, render, redirect
from django.views.generic.edit import FormView
from .forms import ReportForm
from .models import User, Report, ReportFile
from a10app.templatetags.auth_extras import has_group
from django.views.decorators.http import require_POST
from django.db.models import Q


def index(request):
    # print("why am I in here booo")

    return render(request, "index.html")

def main_page(request):
    reports = Report.objects.filter(status="Resolved")
    return render(request, "main_page.html", {"reports": reports})

def logout_view(request):
    logout(request)
    return redirect("/")

class ReportFormView(FormView):
    form_class = ReportForm
    template_name = "make_report.html"  # Replace with your template.
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
        if not request.user.is_anonymous:
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

    if not request.user.is_anonymous:
        user = User.objects.get(id=request.user.id)
        if has_group(user, "site_admin") and report.status == "New":
            report.status="In Progress"
            report.save()

    files = ReportFile.objects.filter(report=report)
    pdf = ReportFile.objects.filter(report=report, content_type="application/pdf")
    text = ReportFile.objects.filter(report=report, content_type="text/plain")
    images = ReportFile.objects.filter(report=report ,content_type__contains="image")
    return render(request, "view_report.html", {"report" : report, "pdf" : pdf, "text" : text, "images" : images})

def mark_report_as_resolved(request, report_id):
    report = Report.objects.get(id=report_id)
    report.status = "Resolved"
    report.admin_comments = request.POST["comments"]
    report.save()

    return render(request, "report_list.html", {"reports" : Report.objects.all()})


def user_page(request):
    report_list = []
    if not request.user.is_anonymous:
        user = request.user
        report_list = Report.objects.filter(user=user)
    return render(request, "user_page.html", {"report_list": report_list})

def delete(request, report_id):
    report = Report.objects.get(id=report_id)
    if(request.user.id != report.user.id):
        return redirect("/")
    report.delete()
    return redirect("a10app:user_page")


def search_reports(request):
    search_parameter = request.POST["search_parameters"]
    #reports = Report.objects.filter(title__iregex = search_parameter, status__iregex = search_parameter)

    q_filter = Q()
    for field in ["title", "status", "text"]:
        q_filter |= Q(**{f"{field}__icontains": search_parameter})

    reports = Report.objects.filter(q_filter)
    return render(request, "main_page.html", {"reports": reports})