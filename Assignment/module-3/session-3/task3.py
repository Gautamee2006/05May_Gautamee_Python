# Create a function book_movie_ticket that takes the number of tickets as input and divides 
# a fixed wallet balance by the number of tickets to get the price per ticket.
# Handle ZeroDivisionError and ValueError using multiple except blocks,
# and print a different message for each error.<br><br><em><strong>Hint:</strong>
# Use two separate except blocks for ZeroDivisionError and ValueError.</em>

def book_movie_ticket():
    balance=1000
    
    try:
        tickets=int(input("enter number of tickets:"))
        ticket_price=balance/tickets
        print("price of par ticket:",ticket_price)
    except ZeroDivisionError:
        print("Number of tickets cannot be zero!")
    except ValueError:
        print("Please enter a valid number!")

book_movie_ticket()
