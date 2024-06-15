import json

from django.shortcuts import render
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.forms.models import model_to_dict
from rest_framework.decorators import api_view

from .models import Domain, Service


@api_view(['GET', 'POST', 'PUT', 'DELETE']) 
def domain_view(request, pk = None, *args, **kwargs):
    
    if request.method == "POST":
        try:
            data = json.loads(request.body.decode("utf-8"))
            
            domain_name = data.get("domain_name")

            if domain_name is None:
                return JsonResponse({"error": "All fields are required"}, status = 400)
            
            # checking if the domain already exists
            if Domain.objects.filter(domain_name = domain_name).exists():
                return JsonResponse({"error": "Domain already exists"}, status=400)
            
            domain = Domain(domain_name = domain_name)
            domain.save()

            data = model_to_dict(domain)
            return JsonResponse(data, safe = False, status = 201)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    if request.method == "GET":
        if pk is not None:
            try:
                domain = Domain.objects.get(id = pk) 
                data = model_to_dict(domain)
                return JsonResponse(data, safe = False)
            except:
                return JsonResponse({"error": "Domain not found"}, status=404) 

        domains = Domain.objects.all()
        data = []
        for domain in domains:
            domain_data = model_to_dict(domain)
            data.append(domain_data)
        return JsonResponse(data, safe = False)
    
    if request.method == "PUT":
        if pk is not None:
            try:
                data = json.loads(request.body.decode("utf-8"))

                domain = Domain.objects.get(id = pk) 

                domain_name = data.get("domain_name")

                if domain_name is None:
                    return JsonResponse({"error": "domain_name field is required"})

                domain.domain_name = domain_name

                domain.save()

                data = model_to_dict(domain)
                return JsonResponse(data, safe = False, status = 200)
            except Domain.DoesNotExist:
                return JsonResponse({"error": "Domain not found"}, status=404)
            except json.JSONDecodeError:
                return JsonResponse({"error": "Invalid JSON"}, status=400)
            except Exception as e:
                return JsonResponse({"error": str(e)}, status=500) 
            
    if request.method == "DELETE":
        obj = get_object_or_404(Domain, id = pk)
        obj.delete()

        return JsonResponse({"message": "domain resource deleted successfully"}, status = 200)

    return JsonResponse({"error": "Method not allowed"}, status=405)


@api_view(['GET', 'POST', 'PUT', 'DELETE']) 
def service_view(request, pk = None, *args, **kwargs):
    
    if request.method == "POST":
        try:
            data = json.loads(request.body.decode("utf-8"))

            domain_id = data.get("domain")
            service_name = data.get("service_name")

            if domain_id is None or service_name is None:
                return JsonResponse({"error": "All fields are required"}, status = 400)
                
            #checking if the service already exists
            if Service.objects.filter(service_name = service_name).exists():
                return JsonResponse({"error": "Service already exists"}, status=400)
            
            domain = Domain.objects.get(id = domain_id)
                
            service = Service(
                domain = domain,
                service_name = service_name
            )
            service.save()

            data = model_to_dict(service)
            return JsonResponse(data, safe = True, status = 201)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500) 

    if request.method == "GET":
        if pk is not None:
            try:
                service = Service.objects.get(id = pk) 
                data = {
                    "id": service.id,
                    "domain": service.domain.id,
                    "service_name": service.service_name,
                }
                return JsonResponse(data, safe = False, status = 201)
            except:
                return JsonResponse({"error": "Service not found"}, status=404)
        
        services = Service.objects.all()
        data = []
        for service in services:
            service_data = model_to_dict(service)
            data.append(service_data)
        return JsonResponse(data, safe = False, status = 201)

    if request.method == "PUT":
        if pk is not None:
            try:
                data = json.loads(request.body.decode("utf-8"))

                service = Service.objects.get(id = pk)
                
                domain_id = data.get("domain")
                service_name = data.get("service_name")

                if domain_id is None or service_name is None:
                    return JsonResponse({"error": "All fields are required"}, status = 400)

                service.domain.id = domain_id 
                service.service_name = service_name

                service.save()

                data = model_to_dict(service)
                return JsonResponse(data, safe = True, status = 201)
            except Service.DoesNotExist:
                return JsonResponse({"error": "Service not found"}, status=404)
            except json.JSONDecodeError:
                return JsonResponse({"error": "Invalid JSON"}, status=400)
            except Exception as e:
                return JsonResponse({"error": str(e)}, status=500)

    if request.method == "DELETE":
        if pk is not None:
            try:
                obj = get_object_or_404(Service, id = pk)
                obj.delete() 

                return JsonResponse({"message": "service resource deleted successfully"}, status = 200)
            except Exception as e:
                return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Method not allowed"}, status = 405)