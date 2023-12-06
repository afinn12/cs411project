from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import get_roadtrip_serializer
from .locations import locations_file

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
