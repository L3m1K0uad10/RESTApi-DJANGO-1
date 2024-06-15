from django.urls import path

from .views import review_view


urlpatterns = [
    path("create/", review_view, name = "review_create"),
    path("<int:pk>/", review_view, name = "review_detail"),
    path("update/<int:pk>/", review_view, name = "review_update"),
    path("delete/<int:pk>/", review_view, name = "review_delete"),
]