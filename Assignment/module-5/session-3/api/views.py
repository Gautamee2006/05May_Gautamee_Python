from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination
from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from .models import Restaurant
from .serializers import RestaurantSerializer

class StandardPageNumberPagination(PageNumberPagination):
    page_size = 3

class RestaurantViewSet(viewsets.ModelViewSet):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer
    pagination_class = LimitOffsetPagination
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['cuisine']
    ordering_fields = ['name', 'cuisine']
