#The BlackJack Game / 21

from os import system
import random
cards = [11, 2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10,10]
should_continue = True
while should_continue==True:
    play_game = input("Do you want to Play a Game of BlackJack? Type 'yes' or 'no': ").lower()
    if play_game=='yes':
        system("cls")
        user_card_1 = random.choice(cards)
        user_card_2 = random.choice(cards)
        user_cards = [user_card_1, user_card_2]
        print(f"Your cards: {user_cards}, Your Score: {sum(user_cards)}")
        computer_card_1 = random.choice(cards)
        computer_card_2 = random.choice(cards)
        computer_cards = [computer_card_1, computer_card_2]
        print(f"Computer's First Card: [{computer_card_1}]")
        stand_or_hit = input("Type 'Hit' to get another Card. Type 'Stand' to Pass: ").lower()
        def stand():
                sum_user_cards = sum(user_cards)
                sum_computer_cards = sum(computer_cards)
                if 11 in user_cards and 11 in computer_cards:
                    if sum_user_cards > 21 or sum_computer_cards > 21:
                         user_cards.remove(11)
                         user_cards.append(1)
                         computer_cards.remove(11)
                         computer_cards.append(1)
                
                if sum_computer_cards<14 and sum_computer_cards<21:
                    another_computer_card = random.choice(cards)
                    computer_cards.append(another_computer_card)
                    sum_computer_cards+=another_computer_card
                if sum_user_cards and sum_computer_cards > 21:
                    print(f"Your Final Cards: {user_cards}")
                    print(f"your Score:{sum_user_cards}")
                    print(f"Computer's Final Cards: {computer_cards}")
                    print(f"Computer Score:{sum_computer_cards}")
                    print("Push!")
                elif sum_computer_cards > 21:
                    print(f"Your Final Cards: {user_cards}")
                    print(f"your Score:{sum_user_cards}")
                    print(f"Computer's Final Cards: {computer_cards}")
                    print(f"Computer Score:{sum_computer_cards}")
                    print("Computer Bust!")
                    print("You Win!")
                elif sum_user_cards > 21:
                    print(f"Your Final Cards: {user_cards}")
                    print(f"your Score:{sum_user_cards}")
                    print(f"Computer's Final Cards: {computer_cards}")
                    print(f"Computer Score:{sum_computer_cards}")
                    print("You Bust!")
                    print("Computer Win!")
                elif sum_user_cards>sum_computer_cards:
                    print(f"Your Final Cards: {user_cards}")
                    print(f"your Score:{sum_user_cards}")
                    print(f"Computer's Final Cards: {computer_cards}")
                    print(f"Computer Score:{sum_computer_cards}")
                    print("You Win!")
                elif sum_computer_cards>sum_user_cards:
                    print(f"Your Final Cards: {user_cards}")
                    print(f"Your Score:{sum_user_cards}")
                    print(f"Computer's Final Cards: {computer_cards}")
                    print(f"Computer Score:{sum_computer_cards}")
                    print("Computer Win!")
                if sum_user_cards == sum_computer_cards:
                    print(f"Your Final Cards: {user_cards}")
                    print(f"your Score:{sum_user_cards}")
                    print(f"Computer's Final Cards: {computer_cards}")
                    print(f"Computer Score:{sum_computer_cards}")
                    print("it's a Push!")
        def hit():
            another_user_card = random.choice(cards)
            user_cards.append(another_user_card)
            
            print(f"Your Cards [{user_cards}], Your Score: {sum(user_cards)}")
            print(f"Computer's First Card: [{computer_card_1}]")
            if sum(user_cards)>=21:
                stand()
            elif sum(user_cards)<21:
                stand_or_hit = input("Type 'Hit' to get another Card. Type 'Stand' to Pass: ").lower()
                if stand_or_hit == 'hit':
                    hit()
                else:
                    stand()
        if stand_or_hit == "hit":
            hit()
        elif stand_or_hit == 'stand':
            stand()
        else:
             print("Invalid Input!")
    if play_game == 'no':
        should_continue = False
        print("Goodbye!")
