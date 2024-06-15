import json

from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth import login, logout, authenticate
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import get_user_model


User = get_user_model()

@csrf_exempt
def user_view(request, pk = None, *args, **kwargs):

    if request.method == "POST": 
        try:
            data = json.loads(request.body.decode("utf-8"))

            action = data.get("action")

            if action == "register":
                # Register a user
                username = data.get("username")
                email = data.get("email")
                password = data.get("password")

                if not username or not email or not password:
                    return JsonResponse({"error": "username, email, and password are required"}, status=400)

                user = User.objects.create_user(username=username, email=email, password=password)
                user.save()

                return JsonResponse({"message": "User registered successfully"}, status=201)
            
            elif action == "login":
                # Login a user
                email = data.get("email")
                password = data.get("password")

                if not email or not password:
                    return JsonResponse({"error": "email and password are required"}, status=400)

                user = authenticate(request, email=email, password=password) #Use authenticate() to verify a set of credentials. It takes credentials as keyword arguments, username and password for the default case

                if user is not None:
                    login(request, user)
                    return JsonResponse({"message": "User logged in successfully"}, status=200)
                else:
                    return JsonResponse({"error": "Invalid credentials"}, status=400)
            
            elif action == "logout":
                logout(request)
                return JsonResponse({"message": "User logged out successfully"}, status=200)
            
            return JsonResponse({"error": "Invalid action"}, status=400)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
        except User.DoesNotExist:
            return JsonResponse({"error": "User not found"}, status=404)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    if request.method == "GET":
        if pk is not None:
            # Get detail of a user
            try:
                user = User.objects.get(id = pk)
                data = {
                    "id": user.id,
                    "username": user.username,
                    "email": user.email,
                    "usertype": user.usertype,
                    "location": user.location,
                }
                return JsonResponse(data, safe = False)
            except User.DoesNotExist:
                return JsonResponse({"error": "User not found"}, status=404)
            except Exception as e:
                return JsonResponse({"error": str(e)}, status=500)

        # List all users
        users = User.objects.all()
        data = []
        for user in users:
            data.append({
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "usertype": user.usertype,
                "location": user.location,
            })
        return JsonResponse(data, safe=False)
 

    if request.method == "PUT":
        if pk is not None:
            try:
                data = json.loads(request.body.decode("utf-8"))

                user = User.objects.get(id = pk)

                username = data.get("username")
                email = data.get("email")
                password = data.get("password")
                usertype = data.get("usertype")
                location = data.get("location")

                if username:
                    user.username = username
                if email:
                    user.email = email
                if password:
                    user.set_password(password) # changing the password we use set_password("new_password")
                if usertype:
                    user.usertype = usertype
                if location:
                    user.location = location

                user.save()
                return JsonResponse({"message": "User updated successfully"}, status=200)
            except json.JSONDecodeError:
                return JsonResponse({"error": "Invalid JSON"}, status=400) 
            except User.DoesNotExist:
                return JsonResponse({"error": "User not found"}, status=404)
        if pk is None:
            return JsonResponse({"error": "User ID is required for updating"}, status=400)

    if request.method == "DELETE":
        if pk is None:
            return JsonResponse({"error": "User ID is required for deletion"}, status=400)
        try:
            user = User.objects.get(id = pk)
            user.delete()
            return JsonResponse({"message": "User deleted successfully"}, status=200)
        except User.DoesNotExist:
            return JsonResponse({"error": "User not found"}, status=404) 

    return JsonResponse({"error": "Unsupported request method"}, status=405) 
    