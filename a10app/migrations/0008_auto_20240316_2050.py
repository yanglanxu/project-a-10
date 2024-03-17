# Generated by Django 4.2.10 on 2024-03-17 00:50

from django.db import migrations
from django.contrib.auth.models import Group, Permission

def make_site_admin(apps, schema_editor):
    Group.objects.get_or_create(name="site_admin")


class Migration(migrations.Migration):

    dependencies = [
        ('a10app', '0007_alter_report_user_delete_user'),
    ]

    operations = [migrations.RunPython(make_site_admin)
    ]
