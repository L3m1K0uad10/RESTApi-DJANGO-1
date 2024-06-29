from django.urls import path 
from .views import professional_view, profile_view, experience_bg_view

urlpatterns = [
    path('', professional_view, name = "professional_list"),
    path('<int:pk>/', professional_view, name = "professional_detail"),
    path('create/', professional_view, name = "professional_create"),
    path('update/<int:pk>/', professional_view, name = "professional_update"),
    path('delete/<int:pk>/', professional_view, name = "professional_delete"),
    path('profile/create/', profile_view, name = "profile_create"),
    path('profile/<int:pk>/', profile_view, name = "profile_detail"),
    path('profile/update/<int:pk>/', profile_view, name = "profile_update"),
    path('experiencebackground/create/', experience_bg_view, name = "experience_bg_create"),
    path('experiencebackground/<int:pk>/', experience_bg_view, name = "experience_bg_detail"),
    path('experiencebackground/professional/<int:professional_id>/', experience_bg_view, name = "experience_bg_professional_detail"),
    path('experiencebackground/update/<int:pk>/', experience_bg_view, name = "experience_bg_update"),
    path('experiencebackground/delete/<int:pk>/', experience_bg_view, name = "experience_bg_delete"),
]