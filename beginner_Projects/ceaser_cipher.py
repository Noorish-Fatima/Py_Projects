# ceaser cipher program

alphabets = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm',
 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']

def encrypt_decrypt():
    def encrypt(original_text, shift_amount):
        cipher_text = ""
        for letter in original_text:
            shifted_position = alphabets.index(letter)+shift_amount
            shifted_position %= len(alphabets)
            cipher_text+=alphabets[shifted_position]
            
        print(f"Here is the Encoded Text: {cipher_text}")

    def decrypt(original_text, shift_amount):
        cipher_text = ""
        for letter in original_text:
            shifted_position = alphabets.index(letter)-shift_amount
            shifted_position %= len(alphabets)
            cipher_text+=alphabets[shifted_position]
        print(f"Here is Decoded Text: {cipher_text}")
   
    if direction == 'encode':
        encrypt(text, shift)
    elif direction == 'decode':
        decrypt(text, shift)
    else:
        print("Invalid Input!")

should_continue = True
while should_continue==True:
    direction = input('''Type "Encode" to Encrypt, Type "Decode" to Decrypt\n''').lower()
    text = input("Enter your Text: ").lower()
    shift = int(input("Enter shift Number: "))
    encrypt_decrypt()

    restart = input("Type 'yes' if you want to continue. otherwise type 'no'.\n ").lower()
    if restart == "no":
        should_continue=False
        print("Goodbye!")

