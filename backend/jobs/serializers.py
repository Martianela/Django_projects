from rest_framework import serializers
from .models import Job

class JobSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job
        fields = ['id','title', 'company_name', 'company_profile_url', 'location', 
                  'posted_date', 'pay_details', 'employment_details', 'skills', 'job_description']
