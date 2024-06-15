from django.urls import path 

from .views import transaction_view


urlpatterns = [
    path("create/", transaction_view, name = "transaction_create"),
    path("", transaction_view, name = "transaction_list"),
    path("<int:pk>/", transaction_view, name = "transaction_detail"),
    path("user/<int:user_id>/", transaction_view, name = "transaction_user_detail"),
    path("professional/<int:professional_id>/", transaction_view, name = "transaction_professional_detail"),
]