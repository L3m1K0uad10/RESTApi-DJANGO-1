from django.urls import path

from .views import appointment_view


urlpatterns = [
    path("create/", appointment_view, name = "appointment_create"),
    path("", appointment_view, name = "appointment_list"),
    path("<int:pk>/", appointment_view, name = "appointment_detail"),
    path("update/<int:pk>/", appointment_view, name = "appointment_update"),
    path("delete/<int:pk>/", appointment_view, name = "appointment_delete"),
]