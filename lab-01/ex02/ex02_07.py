# Enter line from user
print("Enter lines (enter done for stop): ")

lines = []

while True:
    line = input()
    if line.lower() == "done":
        break
    lines.append(line.upper())
print(lines)