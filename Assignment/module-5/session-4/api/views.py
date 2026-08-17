from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import BasicAuthentication, TokenAuthentication, SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from .permissions import IsPremiumUser


class PlaylistView(APIView):
    """
    Music app endpoint for playlists using BasicAuthentication.
    """
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        playlists = [
            {"id": 1, "name": "Top Hits 2026", "genre": "Pop"},
            {"id": 2, "name": "Coding Focus", "genre": "Lo-Fi"}
        ]
        return Response({"message": "Playlists retrieved successfully", "playlists": playlists})


class OrderView(APIView):
    """
    Zomato-style food ordering endpoint using TokenAuthentication.
    """
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        orders = [
            {"id": 101, "item": "Paneer Butter Masala", "status": "Delivered"},
            {"id": 102, "item": "Chicken Biryani", "status": "In Transit"}
        ]
        return Response({"message": "Orders retrieved successfully", "orders": orders})


class CartView(APIView):
    """
    Flipkart-style shopping cart endpoint using SessionAuthentication.
    """
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        cart_items = [
            {"id": 1, "product": "Wireless Headphones", "quantity": 1}
        ]
        return Response({"message": "Cart items retrieved successfully", "cart": cart_items})

    def post(self, request):
        item = request.data.get("item", "Sample Product")
        return Response({"message": f"Added '{item}' to cart successfully", "user": request.user.username})


class TicketView(APIView):
    """
    BookMyShow-style ticket booking endpoint using IsPremiumUser permission class.
    """
    authentication_classes = [TokenAuthentication, SessionAuthentication, BasicAuthentication]
    permission_classes = [IsPremiumUser]

    def get(self, request):
        tickets = [
            {"id": 501, "movie": "Avengers", "seat": "A12", "status": "Confirmed"}
        ]
        return Response({"message": "Tickets retrieved successfully", "tickets": tickets})
