# file with obvious file structure
import os
import sys


def sort(array=[12, 4, 5, 6, 7, 3, 1, 15]):
    less = []
    equal = []
    greater = []

    if len(array) > 1:
        pivot = array[0]
        for x in array:
            if x < pivot:
                less.append(x)
            if x == pivot:
                equal.append(x)
            if x > pivot:
                greater.append(x)
        # Don't forget to return something!
        return sort(less) + equal + sort(greater)  # Just use the + operator to join lists
    # Note that you want equal ^^^^^ not pivot
    else:  # You need to hande the part at the end of the recursion - when you only have one element in your array, just return the array.
        return array

res = sort()
print(res)

num1 = 1
num2 = 2
num3 = 3
other_num1 = 1
other_num2 = 2
other_num3 = 3

list1 = []
list2 = []
list3 = range(10)
other_list1 = 17**6
other_list2 = ["asd"] * 10
other_list3 = [other_list1, other_num3, list1]

# this is a begining of first snippets
for i, x in enumerate(list2):
    print(i, x)
    num2 += num3
    num1 = num2 % 2
    list3 = sort(list3[::-1])

other_num1 = other_num2 + other_num1
for j, y in enumerate(other_list3):
    print(j)
    other_list2, other_list3 = other_list3, other_list2
    other_num2, other_num3 = 0, j