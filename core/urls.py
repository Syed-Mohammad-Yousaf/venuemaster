from django.urls import path
from core.views import views

routes = [
    (r'venues', views.VenueViewSet),
]

urls = [
    path(r'health/', views.health, name='core-health'),
    path('users/', views.UserViewSet.as_view()),
]