# create tuple from list
def create_tuple(lst):
    return tuple(lst)
# Enter numbers to convert and process the input
userInput = input("Enter a list of numbers to reverse: ")
numbers = list(map(int, userInput.split(',')))

print(f"List: {numbers}")
print(f"Tuple: {create_tuple(numbers)}")