# Input work and salary
work_hours = float(input("Enter standard hours: "))
amount_of_hours = float(input("Enter standard salary: "))

standard_hours = 44
pass_standard = max(0, work_hours - standard_hours)

# Total earning
salary = amount_of_hours * standard_hours + pass_standard * amount_of_hours * 1.5

print(f"Worker salary: {salary}")