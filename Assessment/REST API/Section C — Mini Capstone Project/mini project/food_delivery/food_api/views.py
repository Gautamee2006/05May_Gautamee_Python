from rest_framework import viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination

from food_api.models import Category, MenuItem, Order
from food_api.serializers import CategorySerializer, MenuItemSerializer, OrderSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    """
    ModelViewSet for Category resource.
    Supports GET, POST, PUT, PATCH, DELETE.
    """
    queryset = Category.objects.all().order_by('id')
    serializer_class = CategorySerializer
    permission_classes = [AllowAny]


class MenuItemViewSet(viewsets.ModelViewSet):
    """
    ModelViewSet for MenuItem resource.
    Supports GET, POST, PUT, PATCH, DELETE.
    """
    queryset = MenuItem.objects.all().order_by('id')
    serializer_class = MenuItemSerializer
    permission_classes = [AllowAny]


class OrderViewSet(viewsets.ModelViewSet):
    """
    ModelViewSet for Order resource.
    Supports GET, POST, PUT, PATCH, DELETE.
    Requires authentication for POST (creating orders).
    Supports status filtering via query parameter: ?status=pending|confirmed|delivered
    """
    serializer_class = OrderSerializer

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAuthenticated()]
        return [AllowAny()]

    def get_queryset(self):
        queryset = Order.objects.all().order_by('-id')
        status_param = self.request.query_params.get('status', None)
        if status_param:
            queryset = queryset.filter(status=status_param)
        return queryset

    def perform_create(self, serializer):
        serializer.save(customer=self.request.user)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def my_orders(request):
    """
    GET /api/my-orders/
    Protected endpoint returning order history for the authenticated user only.
    """
    orders = Order.objects.filter(customer=request.user).order_by('-id')
    paginator = PageNumberPagination()
    page = paginator.paginate_queryset(orders, request)
    if page is not None:
        serializer = OrderSerializer(page, many=True)
        return paginator.get_paginated_response(serializer.data)
    
    serializer = OrderSerializer(orders, many=True)
    return Response(serializer.data)
