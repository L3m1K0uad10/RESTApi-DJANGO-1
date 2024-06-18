from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .models import Message
from .serializers import MessageSerializer


@api_view(['GET', 'POST', 'PUT', 'DELETE'])
def message_view(request, pk = None, receiver_id = None, sender_id = None, *args, **kwargs):
    
    if request.method == "POST":
        serializer = MessageSerializer(data = request.data)
        if serializer.is_valid():
            instance = serializer.save()
            serializer_response = MessageSerializer(instance)
            data = serializer_response.data
            return Response(data, status = status.HTTP_201_CREATED)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

    if request.method == "GET":
        if pk is not None:
            try:
                message = Message.objects.get(id = pk) 
                serializer = MessageSerializer(message)
                return Response(serializer.data)
            except Message.DoesNotExist:
                return Response({"error": "Review not found"}, status = status.HTTP_400_BAD_REQUEST)

        if sender_id is not None:
            try:
                queryset = Message.objects.filter(sender_id = sender_id)
                serializer = MessageSerializer(queryset, many = True)
                data = serializer.data
                return Response(data)
            except Message.DoesNotExist:
                return Response({"error": "Review not found"}, status = status.HTTP_400_BAD_REQUEST)

        if receiver_id is not None:
            try:
                queryset = Message.objects.filter(receiver_id = receiver_id)
                serializer = MessageSerializer(queryset, many = True)
                data = serializer.data
                return Response(data)
            except Message.DoesNotExist:
                return Response({"error": "Review not found"}, status = status.HTTP_400_BAD_REQUEST)

        queryset = Message.objects.all()
        serializer = MessageSerializer(queryset, many = True)
        data = serializer.data
        return Response(data)
            
    if request.method == "DELETE":
        try:
            instance = get_object_or_404(Message, id = pk)
            instance.delete()
            return Response(status = status.HTTP_204_NO_CONTENT)
        except Exception as e:
                return Response({"error": str(e)}, status = status.HTTP_500_INTERNAL_SERVER_ERROR)

    return Response({"error": "Method not allowed"}, status = status.HTTP_405_METHOD_NOT_ALLOWED)