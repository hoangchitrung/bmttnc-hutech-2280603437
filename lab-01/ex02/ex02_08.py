def divide_for_5(binary_number):
    decimal_number = int(binary_number, 2)

    if (decimal_number % 5 == 0):
        return True
    else:
        return False

print("Enter your chain of binary number (type 2 to stop): ")
binaries = []
while True:
    binary = input()
    if (binary == "done"):
        break
    binaries.append(binary)

result = []
for number in binaries:
    if divide_for_5(number) == True:
        result.append(number)
print(f"Binary number that could divide for 5: {','.join(result)}")
    