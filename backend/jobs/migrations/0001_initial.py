# Generated by Django 4.2.17 on 2024-12-22 03:55

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Job',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=255)),
                ('company_name', models.CharField(max_length=255)),
                ('company_profile_url', models.URLField(blank=True, null=True)),
                ('location', models.CharField(blank=True, max_length=255, null=True)),
                ('posted_date', models.DateField(blank=True, null=True)),
                ('pay_details', models.CharField(blank=True, max_length=255, null=True)),
                ('employment_details', models.TextField(blank=True, null=True)),
                ('skills', models.TextField(blank=True, null=True)),
                ('job_description', models.TextField(blank=True, null=True)),
                ('details_url', models.URLField(blank=True, null=True)),
            ],
        ),
    ]
