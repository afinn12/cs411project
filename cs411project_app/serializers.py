from rest_framework import serializers

class get_roadtrip_serializer(serializers.Serializer):
    origin = serializers.CharField()
    destination = serializers.CharField()
    is_direct_route = serializers.BooleanField()
    distance_limit = serializers.FloatField()
    start_date = serializers.CharField()