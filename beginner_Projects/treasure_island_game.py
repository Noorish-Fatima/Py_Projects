# Tressure Island Game
# ...............................................................................
print("Welcome to Tressure Island!")
print("Your Mission is to find the tressure.")
print("You are at the cross road. Where do you want to Go?")
direction = input("\t Type 'Left' or 'Right': ").lower()
if direction == 'right':
    print("You Fell into a hole. Game over!")
elif direction == 'left':
    print("You've come to a lake. There is an island in the middle of the lake.")
    wait_swim = input("Type 'Wait' to wait for the boat. Type 'Swim' to swim across: ")
    if wait_swim == 'swim':
        print("you got attacked by an angry trout. Game over!")
    elif wait_swim == 'wait':
        print("You arrived at the island unharmed. There is a house with 3 doors.")
        print("One red, one yellow and one blue.")
        choose_color = input("Which color would you choose: ")
        if choose_color=='red':
            print("it's a room full of fire. Game over!")
        elif choose_color=='yellow':
            print("You found the tressure. You Win!")
        elif choose_color=='blue':
            print("You enter a room of beasts. Game over! ")
else:
    print("Invalid input!")
