from django.urls import path
from .views import JobList, JobDetail

urlpatterns = [
    path('jobs/', JobList.as_view(), name='job-list'),
    path('jobs/<uuid:id>/', JobDetail.as_view(), name='job-detail'),
]
