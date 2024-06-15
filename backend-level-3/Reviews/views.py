import json

from django.shortcuts import render
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.conf import settings
from django.contrib.auth import get_user_model
from django.forms.models import model_to_dict
from rest_framework.decorators import api_view

from Professionals.models import Professional
from .models import Review

User = get_user_model()

@api_view(['GET', 'POST', 'PUT', 'DELETE'])
def review_view(request, pk = None, *args, **kwargs):
    
    if request.method == "POST":
        try:
            data = json.loads(request.body.decode("utf-8"))
            
            user_id = data.get("user")
            professional_id = data.get("professional")
            rating = data.get("rating")
            comment = data.get("comment")
            timestamp = data.get("timestamp")

            if user_id is None or professional_id is None or rating is None or timestamp is None:
                return JsonResponse({"error": "All fields are required"}, status = 400)
            
            user = User.objects.get(id = user_id)        
            professional = Professional.objects.get(id = professional_id)

            if comment is None:
                comment = ""

            review = Review(
                user = user,
                professional = professional,
                rating = rating,
                comment = comment,
                timestamp = timestamp,
            )
            review.save()

            data = model_to_dict(review)
            return JsonResponse(data, safe = False, status = 201)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
        except User.DoesNotExist:
            return JsonResponse({"error": "User not found"}, status=404)
        except Professional.DoesNotExist:
            return JsonResponse({"error": "Professional not found"}, status=404)
        except Review.DoesNotExist:
            return JsonResponse({"error": "Review not found"}, status=404)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    if request.method == "GET":
        if pk is not None:
            try:
                review = Review.objects.get(id = pk) 
                data = model_to_dict(review)
                return JsonResponse(data, safe = False)
            except Review.DoesNotExist:
                return JsonResponse({"error": "Review not found"}, status=404)
            except:
                return JsonResponse({"error": "Review not found"}, status=404)

        reviews = Review.objects.all()
        data = []
        for review in reviews:
            review_data = model_to_dict(review)
            data.append(review_data)
        return JsonResponse(data, safe = False)
    
    if request.method == "PUT":
        # only the client user can update a specific review
        if pk is not None:
            try: 
                data =  json.loads(request.body.decode("utf-8"))
                review = Review.objects.get(id = pk)

                rating = data.get("rating")
                comment = data.get("comment")
                timestamp = data.get("timestamp")

                if (rating is not None or comment is not None) and timestamp is None:
                    return JsonResponse({"error": "timestamp field can't be none"}, status = 400)

                if rating is not None and rating != review.rating:
                    review.rating = rating
                if comment is not None and comment != review.comment:
                    review.comment = comment 
                
                review.timestamp = timestamp

                review.save()

                data = model_to_dict(review)
                return JsonResponse(data, safe=False, status=200)
            except Review.DoesNotExist:
                return JsonResponse({"error": "Review request not found"}, status=404)
            except Exception as e:
                return JsonResponse({"error": str(e)}, status=500)
            
    if request.method == "DELETE":
        try:
            review = get_object_or_404(Review, id = pk)
            review.delete()
            return JsonResponse({"message": "review deleted successfully"}, status = 200)
        except Exception as e:
                return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Method not allowed"}, status=405)