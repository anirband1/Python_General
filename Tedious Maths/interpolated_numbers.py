'''
prints equidistant numbers between two numbers 
'''

import sys

divs = int(input("Divisions:    "))


def Divs():

    # a way to quit the infinite loop
    try:
        high = float(input("high:    "))
        low = float(input("low:     "))
    except:
        sys.exit()

    interpolant = (high - low) / divs

    l_num = [high - (i * interpolant) for i in range(divs)]

    print(l_num[1:])

    Divs()


if __name__ == "__main__":
    Divs()