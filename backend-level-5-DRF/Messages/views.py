from rest_framework import generics

from .models import Message
from .serializers import MessageSerializer


# Message views
class MessageListCreateAPIView(generics.ListCreateAPIView):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer

class MessageDetailAPIView(generics.RetrieveAPIView):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    lookup_field = "pk"

class MessageListAPIView(generics.ListAPIView):
    serializer_class = MessageSerializer

    def get_queryset(self):
        if "sender_id" in self.kwargs:
            sender_id = self.kwargs["sender_id"]
            return Message.objects.filter(sender_id = sender_id)
        if "receiver_id" in self.kwargs:
            receiver_id = self.kwargs["receiver_id"]
            return Message.objects.filter(receiver_id = receiver_id)
        
class MessageDestroyAPIView(generics.DestroyAPIView):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    lookup_field = "pk"

