import json

from django.shortcuts import render
from django.http import JsonResponse
from Professionals.models import Professional 
from django.conf import settings
from django.contrib.auth import get_user_model
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from django.forms.models import model_to_dict # use to convert a model instance to dict

from Domains.models import Domain
from .models import Profile, ExperienceBackground


# Get the custom user model
User = get_user_model()

# csrf is required for POST, PUT, DELETE Methods that why if i remove the @csrf_exempt there is error
# to protect cross-site request forgery 
# if i create separately the views for each Method the one that handle the GET will work without @csrf_exempt
@csrf_exempt 
def professional_view(request, pk=None, *args, **kwargs):

    if request.method == "POST": # create a professional profile
        try:
            data = json.loads(request.body.decode("utf-8"))

            user_id = data.get("user")
            domain_id = data.get("domain")
            photo = data.get("photo")
            availability = data.get("availability")
            rating = data.get("rating")

            if not all([user_id, domain_id, photo, availability is not None, rating is not None]):
                return JsonResponse({"error": "All fields are required"}, status=400)
            
            user = User.objects.get(id = user_id)
            domain = Domain.objects.get(id = domain_id)

            professional = Professional(
                user = user,
                domain = domain,
                photo = photo,
                availability = availability,
                rating = rating
            )
            professional.save()

            data = model_to_dict(professional)
            return JsonResponse(data, safe=False, status=201)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
        except User.DoesNotExist:
            return JsonResponse({"error": "User not found"}, status=404)
        except Domain.DoesNotExist:
            return JsonResponse({"error": "Domain not found"}, status=404)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    if request.method == "GET":
        if pk is None:
            try:
                decoded_data = request.body.decode("utf-8") # django receives the request data in bytes type so we need to decode it
                data_dict = json.loads(decoded_data)
                pk = data_dict["id"]
            except (json.JSONDecodeError, KeyError, TypeError):
                pk = None

        if pk is not None:
            # Handling the detail view for a professional using URL parameter
            try:
                professional = Professional.objects.get(id=pk)
                data = model_to_dict(professional)
                return JsonResponse(data, safe=False)
            except Professional.DoesNotExist:
                return JsonResponse({"error": "Professional not found"}, status=404)
        
        # Listing all professionals
        professionals = Professional.objects.all()
        data = []
        for professional in professionals:
            professional_data = model_to_dict(professional)  # same as the previous method we used
            # we can add to it some fields: that specify the exact fields to respond with in other to be more specific
                #data = model_to_dict(model_data, fields=['id', 'user', 'domain', 'photo', 'availability', 'rating'])
            data.append(professional_data)

        return JsonResponse(data, safe=False)
    
    if request.method == "PUT":
        if pk is None:
            try:
                decoded_data = request.body.decode("utf-8")
                data_dict = json.loads(decoded_data)
                pk = data_dict["id"]
            except (json.JSONDecodeError, KeyError, TypeError):
                pk = None
        
        if pk is not None:
            try:
                data = json.loads(request.body.decode("utf-8"))

                professional = Professional.objects.get(id = pk)

                user_id = data.get("user")
                domain_id = data.get("domain")
                photo = data.get("photo")
                availability = data.get("availability")
                rating = data.get("rating")

                if user_id is not None:
                    professional.user = User.objects.get(id = user_id)
                if domain_id is not None:
                    professional.domain = Domain.objects.get(id = domain_id)
                if photo is not None:
                    professional.photo = photo 
                if availability is not None:
                    professional.availability = availability 
                if rating is not None:
                    professional.rating = rating 

                professional.save()

                data = model_to_dict(professional)
                return JsonResponse(data, safe=False, status=200)
            except Professional.DoesNotExist:
                return JsonResponse({"error": "Professional not found"}, status=404)
            except json.JSONDecodeError:
                return JsonResponse({"error": "Invalid JSON"}, status=400)
            except User.DoesNotExist:
                return JsonResponse({"error": "User not found"}, status=404)
            except Domain.DoesNotExist:
                return JsonResponse({"error": "Domain not found"}, status=404)
            except Exception as e:
                return JsonResponse({"error": str(e)}, status=500)

    if request.method == "DELETE":
        obj = get_object_or_404(Professional, id = pk)
        obj.delete()

        return JsonResponse({"message": "professional resource deleted successfully"}, status = 200)

    return JsonResponse({"error": "Unsupported request method"}, status=405)


@csrf_exempt
def profile_view(request, pk = None, *args, **kwargs):

    if request.method == "POST":
        try:
            data = json.loads(request.body.decode("utf-8"))

            print(data)

            professional_id = data.get("professional")
            experience_bg = data.get("experience_bg")
            about = data.get("about")
            title = data.get("title")
            year_of_experience = data.get("year_of_experience")

            if professional_id is None or experience_bg is None or about is None or title is None or year_of_experience is None:
                return JsonResponse({"error": "All fields are required"}, status=400) 
            
            professional = Professional.objects.get(id = professional_id)
            experience_bg = ExperienceBackground.objects.get(id = experience_bg)

            profile = Profile(
                professional = professional,
                experience_bg = experience_bg,
                about = about,
                title = title,
                year_of_experience = year_of_experience,
            )
            profile.save()

            data = model_to_dict(profile)
            return JsonResponse(data, safe = True, status = 201)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
        except Professional.DoesNotExist:
            return JsonResponse({"error": "Professional not found"}, status=404)
        except ExperienceBackground.DoesNotExist:
            return JsonResponse({"error": "Experience background not found"}, status=404)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
        
    if request.method == "GET":
        if pk is not None:
            try:
                profile = Profile.objects.get(id = pk)

                data = model_to_dict(profile)
                return JsonResponse(data, safe = False) # if the data is not a dictionary set safe to False
            except Profile.DoesNotExist:
                return JsonResponse({"error": "Profile not found"}, status=404)
            
    if request.method == "PUT":
        if pk is not None:
            try:
                data = json.loads(request.body.decode("utf-8"))

                profile = Profile.objects.get(id = pk)

                professional_id = data.get("professional")
                experience_bg_id = data.get("experience_bg")
                about = data.get("about")
                title = data.get("title")
                year_of_experience = data.get("year_of_experience")

                if professional_id is not None:
                    professional = Professional.objects.get(id = professional_id)
                    #print(profile.professional.id)
                    if professional_id != profile.professional.id:
                        return JsonResponse({"error": "Profile professional id can't be changed"})  
                    else:
                        profile.professional = professional                  
                if experience_bg_id is not None:
                    profile.experience_bg = ExperienceBackground.objects.get(id = experience_bg_id)
                if about is not None:
                    profile.about = about 
                if title is not None:
                    profile.title = title 
                if year_of_experience is not None:
                    profile.year_of_experience = year_of_experience

                profile.save()

                data = model_to_dict(profile)
                return JsonResponse(data, safe=False, status=200)
            except Professional.DoesNotExist:
                return JsonResponse({"error": "Professional not found"}, status=404)
            except json.JSONDecodeError:
                return JsonResponse({"error": "Invalid JSON"}, status=400)
            except ExperienceBackground.DoesNotExist:
                return JsonResponse({"error": "Experience background not found"}, status=404)
            except Exception as e:
                return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Unsupported request method"}, status=405)