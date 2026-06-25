'''Simulate method overloading in Python by creating a class ZomatoOrder with a method add_item().
 Use default arguments so that add_item() can be called with just an item name or with item name
 and quantity. Show both usages with print statements.<br><br><em><strong>Hint:</strong>
 Python does not support true method overloading, but you can use default or *args parameters.</em>'''

class ZomatoOrder:
    def add_item(self,item_name,quantity=1):
        print("Item:",item_name)
        print("quantity:",quantity)

z=ZomatoOrder()

item=input("enter item name:")
choice=input("Do you want to enter quantity(yes/no):")

if choice.lower() =="yes":
    qtn=input("enter quantity:")
    z.add_item(item,qtn)
else:
    z.add_item(item)