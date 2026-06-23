#Build a class named FoodOrder that represents a Zomato-style order with properties: restaurant_name,
#items (a list), and total_price. Add a method show_order() that prints the order details in a readable 
#format.

class FoodOrder:
    def show_order(self):
        print("Restaurant Name:",self.restaurant_name)
        print("Items:",self.items)
        print("Total Price:",self.total_price)

order=FoodOrder()

order.restaurant_name=input("enter restaurant name:")

order.items=input("Enter items separated by comma:").split(",")

order.total_price=float(input("enter total price:"))

order.show_order()