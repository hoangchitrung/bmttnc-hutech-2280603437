# remove element functions
def removeElement(dictionary, key):
    if key in dictionary:
        del dictionary[key]
        return True
    else:
        return False
    
# create dict and key to delete
my_dict = {'a': 1, 'b': 2,'c': 3}
key = 'b'
result = removeElement(my_dict, key)
if result:
    print(f"Deleted successfully here is the new dict: {my_dict}")
else:
    print("Can not find the element to remove")