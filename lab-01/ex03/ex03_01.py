def evenSum(lst):
    total = 0
    for number in lst:
        if number % 2 == 0:
            total += number
    return total

# Enter list
input_list = input("Enter list of number seperate by , : ")
numbers = list(map(int, input_list.split(',')))

print(f"Result: {evenSum(numbers)}")