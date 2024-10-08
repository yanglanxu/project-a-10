from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib.auth import logout
from django.urls import reverse
from django.shortcuts import get_object_or_404, render, redirect
from django.views.generic.edit import FormView
from .forms import ReportForm
from .models import User, Report, ReportFile, Comment
from a10app.templatetags.auth_extras import has_group
from django.views.decorators.http import require_POST
from django.db.models import Q
from django.contrib import messages

def opening_page(request):
    return render(request, "opening_page.html")


def main_page(request):
    reports = Report.objects.filter(status="Resolved")
    return render(request, "main_page.html", {"reports": reports})

def logout_view(request):
    logout(request)
    return redirect("/")

class ReportFormView(FormView):
    form_class = ReportForm
    template_name = "make_report.html"  # Replace with your template.
    success_url = "/main"  # Replace with your URL or reverse().

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
            if not request.POST.get("anon"):
                report.user=User.objects.get(id=request.user.id)
        report.text = form.cleaned_data["text"]
        report.location = form.cleaned_data["location"]
        report.urgency = form.cleaned_data["urgency"]
        report.save()
        files = form.cleaned_data["files"]
        for f in files:
            new_upload = ReportFile(report=report, file=f)
            new_upload.save()
        return super().form_valid(form)

    def form_invalid(self, form):
        """
        If the form is invalid, re-render the page with error messages.
        """
        for field, errors in form.errors.items():
            for error in errors:
                messages.error(self.request, f"Error in {field}: {error}")
        return super().form_invalid(form)



def report_list(request):
    reports = Report.objects.all()
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

def save_user_comments(request, report_id):
        report = Report.objects.get(id=report_id)
        # Get the comment content from the form
        user_comments = request.POST["user_comments"]
        comment = Comment(report=report, user=request.user, content=user_comments)
        comment.save()
        
        # Redirect back to the same report page
        return view_report(request, report_id)

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

def flag(request, report_id):
    report = Report.objects.get(id=report_id)
    report.flagged += 1
    report.save()
    return redirect("a10app:view_report",report_id=report_id)

def search_reports(request):
    search_parameter = request.POST["search_parameters"]
    search_parameter = search_parameter.strip()


    q_filter = Q()
    for field in ["title", "status", "text"]:
        q_filter |= Q(**{f"{field}__icontains": search_parameter})

    reports = Report.objects.filter(q_filter, status="Resolved")
    return render(request, "main_page.html", {"reports": reports, "search_parameter": search_parameter})

def update_comment(request):
    print("In update_comment")
    if request.method == 'POST' and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        # print("Past if")
        comment_id = request.POST.get('comment_id')
        content = request.POST.get('content')
        print("Comment ID: ", comment_id)
        print("Content: ", content)

        comment = Comment.objects.get(id=comment_id, user=request.user)  # Ensure user can only edit their own comment
        if comment:
            comment.content = content
            comment.save()
            return JsonResponse({'status': 'success', 'message': 'Comment updated successfully.'})
    return JsonResponse({'status': 'error', 'message': 'Failed to update comment.'})

    