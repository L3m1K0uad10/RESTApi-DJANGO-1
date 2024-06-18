from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .models import Review
from .serializers import ReviewSerializer


@api_view(['GET', 'POST', 'PUT', 'DELETE'])
def review_view(request, pk = None, professional_id = None, *args, **kwargs):
    
    if request.method == "POST":
        serializer = ReviewSerializer(data = request.data)
        if serializer.is_valid():
            instance = serializer.save()
            serializer_response = ReviewSerializer(instance)
            data = serializer_response.data
            return Response(data, status = status.HTTP_201_CREATED)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

    if request.method == "GET":
        if pk is not None:
            try:
                review = Review.objects.get(id = pk) 
                serializer = ReviewSerializer(review)
                return Response(serializer.data)
            except Review.DoesNotExist:
                return Response({"error": "Review not found"}, status = status.HTTP_400_BAD_REQUEST)
            
        if professional_id is not None:
            try:
                queryset = Review.objects.filter(professional_id = professional_id)
                serializer = ReviewSerializer(queryset, many = True)
                data = serializer.data 
                return Response(data)
            except Review.DoesNotExist:
                return Response({"error": "Review not found"}, status = status.HTTP_400_BAD_REQUEST)

        queryset = Review.objects.all()
        serializer = ReviewSerializer(queryset, many = True)
        data = serializer.data
        return Response(data)
    
    if request.method == "PUT":
        # only the client user can update a specific review
        if pk is not None:
            try: 
                review = Review.objects.get(id = pk)
                serializer = ReviewSerializer(review, data = request.data, partial = True)
                if serializer.is_valid():
                    instance = serializer.save()
                    serializer_response = ReviewSerializer(instance)
                    data = serializer_response.data
                    return Response(data, status = status.HTTP_200_OK)
                return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
            except Review.DoesNotExist:
                return Response({"error": "Review not found"}, status = status.HTTP_400_BAD_REQUEST)
            
    if request.method == "DELETE":
        try:
            instance = get_object_or_404(Review, id = pk)
            instance.delete()
            return Response(status = status.HTTP_204_NO_CONTENT)
        except Review.DoesNotExist:
                return Response({"error": "Review not found"}, status = status.HTTP_400_BAD_REQUEST)

    return Response({"error": "Method not allowed"}, status = status.HTTP_405_METHOD_NOT_ALLOWED)