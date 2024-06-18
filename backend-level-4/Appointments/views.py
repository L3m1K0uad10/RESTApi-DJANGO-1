from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .models import Appointment
from .serializers import AppointmentSerializer


@api_view(['GET', 'POST', 'PUT', 'DELETE'])
def appointment_view(request, pk = None, *args, **kwargs):
    
    if request.method == "POST":
        serializer = AppointmentSerializer(data = request.data)
        if serializer.is_valid():
            instance = serializer.save()
            serializer_response = AppointmentSerializer(instance)
            data = serializer_response.data
            return Response(data, status = status.HTTP_201_CREATED)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

    if request.method == "GET":
        if pk is not None:
            try:
                appointment = Appointment.objects.get(id = pk) 
                serializer = AppointmentSerializer(appointment)
                return Response(serializer.data)
            except Appointment.DoesNotExist:
                return Response({"detail": "Appointment not found"}, status = status.HTTP_404_NOT_FOUND)
        
        queryset = Appointment.objects.all()
        serializer = AppointmentSerializer(queryset, many = True)
        data = serializer.data
        return Response(data)
    
    if request.method == "PUT":
        if pk is not None:
            try:
                appointment = Appointment.objects.get(pk = pk)
                serializer = AppointmentSerializer(appointment, data = request.data, partial = True) 
                if serializer.is_valid():
                    instance = serializer.save()
                    response_serializer = AppointmentSerializer(instance)
                    data = response_serializer.data
                    return Response(data, status = status.HTTP_200_OK)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            except Appointment.DoesNotExist:
                return Response({"detail": "Appointment not found"}, status = status.HTTP_404_NOT_FOUND) 
            
    if request.method == "DELETE":
        instance = get_object_or_404(Appointment, pk=pk)
        instance.delete()
        return Response(status = status.HTTP_204_NO_CONTENT)

    return Response({"error": "Method not allowed"}, status = status.HTTP_405_METHOD_NOT_ALLOWED)