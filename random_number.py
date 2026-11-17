import random

size = 4
choices = [0,1]

choice_text = ""

for choice in range(size):
    choice_text += str(random.choice(choices))
    

number = int(choice_text, 2)


print(f"Binary {choice_text} | Decimal {number}")