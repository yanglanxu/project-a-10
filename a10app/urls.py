from django.urls import path

from . import views


app_name = "a10app"
urlpatterns = [
    path("", views.main_page, name="main_page"),
    path("logout", views.logout),
    path("report", views.ReportFormView.as_view(), name='report'),
    # path("welcome", views.isAdmin)
    path("user", views.user_page, name="user_page"),
    path("list_reports", views.report_list, name="list_reports"),
    path("<int:report_id>/view_report/", views.view_report, name="view_report"),
    path("<int:report_id>/review_report/", views.review_report, name="review_report"),
     path('report/<int:report_id>/mark_as_reviewed/', views.mark_report_as_reviewed, name='mark_report_as_reviewed'),
]