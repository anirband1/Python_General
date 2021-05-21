'''
INSERTION SORT

Starts arranging in increments from the start of the list.
'''
# changes original list, won't work with tuples


def insertion_sort(list_passed, descending=False):

    # each element being compared to all elements upto itself
    for i in range(len(list_passed)):
        for j in range(len(list_passed[:i])):
            if list_passed[i] < list_passed[j]:

                # switching logic
                temp = list_passed[j]
                list_passed[j] = list_passed[i]
                list_passed[i] = temp

    # reverse the list
    if descending:
        list_passed = list_passed[::-1]
    return list_passed


list_to_sort = [90, 1, -85, 0, 25, 34, 25, 6, 17, 73]

print(insertion_sort(list_to_sort))