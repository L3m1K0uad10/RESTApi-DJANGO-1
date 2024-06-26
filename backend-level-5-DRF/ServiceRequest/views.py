from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics

from .models import ServiceRequest
from .serializers import ServiceRequestSerializer


# service request views
class ServiceRequestListCreateAPIView(generics.ListCreateAPIView):
    queryset = ServiceRequest.objects.all()
    serializer_class = ServiceRequestSerializer

class ServiceRequestDetailAPIView(generics.RetrieveAPIView):
    queryset = ServiceRequest.objects.all()
    serializer_class = ServiceRequestSerializer
    lookup_field = "pk"

class ServiceRequestUpdateAPIView(generics.UpdateAPIView):
    queryset = ServiceRequest.objects.all()
    serializer_class = ServiceRequestSerializer
    lookup_field = "pk"

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", True)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data = request.data, partial = partial)
        if serializer.is_valid():
            self.perform_update(serializer)
            return Response(serializer.data, status = status.HTTP_200_OK)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
    
class ServiceRequestDestroyAPIView(generics.DestroyAPIView):
    queryset = ServiceRequest.objects.all()
    serializer_class = ServiceRequestSerializer
    lookup_field = "pk"
