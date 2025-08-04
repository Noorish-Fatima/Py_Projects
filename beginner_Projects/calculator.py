# Simple Calculator
def add_num(num1, num2):
    return (num1+num2)
def subtract_num(num1, num2):
    return(num1-num2)
def multiply_num(num1,num2):
    return(num1*num2)
def divide_num(num1, num2):
    return(num1/num2)
def modulo_num(num1, num2):
    return(num1%num2)
def expo_num(num1, num2):
    return(num1**num2)
def floor_num(num1, num2):
    return(num1//num2)

continue_calculating = True
while continue_calculating == True:

    num1 = int(input("Enter First Number: "))
    num2 = int(input("Enter second Number: "))
    option = input("select operation: +, -, *, /, %, **, % \n")

    if option == '+':
        print(add_num(num1, num2))
    elif option == '-':
        print(subtract_num(num1, num2))
    elif option == '*':
        print(multiply_num(num1, num2))
    elif option == '/':
        print(divide_num(num1, num2))
    elif option == '%':
        print(modulo_num(num1, num2))
    elif option == '**':
        print(expo_num(num1, num2))
    elif option == '//':
        print(floor_num(num1, num2))
    else:
        print("Invalid Input!")
    
    choice = input("want to continue? Type 'yes' or 'no': ")
    if choice=='no':
        continue_calculating = False
        print("Goodbye!")

