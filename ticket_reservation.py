def print_purchase_count(purchases):
    """print the total number of purchases made"""
    print(f"\ntotal purchases made so far: {purchases}")

def main():
    purchases = 0
    
    print("=== ticket Reservatio System ===\n")
    
    while True:
        # Prompts user to reserve a ticket
        reserve = input("would u like to reserve a ticket? (y/n): ").lower()
        
        if reserve == 'y':
            # Prompts user to pay
            pay = input("pliz proceed to payment? (y/n): ").lower()
            
            if pay == 'y':
                purchases += 1
                print("payment successful! Ticket purchased.")
                print_purchase_count(purchases)
            else:
                print("payment cancelled. Reservation not completed.")
        
        elif reserve == 'n':
            print("\nThank u for using the Ticket Reservation System!")
            print_purchase_count(purchases)
            break
        
        else:
            print("invalid input... Please enter 'y' or 'n'.")
        
        print()

if __name__ == "__main__":
    main()