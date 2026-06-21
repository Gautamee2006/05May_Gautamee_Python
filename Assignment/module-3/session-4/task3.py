'''Simulate a Flipkart-style checkout process where a function process_payment(amount) 
raises a PaymentFailedError (custom exception) if the amount is less than or equal to zero,
 and prints 'Payment Successful' otherwise.'''

class PaymentFailedError(Exception):
    pass

def process_payment(amount):
    try:
        if amount<=0:
             raise PaymentFailedError("payment not valid!")
        else:
            print("Payment Successful")
    except PaymentFailedError as e:
        print("ERROR:",e)

amount=int(input("enter Your Budget:"))
process_payment(amount)