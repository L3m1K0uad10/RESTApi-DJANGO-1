from Professionals.models import Professional 
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .models import Profile, ExperienceBackground
from .serializers import ProfessionalSerializer, ProfileSerializer, ExperienceBackgroundSerializer


@api_view(['GET', 'POST', 'PUT', 'DELETE']) 
def professional_view(request, pk = None, *args, **kwargs):

    if request.method == "POST": # create a professional profile
        serializer = ProfessionalSerializer(data = request.data)
        if serializer.is_valid():
            instance = serializer.save()
            response_serializer = ProfessionalSerializer(instance)
            data = response_serializer.data
            return Response(data, status = status.HTTP_201_CREATED)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)


    if request.method == "GET":
        if pk is not None:
            try:
                professional = Professional.objects.get(pk = pk)
                serializer = ProfessionalSerializer(professional)
                return Response(serializer.data)
            except Professional.DoesNotExist:
                return Response({"detail": "Professional not found"}, status=status.HTTP_404_NOT_FOUND)
        
        queryset = Professional.objects.all()
        serializer = ProfessionalSerializer(queryset, many = True)
        data = serializer.data
        return Response(data)
    
    if request.method == "PUT":
        if pk is not None:
            try:
                professional = Professional.objects.get(pk = pk)
                serializer = ProfessionalSerializer(professional, data=request.data, partial = True) # partial set to true give the leverage to handle partial updates, PATCH method can be used as well for partial update
                if serializer.is_valid():
                    instance = serializer.save()
                    response_serializer = ProfessionalSerializer(instance)
                    data = response_serializer.data
                    return Response(data, status = status.HTTP_200_OK)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            except Professional.DoesNotExist:
                return Response({"detail": "Professional not found"}, status=status.HTTP_404_NOT_FOUND)
            
    if request.method == "DELETE":
        instance = get_object_or_404(Professional, pk=pk)
        instance.delete()
        return Response(status = status.HTTP_204_NO_CONTENT) # once delete the status code is 204 therefore No content, it is the Strict RESTful conventions(common way)

    return Response({"error": "Method not allowed"}, status = status.HTTP_405_METHOD_NOT_ALLOWED)

#@csrf_exempt
@api_view(['GET', 'POST', 'PUT', 'DELETE']) 
def profile_view(request, pk = None, *args, **kwargs):

    if request.method == "POST":
        serializer = ProfileSerializer(data = request.data)
        if serializer.is_valid():
            instance = serializer.save()
            response_serializer = ProfileSerializer(instance)
            data = response_serializer.data
            return Response(data, status = status.HTTP_201_CREATED)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
        
    if request.method == "GET":
        if pk is not None:
            try:
                profile = Profile.objects.get(pk = pk)
                serializer = ProfileSerializer(profile)
                return Response(serializer.data)
            except Profile.DoesNotExist:
                return Response({"detail": "Profile not found"}, status = status.HTTP_404_NOT_FOUND)
            
    if request.method == "PUT":
        if pk is not None:
            try:
                profile = Profile.objects.get(pk = pk)
                serializer = ProfileSerializer(profile, data=request.data, partial = True) # partial set to true give the leverage to handle partial updates, PATCH method can be used as well for partial update
                if serializer.is_valid():
                    instance = serializer.save()
                    response_serializer = ProfileSerializer(instance)
                    data = response_serializer.data
                    return Response(data, status = status.HTTP_200_OK)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            except Profile.DoesNotExist:
                return Response({"detail": "Profile not found"}, status=status.HTTP_404_NOT_FOUND)

    return Response({"error": "Method not allowed"}, status = status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(['GET', 'POST', 'PUT', 'DELETE'])
def experience_bg_view(request, pk = None, professional_id = None, *args, **kwargs):

    if request.method == "POST":
        serializer = ExperienceBackgroundSerializer(data = request.data)
        if serializer.is_valid():
            instance = serializer.save()
            response_serializer = ExperienceBackgroundSerializer(instance)
            data = response_serializer.data
            return Response(data, status = status.HTTP_201_CREATED)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

    if request.method == "GET":
        if pk is not None:
            try:
                experience_bg = ExperienceBackground.objects.get(pk = pk)
                serializer = ExperienceBackgroundSerializer(experience_bg)
                return Response(serializer.data)
            except ExperienceBackground.DoesNotExist:
                return Response({"detail": "Experience Background not found"}, status=status.HTTP_404_NOT_FOUND)

        if professional_id is not None:
            try:
                professional = Professional.objects.get(id = professional_id)
                profile = Profile.objects.get(professional = professional)
                queryset = profile.experience_backgrounds.all()
                
                serializer = ExperienceBackgroundSerializer(queryset, many = True)
                data = serializer.data
                return Response(data)
            except Professional.DoesNotExist:
                return Response({"detail": "Professional not found"}, status=status.HTTP_404_NOT_FOUND)
            except Profile.DoesNotExist:
                return Response({"detail": "Profile not found"}, status=status.HTTP_404_NOT_FOUND)

    if request.method == "PUT":
        if pk is not None:
            try:
                experience_bg = ExperienceBackground.objects.get(pk = pk)
                serializer = ExperienceBackgroundSerializer(experience_bg, data=request.data, partial = True) # partial set to true give the leverage to handle partial updates, PATCH method can be used as well for partial update
                if serializer.is_valid():
                    instance = serializer.save()
                    response_serializer = ExperienceBackgroundSerializer(instance)
                    data = response_serializer.data
                    return Response(data, status = status.HTTP_200_OK)
                return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
            except ExperienceBackground.DoesNotExist:
                return Response({"detail": "Experience Background not found"}, status = status.HTTP_404_NOT_FOUND)

    if request.method == "DELETE":
        instance = get_object_or_404(ExperienceBackground, pk=pk)
        instance.delete()
        return Response(status = status.HTTP_204_NO_CONTENT)

    return Response({"error": "Method not allowed"}, status = status.HTTP_405_METHOD_NOT_ALLOWED)