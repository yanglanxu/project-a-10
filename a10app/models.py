from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Report(models.Model):
    title = models.TextField(blank=True, max_length=500)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    text = models.TextField(blank=True, max_length=2000)
    urgency = models.IntegerField(default=1)
    reviewed = models.BooleanField(default=False)

class ReportFile(models.Model):
    file = models.FileField(upload_to="media/")
    content_type = models.CharField(null=True, blank=True, max_length=100)
    report = models.ForeignKey(Report, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        self.content_type = self.file.file.content_type
        super().save(*args, **kwargs)
    

