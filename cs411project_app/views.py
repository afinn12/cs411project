from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import get_roadtrip_serializer
from .locations import locations_file, googlemaps_key
import json
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

def login(request):
    return render(request, 'login.html')

def logout(request):
    return render(request, 'logout.html')

def home(request):
    return render(request, 'home.html')

def map(request):
    user_info = None
    if request.user.is_authenticated:
        user_info = {
            'username': request.user.username,
            'email': request.user.email,
            # Add other user information as needed
        }
    return render(request, 'map.html', {'user_info': user_info})

@login_required
def test_map(request):
    user_info = None
    if request.user.is_authenticated:
        user_info = {
            'username': request.user.username,
            'email': request.user.email,
            # Add other user information as needed
        }
    return render(request, 'test_map.html', {'user_info': user_info})

class get_roadtrip_APIView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = get_roadtrip_serializer(data=request.data)
        if serializer.is_valid():
            # Call your function with the validated data
            result = locations_file.get_roadtrip(
                serializer.validated_data['origin'],
                serializer.validated_data['destination'],
                serializer.validated_data['is_direct_route'],
                serializer.validated_data['distance_limit'],
                serializer.validated_data['start_date'],
            )
            return Response(result, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class get_google_apikey(APIView):
    def post(self, request, *args, **kwargs):
        return Response(googlemaps_key.googlemaps_key, status=status.HTTP_200_OK)
    

class get_sample_roadtrip_APIView(APIView):
    def post(self, request, *args, **kwargs):
        sample_result = json.load(open('cs411project_app/sample_api_output.json'))
        return Response(sample_result, status=status.HTTP_200_OK)
