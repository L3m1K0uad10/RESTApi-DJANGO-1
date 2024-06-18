from django.urls import path

from .views import user_view


urlpatterns = [
    path('register/', user_view, name = "user_register"),
    path('login/', user_view, name = 'user_login'),
    path('logout/', user_view, name = 'user_logout'),
    path('', user_view, name = 'user_list'),
    path('<int:pk>/', user_view, name = 'user_detail'),
    path('update/<int:pk>/', user_view, name = 'user_update'),
    path('delete/<int:pk>/', user_view, name = 'user_update'),
]