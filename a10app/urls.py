from django.urls import path

from . import views


app_name = "a10app"
urlpatterns = [
    path("", views.main_page, name="main_page"),
    path("logout", views.logout),
    path("report", views.ReportFormView.as_view(), name='report'),
    # path("welcome", views.isAdmin)
    path("user", views.user_page, name="user_page"),
    path("<int:report_id>/delete", views.delete, name="delete"),
    path("list_reports", views.report_list, name="list_reports"),
    path("<int:report_id>/view_report/", views.view_report, name="view_report"),
    path('report/<int:report_id>/mark_as_resolved/', views.mark_report_as_resolved, name='mark_report_as_resolved'),
    path('report/<int:report_id>/flag/', views.flag, name='flag_report'),
    path('search/', views.search_reports, name='search_reports')
]