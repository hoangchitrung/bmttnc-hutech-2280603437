# Enter rows and cols
inputStr = input("Enter X, Y: ")
dimension = [int(x) for x in inputStr.split(",")]

rowsNum = dimension[0]
colsNum = dimension[1]

# create a multi-array with 0 elements inside 
multiList =  [[0 for col in range(colsNum)] for row in range(rowsNum)]

# Calculating i and j for the elements inside arrays
for i in range(rowsNum):
    for j in range(colsNum):
        multiList[i][j] = i * j
print(multiList)