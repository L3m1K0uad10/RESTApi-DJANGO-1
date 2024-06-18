from django.urls import path

from .views import message_view

urlpatterns = [
    path("", message_view, name = "message_list"),
    path("create/", message_view, name = "message_create"),
    path("<int:pk>/", message_view, name = "message_detail"),
    path("inbox/<int:receiver_id>/", message_view, name = "message_by_receiver"),
    path("sent/<int:sender_id>/", message_view, name = "message_by_sender"),
    path("delete/<int:pk>/", message_view, name = "message_delete"),
]