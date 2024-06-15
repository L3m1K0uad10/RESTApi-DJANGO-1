import json

from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from django.conf import settings
from django.contrib.auth import get_user_model
from django.forms.models import model_to_dict

from Professionals.models import Professional
from Transactions.models import Transaction

User = get_user_model()

@csrf_exempt
def transaction_view(request, pk = None, user_id = None, professional_id = None, *args, **kwargs):
    
    if request.method == "POST":
        try:
            data = json.loads(request.body.decode("utf-8"))
            
            user_id = data.get("user")
            professional_id = data.get("professional")
            amount = data.get("amount")
            timestamp = data.get("timestamp")
            currency = data.get("currency")

            if user_id is None or professional_id is None or amount is None:
                return JsonResponse({"error": "All fields are required"}, status = 400)
            
            user = User.objects.get(id = user_id)        
            professional = Professional.objects.get(id = professional_id)

            if currency is None:
                currency = "USD"

            transaction = Transaction(
                user = user,
                professional = professional,
                amount = amount,
                timestamp = timestamp,
                currency = currency
            )
            transaction.save()

            data = model_to_dict(transaction)
            return JsonResponse(data, safe = False, status = 201)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
        except User.DoesNotExist:
            return JsonResponse({"error": "User not found"}, status=404)
        except Professional.DoesNotExist:
            return JsonResponse({"error": "Professional not found"}, status=404)
        except Transaction.DoesNotExist:
            return JsonResponse({"error": "Transaction not found"}, status=404)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    if request.method == "GET":
        if pk is not None:
            try:
                transaction = Transaction.objects.get(id = pk) 
                data = model_to_dict(transaction)
                return JsonResponse(data, safe = False)
            except Transaction.DoesNotExist:
                return JsonResponse({"error": "Transaction not found"}, status=404)
            except:
                return JsonResponse({"error": "Transaction not found"}, status=404)
             
        if user_id is not None:
            try:
                transactions = Transaction.objects.filter(user_id=user_id)
                data = []
                for transaction in transactions:
                    transaction_data = model_to_dict(transaction)
                    data.append(transaction_data)
                return JsonResponse(data, safe=False)
            except Transaction.DoesNotExist:
                return JsonResponse({"error": "Transaction not found"}, status=404)
            except:
                return JsonResponse({"error": "Transaction not found"}, status=404)

        if professional_id is not None:
            try:
                transactions = Transaction.objects.filter(professional_id=professional_id)
                data = []
                for transaction in transactions:
                    transaction_data = model_to_dict(transaction)
                    data.append(transaction_data)
                return JsonResponse(data, safe=False)
            except Transaction.DoesNotExist:
                return JsonResponse({"error": "Transaction not found"}, status=404)
            except:
                return JsonResponse({"error": "Transaction not found"}, status=404)

        transactions = Transaction.objects.all()
        data = []
        for transaction in transactions:
            transaction_data = model_to_dict(transaction)
            data.append(transaction_data)
        return JsonResponse(data, safe = False)

    return JsonResponse({"error": "Method not allowed"}, status=405)