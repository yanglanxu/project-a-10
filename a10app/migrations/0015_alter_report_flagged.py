# Generated by Django 4.2.10 on 2024-04-10 16:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('a10app', '0014_report_flagged'),
    ]

    operations = [
        migrations.AlterField(
            model_name='report',
            name='flagged',
            field=models.IntegerField(default=0),
        ),
    ]
