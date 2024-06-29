from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .models import Domain, Service
from .serializers import DomainSerializer, ServiceSerializer


@api_view(['GET', 'POST', 'PUT', 'DELETE']) 
def domain_view(request, pk = None, *args, **kwargs):
    
    if request.method == "POST":
        serializer = DomainSerializer(data = request.data)
        if serializer.is_valid():
            instance = serializer.save()
            serializer_response = DomainSerializer(instance)
            data = serializer_response.data
            return Response(data, status = status.HTTP_201_CREATED)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
            

    if request.method == "GET":
        if pk is not None:
            try:
                domain = Domain.objects.get(id = pk) 
                serializer = DomainSerializer(domain)
                return Response(serializer.data)
            except Domain.DoesNotExist:
                return Response({"detail": "Domain not found"}, status=status.HTTP_404_NOT_FOUND)
        
        queryset = Domain.objects.all()
        serializer = DomainSerializer(queryset, many = True)
        data = serializer.data
        return Response(data)
    
    if request.method == "PUT":
        if pk is not None:
            try:
                domain = Domain.objects.get(pk = pk)
                serializer = DomainSerializer(domain, data=request.data, partial = True) 
                if serializer.is_valid():
                    instance = serializer.save()
                    response_serializer = DomainSerializer(instance)
                    data = response_serializer.data
                    return Response(data, status = status.HTTP_200_OK)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            except Domain.DoesNotExist:
                return Response({"detail": "Domain not found"}, status=status.HTTP_404_NOT_FOUND)
            
    if request.method == "DELETE":
        instance = get_object_or_404(Domain, pk=pk)
        instance.delete()
        return Response(status = status.HTTP_204_NO_CONTENT)

    return Response({"error": "Method not allowed"}, status = status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(['GET', 'POST', 'PUT', 'DELETE']) 
def service_view(request, pk = None, *args, **kwargs):
    
    if request.method == "POST":
        serializer = ServiceSerializer(data = request.data)
        if serializer.is_valid():
            instance = serializer.save()
            serializer_response = ServiceSerializer(instance)
            data = serializer_response.data
            return Response(data, status = status.HTTP_201_CREATED)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
             
    if request.method == "GET":
        if pk is not None:
            try:
                service = Service.objects.get(id = pk) 
                serializer = ServiceSerializer(service)
                return Response(serializer.data)
            except Service.DoesNotExist:
                return Response({"detail": "Service not found"}, status=status.HTTP_404_NOT_FOUND)
        
        queryset = Service.objects.all()
        serializer = ServiceSerializer(queryset, many = True)
        data = serializer.data
        return Response(data)

    if request.method == "PUT":
        if pk is not None:
            try:
                service = Service.objects.get(pk = pk)
                serializer = ServiceSerializer(service, data=request.data, partial = True) 
                if serializer.is_valid():
                    instance = serializer.save()
                    response_serializer = ServiceSerializer(instance)
                    data = response_serializer.data
                    return Response(data, status = status.HTTP_200_OK)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            except Service.DoesNotExist:
                return Response({"detail": "Service not found"}, status=status.HTTP_404_NOT_FOUND)

    if request.method == "DELETE":
        instance = get_object_or_404(Service, pk=pk)
        instance.delete()
        return Response(status = status.HTTP_204_NO_CONTENT)

    return Response({"error": "Method not allowed"}, status = status.HTTP_405_METHOD_NOT_ALLOWED)