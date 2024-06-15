import json

from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .models import ServiceRequest
from django.conf import settings
from django.contrib.auth import get_user_model
from django.views.decorators.csrf import csrf_exempt

from Professionals.models import Professional
from Domains.models import Domain, Service


# Get the custom user model
User = get_user_model() #This function retrieves the user model that is defined in AUTH_USER_MODEL in your settings.py

# Create your views here.
@csrf_exempt
def service_request_view(request, pk = None, *args, **kwargs):

    if request.method == "POST":
        try:
            data = json.loads(request.body.decode("utf-8"))

            user_id = data.get("user")
            professional_id = data.get("professional")
            category_id = data.get("category")
            service_id = data.get("service")
            description = data.get("description")
            urgency = data.get("urgency")
            status = data.get("status")
            budget = data.get("budget")

            if urgency is None:
                urgency = 'Low'
                
            if status is None:
                status = 'Pending'

            if user_id is None or professional_id is None or category_id is None or service_id is None or budget is None:
                return JsonResponse({"error": "user, professional, category, service and budget fields are required"}, status=400)

            user = User.objects.get(id = user_id)
            professional = Professional.objects.get(id = professional_id)
            category = Domain.objects.get(id = category_id)
            service = Service.objects.get(id = service_id)

            service_request = ServiceRequest(
                user = user,
                professional = professional,
                category = category,
                service = service,
                description = description,
                urgency = urgency,
                status = status,
                budget = budget
            )   
            service_request.save()

            data = {
                "id": service_request.id,
                "professional": service_request.professional.user.username,
                "category": service_request.category.domain_name,
                "service": service_request.service.service_name,
                "description": service_request.description,
                "urgency": service_request.urgency,
                "status": service_request.status,
                "budget": service_request.budget,
            } 
            return JsonResponse(data, safe = True, status = 201)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
        except User.DoesNotExist:
            return JsonResponse({"error": "User not found"}, status=404)
        except Professional.DoesNotExist:
            return JsonResponse({"error": "Professional not found"}, status=404)
        except Domain.DoesNotExist:
            return JsonResponse({"error": "Category not found"}, status=404)
        except Service.DoesNotExist:
            return JsonResponse({"error": "Service not found"}, status=404)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500) 

    if request.method == "GET":
        if pk is not None:
            try:
                service_request = ServiceRequest.objects.get(id = pk)

                data = {
                    "id": service_request.id,
                    "professional": service_request.professional.user.username,
                    "category": service_request.category.domain_name,
                    "service": service_request.service.service_name,
                    "description": service_request.description,
                    "urgency": service_request.urgency,
                    "status": service_request.status,
                    "budget": service_request.budget,
                }
                return JsonResponse(data, safe=False)
            except ServiceRequest.DoesNotExist:
                return JsonResponse({"error": "Service request not found"}, status=404)
        
        service_requests = ServiceRequest.objects.all()
        data = []
        for service_request in service_requests:
            data.append({
                "id": service_request.id,
                "professional": service_request.professional.user.username,
                "category": service_request.category.domain_name,
                "service": service_request.service.service_name,
                "description": service_request.description,
                "urgency": service_request.urgency,
                "status": service_request.status,
                "budget": service_request.budget,
            })
        return JsonResponse(data, safe=False)
    
    if request.method == "PUT":
        #only urgency and status can be updated(urgency by the user and status for data display)
        #why not other fields because there is message possibility between user-professional
        if pk is not None:
            try: 
                data =  json.loads(request.body.decode("utf-8"))
                service_request = ServiceRequest.objects.get(id = pk)

                urgency = data.get("urgency")
                status = data.get("status")

                if urgency is not None:
                    service_request.urgency = urgency
                if status is not None:
                    service_request.status = status 
                
                service_request.save()

                data = {
                    "id": service_request.id,
                    "professional": service_request.professional.user.username,
                    "category": service_request.category.domain_name,
                    "service": service_request.service.service_name,
                    "description": service_request.description,
                    "urgency": service_request.urgency,
                    "status": service_request.status,
                    "budget": service_request.budget,
                }
                return JsonResponse(data, safe=False, status=200)
            except ServiceRequest.DoesNotExist:
                return JsonResponse({"error": "Service request not found"}, status=404)
            except Exception as e:
                return JsonResponse({"error": str(e)}, status=500)
            
    if request.method == "DELETE": # cancelling a service request
        service_request = get_object_or_404(ServiceRequest, id = pk)
        service_request.delete()
        return JsonResponse({"message": "service request deleted successfully"}, status = 200)

    return JsonResponse({"error": "Unsupported request method"}, status=405) 