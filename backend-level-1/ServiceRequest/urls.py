from django.urls import path

from .views import service_request_view



urlpatterns = [
    path("create/", service_request_view, name = "service_request_create"),
    path("", service_request_view, name = "service_request_list"),
    path("<int:pk>/", service_request_view, name = "service_request_detail"),
    path("update/<int:pk>/", service_request_view, name = "service_request_update"),
    path("delete/<int:pk>/", service_request_view, name = "service_request_delete"),
]