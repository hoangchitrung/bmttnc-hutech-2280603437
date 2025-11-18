def reverseList(inputList):
    return inputList[::-1]
userInput = input("Enter a list of numbers to reverse: ")
numbers = list(map(int, userInput.split(',')))
print(f"Result: {reverseList(userInput)}")