from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from .models import Restaurant


class RestaurantAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.restaurant_data = {
            "name": "Gourmet Bistro",
            "cuisine": "French",
            "rating": 4.8
        }
        self.restaurant = Restaurant.objects.create(
            name="Spice Villa",
            cuisine="Indian",
            rating=4.5
        )

    def test_create_restaurant(self):
        response = self.client.post('/api/restaurants/', self.restaurant_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], "Gourmet Bistro")
        self.assertEqual(response.data['cuisine'], "French")
        self.assertEqual(response.data['rating'], 4.8)

    def test_list_restaurants(self):
        response = self.client.get('/api/restaurants/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data, list)
        self.assertGreaterEqual(len(response.data), 1)

    def test_retrieve_restaurant(self):
        response = self.client.get(f'/api/restaurants/{self.restaurant.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], "Spice Villa")

    def test_retrieve_restaurant_not_found(self):
        response = self.client.get('/api/restaurants/9999/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_restaurant_put(self):
        updated_data = {
            "name": "Spice Villa Deluxe",
            "cuisine": "North Indian",
            "rating": 4.9
        }
        response = self.client.put(f'/api/restaurants/{self.restaurant.id}/', updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], "Spice Villa Deluxe")

    def test_update_restaurant_patch(self):
        patch_data = {"rating": 4.7}
        response = self.client.patch(f'/api/restaurants/{self.restaurant.id}/', patch_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['rating'], 4.7)

    def test_delete_restaurant(self):
        response = self.client.delete(f'/api/restaurants/{self.restaurant.id}/')
        self.assertIn(response.status_code, [status.HTTP_200_OK, status.HTTP_204_NO_CONTENT])
        self.assertFalse(Restaurant.objects.filter(id=self.restaurant.id).exists())

    def test_create_restaurant_bad_request(self):
        invalid_data = {"name": ""}
        response = self.client.post('/api/restaurants/', invalid_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
