from django.urls import path

from . import views


app_name = "a10app"
urlpatterns = [
    path("", views.index),
    path("logout", views.logout),
    path("submit", views.submit),
    path("report", views.ReportFormView.as_view()),
    # path("welcome", views.isAdmin)
]