# Generated by Django 4.2.10 on 2024-03-16 22:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('a10app', '0005_alter_report_urgency'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='is_superuser',
        ),
    ]
