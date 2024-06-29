from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from Transactions.models import Transaction
from .serializers import TransactionSerializer


@api_view(['GET', 'POST', 'PUT', 'DELETE'])
def transaction_view(request, pk = None, user_id = None, professional_id = None, *args, **kwargs):
    
    if request.method == "POST":
        serializer = TransactionSerializer(data = request.data)
        if serializer.is_valid():
            instance = serializer.save()
            serializer_response = TransactionSerializer(instance)
            data = serializer_response.data 
            return Response(data, status = status.HTTP_201_CREATED)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

    if request.method == "GET":
        if pk is not None:
            try:
                transaction = Transaction.objects.get(id = pk) 
                serializer = TransactionSerializer(transaction)
                return Response(serializer.data)
            except Transaction.DoesNotExist:
                return Response({"error": "Transaction not found"}, status = status.HTTP_404_NOT_FOUND)
             
        if user_id is not None:
            try:
                queryset = Transaction.objects.filter(user_id = user_id)
                serializer = TransactionSerializer(queryset, many = True)
                data = serializer.data
                return Response(data)
            except Transaction.DoesNotExist:
                return Response({"error": "Transaction not found"}, status = status.HTTP_404_NOT_FOUND)

        if professional_id is not None:
            try:
                queryset = Transaction.objects.filter(professional_id = professional_id)
                serializer = TransactionSerializer(queryset, many = True)
                data = serializer.data
                return Response(data)
            except Transaction.DoesNotExist:
                return Response({"error": "Transaction not found"}, status = status.HTTP_404_NOT_FOUND)

        queryset = Transaction.objects.all()
        serializer = TransactionSerializer(queryset, many = True)
        data = serializer.data
        return Response(data)

    return Response({"error": "Method not allowed"}, status = status.HTTP_405_METHOD_NOT_ALLOWED)