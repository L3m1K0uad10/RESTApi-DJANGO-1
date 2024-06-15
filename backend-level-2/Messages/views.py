import json

from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from django.conf import settings
from django.contrib.auth import get_user_model
from django.forms.models import model_to_dict

from .models import Message

User = get_user_model()

@csrf_exempt
def message_view(request, pk = None, receiver_id = None, sender_id = None, *args, **kwargs):
    
    if request.method == "POST":
        try:
            data = json.loads(request.body.decode("utf-8"))
            
            sender_id = data.get("sender")
            receiver_id = data.get("receiver")
            content = data.get("content")
            timestamp = data.get("timestamp")

            if sender_id is None or receiver_id is None or content is None or timestamp is None:
                return JsonResponse({"error": "All fields are required"}, status = 400)
            
            sender = User.objects.get(id = sender_id)        
            receiver = User.objects.get(id = receiver_id)

            message = Message(
                sender = sender,
                receiver = receiver,
                content = content,
                timestamp = timestamp,
            )
            message.save()

            data = model_to_dict(message)
            return JsonResponse(data, safe = False, status = 201)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
        except User.DoesNotExist:
            return JsonResponse({"error": "User not found"}, status=404)
        except Message.DoesNotExist:
            return JsonResponse({"error": "Message not found"}, status=404)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    if request.method == "GET":
        if pk is not None:
            try:
                message = Message.objects.get(id = pk) 
                data = model_to_dict(message)
                return JsonResponse(data, safe = False)
            except Message.DoesNotExist:
                return JsonResponse({"error": "Review not found"}, status=404)
            except:
                return JsonResponse({"error": "Review not found"}, status=404)

        if sender_id is not None:
            try:
                messages = Message.objects.filter(sender_id = sender_id)
                data = []
                for message in messages:
                    message_data = model_to_dict(message)
                    data.append(message_data)
                return JsonResponse(data, safe = False)
            except Message.DoesNotExist:
                return JsonResponse({"error": "Message not found"}, status=404)
            except:
                return JsonResponse({"error": "Message not found"}, status=404)

        if receiver_id is not None:
            try:
                messages = Message.objects.filter(receiver_id = receiver_id)
                data = []
                for message in messages:
                    message_data = model_to_dict(message)
                    data.append(message_data)
                return JsonResponse(data, safe = False)
            except Message.DoesNotExist:
                return JsonResponse({"error": "Message not found"}, status=404)
            except:
                return JsonResponse({"error": "Message not found"}, status=404)

        messages = Message.objects.all()
        data = []
        for message in messages:
            message_data = model_to_dict(message)
            data.append(message_data)
        return JsonResponse(data, safe = False)
            
    if request.method == "DELETE":
        try:
            message = get_object_or_404(Message, id = pk)
            message.delete()
            return JsonResponse({"message": "Message deleted successfully"}, status = 200)
        except Exception as e:
                return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Method not allowed"}, status=405)