from core.models import Venue, User
from core.serializer import VenueSerializer
from django.shortcuts import render
from django.views.generic import ListView
from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
# Create your views here.


@api_view()
def health(request):
    return Response({'Status': 200})


class VenueViewSet(viewsets.ModelViewSet):
    queryset = Venue.objects.all()
    serializer_class = VenueSerializer


class UserViewSet(ListView):
    context_object_name = 'users'
    template_name = 'users.html'
    model = User