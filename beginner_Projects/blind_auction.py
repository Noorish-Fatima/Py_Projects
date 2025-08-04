# blind auction program
from os import system
bids = {}
continue_bidding = True

def highest_bidder(bidding_dictionary):
    winner = ""
    highest_bid = 0
    max(bidding_dictionary)
    for bidder in bidding_dictionary:
        
        bid_amount = bidding_dictionary[bidder]
        if bid_amount> highest_bid:
            highest_bid = bid_amount
            winner = bidder

    print(f"Winner is {winner} with amount ${highest_bid}")

while continue_bidding == True:
    name = input("Enter Your name: ")
    price = int(input("Enter Your Bid Amount: $"))
    bids[name] = price
    should_continue = input("Are there any other Bidders? 'yes' or 'no': ").lower()
    
    if should_continue == 'no':
        continue_bidding = False
        highest_bidder(bids)
    elif should_continue == 'yes':
        system("cls")