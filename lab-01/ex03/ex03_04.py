def getFirstLast(tuple_data):
    first = tuple_data[0]
    last = tuple_data[-1]
    return first, last

input_tuple = eval(input("Enter tuple: "))
first, last = getFirstLast(input_tuple)

print(f"First Element: {first}")
print(f"Last Element: {last}")