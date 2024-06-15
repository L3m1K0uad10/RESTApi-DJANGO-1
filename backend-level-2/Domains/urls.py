from django.urls import path

from .views import domain_view, service_view


urlpatterns = [
    path("", domain_view, name = "domain_list"),
    path("create/", domain_view, name = "domain_create"),
    path("<int:pk>/", domain_view, name = "domain_detail"),
    path("update/<int:pk>/", domain_view, name = "domain_update"),
    path("delete/<int:pk>/", domain_view, name = "domain_delete"),
    path("services/create/", service_view, name = "service_create"),
    path("services/", service_view, name = "service_list"),
    path("services/<int:pk>/", service_view, name = "service_detail"),
    path("services/update/<int:pk>/", service_view, name = "service_update"),
    path("services/delete/<int:pk>/", service_view, name = "service_delete"),
]