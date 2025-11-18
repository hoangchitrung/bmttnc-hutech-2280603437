# count appear function
def countAppear(lst):
    count_dict = {}
    for item in lst:
        if item in count_dict:
            count_dict[item] += 1
        else:
            count_dict[item] = 1
    return count_dict

# Input string into a dict
inputString = input("Enter list word seperate by space: ")
word_list = inputString.split()

appearTimes = countAppear(word_list)
print(f"Appear Times: {appearTimes}")
