from django.db import models
import os

from django.contrib.auth.models import User
from django.dispatch import receiver

# Create your models here.

class Report(models.Model):
    title = models.TextField(blank=True, max_length=500)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    text = models.TextField(blank=True, max_length=2000)
    urgency = models.IntegerField(default=1)
    admin_comments = models.TextField(blank=True, max_length=2000)
    status = models.CharField(default="New", max_length=50)
    location = models.TextField(blank=True, max_length=2000)
    flagged = models.IntegerField(default=0)

class ReportFile(models.Model):
    file = models.FileField(upload_to="media/")
    content_type = models.CharField(null=True, blank=True, max_length=100)
    report = models.ForeignKey(Report, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        self.content_type = self.file.file.content_type
        super().save(*args, **kwargs)

class Comment(models.Model):
    report = models.ForeignKey(Report, related_name='comments', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField(blank=True, max_length=2000)
    created_at = models.DateTimeField(auto_now_add=True)

@receiver(models.signals.post_delete, sender=ReportFile)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    if instance.file:
        instance.file.delete(False)
    

