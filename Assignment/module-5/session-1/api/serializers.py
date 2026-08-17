from rest_framework import serializers


class RestaurantSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100)
    cuisine = serializers.CharField(max_length=100)


#Create a basic Django REST Framework Serializer class for a Zomato-style Restaurant object with only two fields: name and cuisine. Use serializers.Serializer.