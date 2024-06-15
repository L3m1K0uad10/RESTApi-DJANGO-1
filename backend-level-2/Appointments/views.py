import json

from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from django.conf import settings
from django.contrib.auth import get_user_model
from django.forms.models import model_to_dict

from Professionals.models import Professional
from ServiceRequest.models import ServiceRequest
from Appointments.models import Appointment


User = get_user_model()

@csrf_exempt
def appointment_view(request, pk = None, *args, **kwargs):
    
    if request.method == "POST":
        try:
            data = json.loads(request.body.decode("utf-8"))
            
            professional_id = data.get("professional")
            user_id = data.get("user")
            service_request_id = data.get("service_request")
            date = data.get("date")
            status = data.get("status")

            if professional_id is None or user_id is None or service_request_id is None:
                return JsonResponse({"error": "All fields are required"}, status = 400)
            
            professional = Professional.objects.get(id = professional_id)
            user = User.objects.get(id = user_id)
            service_request = ServiceRequest.objects.get(id = service_request_id)

            if status is None:         
                appointment = Appointment(
                    professional = professional,
                    user = user,
                    service_request = service_request,
                    date = date,
                )
                appointment.save()

                data = model_to_dict(appointment)
            elif status is not None:
                appointment = Appointment(
                    professional = professional,
                    user = user,
                    service_request = service_request,
                    date = date,
                    status = status,
                )    
                appointment.save()

                data = model_to_dict(appointment)
            return JsonResponse(data, safe = False, status = 201)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
        except User.DoesNotExist:
            return JsonResponse({"error": "User not found"}, status=404)
        except Professional.DoesNotExist:
            return JsonResponse({"error": "Professional not found"}, status=404)
        except ServiceRequest.DoesNotExist:
            return JsonResponse({"error": "Service Request not found"}, status=404)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    if request.method == "GET":
        if pk is not None:
            try:
                appointment = Appointment.objects.get(id = pk) 
                data = model_to_dict(appointment)
                return JsonResponse(data, safe = False)
            except:
                return JsonResponse({"error": "Appointment not found"}, status=404) 

        appointments = Appointment.objects.all()
        data = []
        for appointment in appointments:
            appointment_data = model_to_dict(appointment)
            data.append(appointment_data)
        return JsonResponse(data, safe = False)
    
    if request.method == "PUT":
        if pk is not None:
            try:
                data = json.loads(request.body.decode("utf-8"))

                appointment = Appointment.objects.get(id = pk) 

                professional_id = data.get("professional")
                user_id = data.get("user")
                service_request_id = data.get("service_request")
                date = data.get("date")
                status = data.get("status")

                if professional_id is None or user_id is None or service_request_id is None:
                    return JsonResponse({"error": "All fields are required"}, status = 400)

                if service_request_id != appointment.service_request.id:
                    return JsonResponse({"error": "service request can't be changed for an appointment, delete the appointment and replace it"})

                appointment.professional = Professional.objects.get(id = professional_id)
                appointment.user = User.objects.get(id = user_id)

                if date != appointment.date:
                    appointment.date = date 
                
                if status is not None and status != appointment.status:
                    appointment.status = status

                    appointment.save()

                    data = model_to_dict(appointment)
                else:
                    appointment.save()

                    data = model_to_dict(appointment)
                return JsonResponse(data, safe = False, status = 200)
            except json.JSONDecodeError:
                return JsonResponse({"error": "Invalid JSON"}, status=400)
            except User.DoesNotExist:
                return JsonResponse({"error": "User not found"}, status=404)
            except Professional.DoesNotExist:
                return JsonResponse({"error": "Professional not found"}, status=404)
            except ServiceRequest.DoesNotExist:
                return JsonResponse({"error": "Service Request not found"}, status=404)
            except Exception as e:
                return JsonResponse({"error": str(e)}, status=500) 
            
    if request.method == "DELETE":
        obj = get_object_or_404(Appointment, id = pk)
        obj.delete()

        return JsonResponse({"message": "appointment resource deleted successfully"}, status = 200)

    return JsonResponse({"error": "Method not allowed"}, status=405)