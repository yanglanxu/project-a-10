from django.urls import path

from . import views


app_name = "a10app"
urlpatterns = [
    path("", views.main_page, name="main_page"),
    path("logout", views.logout),
    path("report", views.ReportFormView.as_view(), name='report'),
    path('redirect-to-report/', views.redirect_to_report, name='redirect_to_report'),
    # path("welcome", views.isAdmin)
    path("listreports", views.report_list, name="list_reports"),
    path("<int:report_id>/view_report/", views.view_report, name="view_report"),
]