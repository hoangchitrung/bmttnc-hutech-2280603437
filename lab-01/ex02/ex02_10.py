def reverse_string(inputString):
    return inputString[::-1]
userInput = input("Enter string to reverse: ")
print(f"Result: {reverse_string(userInput)}")