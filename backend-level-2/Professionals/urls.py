from django.urls import path 
from .views import professional_view, profile_view

urlpatterns = [
    path('', professional_view, name = "professional_list"),
    path('<int:pk>/', professional_view, name = "professional_detail"),
    path('create/', professional_view, name = "professional_create"),
    path('update/<int:pk>/', professional_view, name = "professional_update"),
    path('delete/<int:pk>/', professional_view, name = "professional_delete"),
    path('profile/create/', profile_view, name = "profile_create"),
    path('profile/<int:pk>/', profile_view, name = "profile_detail"),
    path('profile/update/<int:pk>/', profile_view, name = "profile_update"),
]