# Hangman Game
import random
from hangman_words import Word_List as words_list

stages = [ '''
               ____ 
              |    |
              O    |
              |    |
             / \\   |
              |    |
             / \\   |
            _______|''',
             ''' 
               ____ 
              |    |
              O    |
              |    |
             / \\   |
              |    |
                   |
            _______|''',
             ''' 
               ____ 
              |    |
              O    |
              |    |
             / \\   |
                   |
                   |
            _______|''',
              '''
               ____ 
              |    |
              O    |
              |    |
             /     |
                   |
                   |
            _______|''',
            '''
               ____ 
              |    |
              O    |
              |    |
                   |
                   |
                   |
            _______|''',
             '''
               ____ 
              |    |
              O    |
                   |
                   |
                   |
                   |
            _______|''',
            '''
               ____ 
              |    |
                   |
                   |
                   |
                   |
                   |
            _______|'''
            ]

computer_word = random.choice(words_list)

placeholder = "_ "
word_length = len(computer_word) 
for position in range(word_length):
    placeholder+= "_ "
print(placeholder)
chances = 6
game_over= False
correct_letters = []
while chances>0 and not game_over :
    print(stages[chances])
    print(f"{chances}/6 Lives Left")
    display = ""
    user_guess = input("Guess a Letter: ").lower()
    if user_guess in correct_letters:
        print(f"You've already Guessed Letter {user_guess}")
    
    for char in computer_word:
        if char == user_guess:
            display += char
            correct_letters.append(user_guess)
        elif char in correct_letters:
            display+=char
        else:
            display += "_ "
    print(display)
    # print(display)
    

    if user_guess not in computer_word:
        print(f"Letter {user_guess} is Not in the word. You lose a live!")
        chances-=1
    
    if chances==0:
        print(f"Chances: {chances}")
        print(f"Word was: {computer_word}")
        print("You Lose! no lives left")

    if "_ " not in display:
        game_over = True
        print("You win")


