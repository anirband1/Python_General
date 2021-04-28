'''
BUBBLE SORT:

If a number in a list is greater than the, succeeding number, switch places.
'''
# changes original list, won't work with tuples


def bubble_sort(list_passed, descending=False):
    for i in range(len(list_passed) - 1):
        for j in range(len(list_passed) - 1):
            if list_passed[j] > list_passed[j + 1]:
                temp = list_passed[j]
                list_passed[j] = list_passed[j + 1]
                list_passed[j + 1] = temp
    if descending:
        list_passed = list_passed[::-1]
    return list_passed


list_to_sort = [90, 1, -85, 0, 34, 25, 6, 17, 73]

print(bubble_sort(list_to_sort))