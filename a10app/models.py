from django.db import models

# Create your models here.
class Users(models.Model):
    userName = models.CharField(max_length=300, verbose_name='username')
    email = models.CharField(max_length=500, verbose_name='email')
    is_superuser = models.BooleanField()

    def __str__(self):
        return self.userName