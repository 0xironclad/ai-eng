import math

# is_published = True
# if is_published:
#     print("Published")
# else:
#     print("Not published")

text = """
This is a multi-line string
that spans multiple lines
I think it's pretty cool
"""
# print(text)
# print(f'Number of chars: {len(text)}')
# print('hello'[0:3])
# print('hello'[-1])

first_name = "john"
last_name = "doe"
full_name = f"{first_name} {last_name}"
# print(f'{full_name} is a very good programmer')
# print(full_name.upper())
# print(full_name.lower())
# print(full_name.title())
# print(full_name.find('o'))
# print(full_name.replace('o', 'a'))
# print('john' in full_name)

x = 10
y = x + 2j
# print(type(y))
# print(x/3)
# print(x//3)
# print(x%3)
# print(x**3)
# print(math.pow(2, 3))

# x = input("x: ")
# y = int(x) + 1
# print(f"y: {y}")

# print("Bag".casefold())

# age = input("Age: ")
# message = "Elligible" if int(age) >= 18 else "Not eligible"
# print(message)

# if 30 > int(age) > 18:
#     print("You are eligible")
# else:
#     print("You are not eligible")


# for i in range(1, 10, 2):
#     if i == 6:
#         print("Found 6")
#         break
#     print(i)
# else:
#     print("Loop finished without break")


# number = 100
# while number > 0:
#     print(number)
#     number //= 2

# count = 0
# for i in range(1, 10):
#     if i % 2 == 0:
#         count += 1
#         print(i)
# print(f"We have {count} even numbers")


def increment(number, by=3):
    return number + by


# print(increment(number=2))


def process_user(name: str, age: int) -> bool:
    return "student" in name and age >= 18


grades = [85, 90, 78, 92, 88]
# for index, grade in enumerate(grades):
#     print(index, grade)
# print(f'Average grade: {sum(grades) / len(grades)}')

# nums = [3, 1, 4, 1, 5]
# nums.sort()
# print(nums)
# nums.remove(1)
# print(nums)
# nums.insert(0, 10)
# print(nums)
# nums.pop()
# print(nums)
# print(f'index of 4: {nums.index(4)}')
# print(f'length: {len(nums)}')
# nums.extend([6, 7, 8, 5, 6, 7])
# print(nums)
# print(f'count of 6: {nums.count(6)}')
# nums.sort()
# nums.reverse()
# print(nums)
# nums.clear()
# print(nums)


coordinates = (1, 2, 3)
x, *rest = coordinates
# print(type(rest), type(coordinates))
# print(x, rest)

# l2 = [n ** 2 for n in range(10) if 9 >n > 4]
# print(l2)
# l3 = list(coordinates)
# print(l3)
# del l3[0]
# print(l3)
# l3.extend([x for x in range(10) if x > 5])
# print(l3)
# del l3[0:3]
# print(l3)


s = {1, 2, 3}
print(s)
s.add(4)
print(s)
s.remove(1)
print(s)
s.clear()
print(s)