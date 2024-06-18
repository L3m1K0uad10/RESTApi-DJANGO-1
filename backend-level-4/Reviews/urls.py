from django.urls import path

from .views import review_view


urlpatterns = [
    path("", review_view, name = "review_list"),
    path("create/", review_view, name = "review_create"),
    path("<int:pk>/", review_view, name = "review_detail"),
    path("professional/<int:professional_id>/", review_view, name = "review_professional_detail"),
    path("update/<int:pk>/", review_view, name = "review_update"),
    path("delete/<int:pk>/", review_view, name = "review_delete"),
]