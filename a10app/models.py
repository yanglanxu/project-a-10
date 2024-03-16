from django.db import models

# Create your models here.
class User(models.Model):
    userName = models.CharField(max_length=300, verbose_name='username')
    email = models.CharField(max_length=500, verbose_name='email')
    is_superuser = models.BooleanField()

    def __str__(self):
        return self.userName

class Report(models.Model):
    title = models.TextField(blank=True, max_length=500)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    text = models.TextField(blank=True, max_length=2000)
    urgency = models.IntegerField(default=1)

class ReportFile(models.Model):
    file = models.FileField(upload_to="media/")
    report = models.ForeignKey(Report, on_delete=models.CASCADE)

