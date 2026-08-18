from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import OrderSerializer


class PlaceOrderAPIView(APIView):
    """
    API View to place a new order.
    Accepts customer_name, item, and quantity in JSON body.
    Validates quantity and saves the order to SQLite database.
    """

    def post(self, request):
        serializer = OrderSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
