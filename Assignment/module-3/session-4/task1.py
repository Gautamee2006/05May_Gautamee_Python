# Create a custom exception class called InvalidCouponCodeError for a Zomato-style 
# food ordering app, and raise this exception if a user tries to apply a coupon code 
# that is not in the list of valid codes.

class InvalidCouponCodeError(Exception):
    pass

code=['food10','save20','welcome50']
couponcode=input("enter coupponcode:")
try:
    if couponcode in code:
        print("Coupon Applied Successfully!")
    else:
        raise InvalidCouponCodeError 
except InvalidCouponCodeError:
    print("Error!")
    