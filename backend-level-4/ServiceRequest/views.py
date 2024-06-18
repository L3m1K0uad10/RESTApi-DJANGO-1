from django.shortcuts import get_object_or_404
from .models import ServiceRequest
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .models import ServiceRequest
from .serializers import ServiceRequestSerializer


@api_view(['GET', 'POST', 'PUT', 'DELETE'])
def service_request_view(request, pk = None, *args, **kwargs):

    if request.method == "POST":
        serializer = ServiceRequestSerializer(data = request.data)
        if serializer.is_valid():
            instance = serializer.save()
            serializer_response = ServiceRequestSerializer(instance)
            data = serializer_response.data
            return Response(data, status = status.HTTP_201_CREATED)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

    if request.method == "GET":
        if pk is not None:
            try:
                service_request = ServiceRequest.objects.get(id = pk)
                serializer = ServiceRequestSerializer(service_request)
                return Response(serializer.data)
            except ServiceRequest.DoesNotExist:
                return Response({"detail": "Service Request not found"}, status = status.HTTP_404_NOT_FOUND)
        
        queryset = ServiceRequest.objects.all()
        serializer = ServiceRequestSerializer(queryset, many = True)
        data = serializer.data 
        return Response(data)

    if request.method == "PUT":
        if pk is not None:
            try: 
                service_request = ServiceRequest.objects.get(id = pk)
                serializer = ServiceRequestSerializer(service_request, data = request.data, partial = True)
                if serializer.is_valid():
                    instance = serializer.save()
                    serializer_response = ServiceRequestSerializer(instance)
                    data = serializer_response.data
                    return Response(data, status = status.HTTP_200_OK)
                return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
            except ServiceRequest.DoesNotExist:
                return Response({"detail": "Service Request not found"}, status = status.HTTP_404_NOT_FOUND)
            
    if request.method == "DELETE": # cancelling a service request
        instance = get_object_or_404(ServiceRequest, id = pk)
        instance.delete()
        return Response(status = status.HTTP_204_NO_CONTENT)

    return Response({"error": "Method not allowed"}, status = status.HTTP_405_METHOD_NOT_ALLOWED)