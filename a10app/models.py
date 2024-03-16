from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Report(models.Model):
    title = models.TextField(blank=True, max_length=500)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    text = models.TextField(blank=True, max_length=2000)
    urgency = models.IntegerField(default=1)

class ReportFile(models.Model):
    file = models.FileField(upload_to="media/")
    report = models.ForeignKey(Report, on_delete=models.CASCADE)

