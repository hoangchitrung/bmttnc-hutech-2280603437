def isPrime(number):
    if number < 2:
        return False
    for i in range(2, int(number ** 0.5) + 1):
        if (number % i == 0):
            return False
    return True
number = int(input("Enter number to check if it prime: "))
if isPrime(number) == True:
    print(f"{number} is prime")
else:
    print(f"{number} is not prime")