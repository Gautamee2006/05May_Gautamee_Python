from rest_framework.views import APIView
from rest_framework import generics, mixins, status
from rest_framework.response import Response
from django.http import Http404
from .models import Restaurant
from .serializers import RestaurantSerializer


# ==============================================================================
# Task 5 (Part 1): Restaurant CRUD API using DRF's APIView Class
# ==============================================================================

class RestaurantListCreateAPIView(APIView):
    """
    APIView for listing all restaurants (GET) and creating a new restaurant (POST).
    """

    def get(self, request):
        restaurants = Restaurant.objects.all()
        serializer = RestaurantSerializer(restaurants, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = RestaurantSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RestaurantDetailAPIView(APIView):
    """
    APIView for retrieving (GET), updating (PUT/PATCH), and deleting (DELETE) a restaurant by ID.
    """

    def get_object(self, pk):
        try:
            return Restaurant.objects.get(pk=pk)
        except Restaurant.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        restaurant = self.get_object(pk)
        serializer = RestaurantSerializer(restaurant)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        restaurant = self.get_object(pk)
        serializer = RestaurantSerializer(restaurant, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        restaurant = self.get_object(pk)
        serializer = RestaurantSerializer(restaurant, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        restaurant = self.get_object(pk)
        restaurant.delete()
        return Response({"message": "Restaurant deleted successfully"}, status=status.HTTP_200_OK)


# ==============================================================================
# Task 5 (Part 2): Refactored Restaurant CRUD API using DRF's GenericAPIView and Mixins
# ==============================================================================

class RestaurantListCreateView(mixins.ListModelMixin,
                               mixins.CreateModelMixin,
                               generics.GenericAPIView):
    """
    Refactored view for listing all restaurants and creating a new restaurant.
    - ListModelMixin: handles GET (list all)
    - CreateModelMixin: handles POST (create new)
    """
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class RestaurantDetailView(mixins.RetrieveModelMixin,
                           mixins.UpdateModelMixin,
                           mixins.DestroyModelMixin,
                           generics.GenericAPIView):
    """
    Refactored view for retrieving, updating, and deleting a restaurant by ID.
    - RetrieveModelMixin: handles GET (retrieve by ID)
    - UpdateModelMixin: handles PUT / PATCH (update by ID)
    - DestroyModelMixin: handles DELETE (delete by ID)
    """
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
