from rest_framework import generics

from Transactions.models import Transaction
from .serializers import TransactionSerializer


# Transaction views
class TransactionListeCreateAPIView(generics.ListCreateAPIView):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer

class TransactionDetailAPIView(generics.RetrieveAPIView):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    lookup_field = "pk"

class TransactionListAPIView(generics.ListAPIView):
    serializer_class = TransactionSerializer

    def get_queryset(self):
        if "user_id" in self.kwargs:
            user_id = self.kwargs["user_id"]
            return Transaction.objects.filter(user_id = user_id)
        elif "professional_id" in self.kwargs:
            professional_id = self.kwargs["professional_id"]
            return Transaction.objects.filter(professional_id = professional_id)
