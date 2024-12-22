from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import NotFound
from .models import Job
from .serializers import JobSerializer

class JobList(APIView):
    def get(self, request):
        jobs = Job.objects.all()  # Get all jobs
        serializer = JobSerializer(jobs, many=True)
        return Response(serializer.data)

    def post(self, request):
        # Deserialize the incoming data to a Job object
        serializer = JobSerializer(data=request.data)
        
        # Check if the incoming data is valid
        if serializer.is_valid():
            serializer.save()  # Save the new job entry
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        # If invalid data, return an error response
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class JobDetail(APIView):
    def get(self, request, id):
        try:
            # Fetch the job by its UUID (id)
            job = Job.objects.get(id=id)
           
            serializer = JobSerializer(job)
            # Return the serialized data as response
            return Response(serializer.data)
        except Job.DoesNotExist:
            raise NotFound("Job not found")
