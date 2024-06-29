from django.contrib.auth import login, logout, authenticate
from django.contrib.auth import get_user_model
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .serializers import UserSerializer, UserRegistrationSerializer


User = get_user_model()

@api_view(['GET', 'POST', 'PUT', 'DELETE'])
def user_view(request, pk = None, *args, **kwargs):

    if request.method == "POST": 
        data = request.data
        action = data.get("action")

        if action == "register":
            serializer = UserRegistrationSerializer(data = data)
            if serializer.is_valid():
                instance = serializer.save()
                return Response({"message": "User registered successfully"}, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
        elif action == "login":
            email = data.get('email')
            password = data.get('password')

            if not email or not password:
                return Response({"error": "Email and password are required"}, status=status.HTTP_400_BAD_REQUEST)

            user = authenticate(request, email = email, password = password)
            if user is not None:
                login(request, user)
                return Response({"message": "User logged in successfully"}, status = status.HTTP_200_OK)
            return Response({"error": "Invalid credentials"}, status = status.HTTP_400_BAD_REQUEST)
            
        elif action == "logout":
            logout(request)
            return Response({"message": "User logged out successfully"}, status=status.HTTP_200_OK)
            
    if request.method == "GET":
        if pk is not None:
            try:
                user = User.objects.get(id = pk)
                serializer = UserSerializer(user)
                return Response(serializer.data)
            except User.DoesNotExist:
                return Response({"error": "User not found"}, status = status.HTTP_404_NOT_FOUND)

        queryset = User.objects.all()
        serializer = UserSerializer(queryset, many = True)
        data = serializer.data
        return Response(data)

    if request.method == "PUT":
        if pk is not None:
            try:
                user = User.objects.get(id = pk)           
                serializer = UserSerializer(user, data = request.data, partial = True)
                if serializer.is_valid():
                    instance = serializer.save()
                    serializer_response = UserSerializer(instance)
                    data = serializer_response.data
                    return Response(data, status = status.HTTP_200_OK)
                return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
            except User.DoesNotExist:
                return Response({"error": "User not found"}, status = status.HTTP_404_NOT_FOUND)

    if request.method == "DELETE":
        try:
            user = User.objects.get(id = pk)
            user.delete()
            return Response(status = status.HTTP_204_NO_CONTENT)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

    return Response({"error": "Method not allowed"}, status = status.HTTP_405_METHOD_NOT_ALLOWED)    