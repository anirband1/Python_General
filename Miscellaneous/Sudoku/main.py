import numpy as np

# * Add - No processing, interaction with sudoku
# * Elim - Processing, interaction with sol_arr

# region sudoku user input

# sudoku = np.zeros(shape=(9, 9))

# for i in range(9):
#     for j in range(9):

#         temp_str = input(f'x{i+1}, y{j+1}:  ' )

#         sudoku[i, j] = None if temp_str in [' ', ''] else int(temp_str)

# endregion

# region Init test sudoku
_ = np.nan

# Guardian - Hard
sudoku1 = [[_, _, _, _, _, 4, _, _, _],
           [4, _, _, 3, _, 9, 8, _, _],
           [_, 7, _, 8, _, _, _, 5, _],
           [_, 8, _, _, _, 5, _, 7, 2],
           [_, 4, _, 6, _, _, _, _, _],
           [6, _, _, _, 9, _, 5, 3, _],
           [8, _, _, _, _, _, _, _, _],
           [_, 3, _, _, 8, 2, 7, _, _],
           [_, _, 7, 5, _, _, _, 1, _]]

# Wikipedia - Easy
sudoku2 = [[5, 3, _, _, 7, _, _, _, _],
           [6, _, _, 1, 9, 5, _, _, _],
           [_, 9, 8, _, _, _, _, 6, _],
           [8, _, _, _, 6, _, _, _, 3],
           [4, _, _, 8, _, 3, _, _, 1],
           [7, _, _, _, 2, _, _, _, 6],
           [_, 6, _, _, _, _, 2, 8, _],
           [_, _, _, 4, 1, 9, _, _, 5],
           [_, _, _, _, 8, _, _, 7, 9]]

# Nature - V. Hard
sudoku3 = [[_, _, _, 8, _, 1, _, _, _],
           [_, _, _, _, _, _, 4, 3, _],
           [5, _, _, _, _, _, _, _, _],
           [_, _, _, _, 7, _, 8, _, _],
           [_, _, _, _, _, _, 1, _, _],
           [_, 2, _, _, 3, _, _, _, _],
           [6, _, _, _, _, _, _, 7, 5],
           [_, _, 3, 4, _, _, _, _, _],
           [_, _, _, 2, _, _, 6, _, _]]

sudoku = np.array(sudoku3)
# endregion

# region Init sol_arr
sol_arr = np.zeros(shape=(9, 9, 9))

for _i in range(9):
    for _j in range(9):
        for _k in range(9):
            sol_arr[_i, _j, _k] = _k + 1
# endregion

boxes_list = [[[0, 0], [0, 1], [0, 2],
               [1, 0], [1, 1], [1, 2],
               [2, 0], [2, 1], [2, 2]],

               [[0, 3], [0, 4], [0, 5],
               [1, 3], [1, 4], [1, 5],
               [2, 3], [2, 4], [2, 5]],

               [[0, 6], [0, 7], [0, 8],
               [1, 6], [1, 7], [1, 8],
               [2, 6], [2, 7], [2, 8]],

               [[3, 0], [3, 1], [3, 2],
               [4, 0], [4, 1], [4, 2],
               [5, 0], [5, 1], [5, 2]],

               [[3, 3], [3, 4], [3, 5],
               [4, 3], [4, 4], [4, 5],
               [5, 3], [5, 4], [5, 5]],

               [[3, 6], [3, 7], [3, 8],
               [4, 6], [4, 7], [4, 8],
               [5, 6], [5, 7], [5, 8]],

               [[6, 0], [6, 1], [6, 2],
               [7, 0], [7, 1], [7, 2],
               [8, 0], [8, 1], [8, 2]],

               [[6, 3], [6, 4], [6, 5],
               [7, 3], [7, 4], [7, 5],
               [8, 3], [8, 4], [8, 5]],

               [[6, 6], [6, 7], [6, 8],
               [7, 6], [7, 7], [7, 8],
               [8, 6], [8, 7], [8, 8]]]

# + Elimination
# -- Horizontal, Vertical elimination works
# -- Box elimination works

def H_V_Eliminate(): 
    # Eliminates possibility of number from all horizontal and vertical boxes

    for i in range(9):
        for j in range(9):

            if not np.isnan(sudoku.item((i, j))):

                num = sudoku.item((i, j))

                for k in range(9):
                    sol_arr[i, j, k] = 0 # if box is a number, change sol_arr to all zeros
                
                    sol_arr[i, k, int(num-1)] = 0 # change num to zero in all sol_arr left and right to this box
                    sol_arr[k, j, int(num-1)] = 0 # change num to zero in all sol_arr above and below to this box

def Boxes_Eliminate(): 
    for i in range(9): # box no.
        for coords in boxes_list[i]: # coord

            if not np.isnan(sudoku.item((coords[0], coords[1]))):

                num = sudoku.item((coords[0], coords[1]))

                for coords in boxes_list[i]:

                    sol_arr[coords[0], coords[1], int(num-1)] = 0


# + Checking / Placing
# -- Single possibility number addition works
# -- Remaining number in a box works
# -- Remaining number in a line works

def Single_Sol():
    # If there is only one possibility of a number, it adds the number to sudoku

    for i in range(9):
        for j in range(9):

            if np.count_nonzero(sol_arr[i, j]) == 1: # Check if array has only 1 non-zero number

                # add said number to sudoku at that coord
                sudoku[i, j] = np.nonzero(sol_arr[i, j])[0] + 1 #. +1 as np.nonzero returns index of said number
    
def Box_Check():  
    for i in range(9): # for all boxes
        for coords in boxes_list[i]: # for coords in box

            if np.isnan(sudoku.item((coords[0], coords[1]))): # if place is a nan
                for num in sol_arr[coords[0], coords[1]]: # for each num in its sol_arr

                    # performance gains... functionality is same as in the comments
                    if not_in_other_sol := not any(
                        coords != coords2
                        and num in sol_arr[coords2[0], coords2[1]]
                        for coords2 in boxes_list[i]
                    ):
                        sudoku[coords[0], coords[1]] = num

                    '''not_in_other_sol = True

                    for coords2 in boxes_list[i]: # check each place in box again

                        # if number not in any other sol_arr in box, add number to place
                        if coords != coords2:
                            if num in sol_arr[coords2[0], coords2[1]]: 
                                not_in_other_sol = False

                    if not_in_other_sol:
                        sudoku[coords[0], coords[1]] = num'''

def Line_Check():
    for i in range(9):
        for j in range(9):

            if np.isnan(sudoku.item((i, j)) ):

                for num_h in sol_arr[i, j]: # for num_h in sol_arr of coords

                    if not_in_other_lines := not any(
                        j != l and num_h in sol_arr[i, l] for l in range(9)
                    ):
                        sudoku[i, j] = num_h
                    
                    '''not_in_other_lines = True

                    for l in range(9): # second check

                        if j != l and num_h in sol_arr[i, l]:
                            not_in_other_lines = False

                    if not_in_other_lines:
                        sudoku[i, j] = num_h'''

                for num_v in sol_arr[i, j]: # for num_v in sol_arr of coords

                    if not_in_other_lines := not any(
                        i != l and num_v in sol_arr[l, j] for l in range(9)
                    ):
                        sudoku[i, j] = num_v

# passes = 0
# while np.count_nonzero(sol_arr) > 0:
#     H_V_Eliminate()
#     Boxes_Eliminate()
#     Box_Check()
#     Line_Check()
#     Single_Sol()
#     passes += 1
# print(passes)

for _ in range(20):
    H_V_Eliminate()
    Boxes_Eliminate()
    Single_Sol()
    Box_Check()
    Line_Check()


# TODO: Disjoint Subset ——–> ELIM 
# TODO: Temporary slate system _…...—–·•••°°°˘¯¯¯˚˚˚˚˚¯¯¯˘°°°°°°•••••••··———......………˛___˛…………....———···••••°°°˘¯¯¯˚˚˚˚˚ 



# TODO:             _….—·•°˘¯˚¯˘°•·—.…__….—·•°˘¯˚¯˘°•·—.…__….—·•°˘¯˚¯˘°•·—.…__….—·•°˘¯˚¯˘°•·—.…__….—·•°˘¯˚¯˘°•·—.…__….—·•°˘¯˚¯˘°•·—.…__….—·•°˘¯˚¯˘°•·—.…_
# TODO:                  _….—·•°˘¯˚¯˘°•·—.…__….—·•°˘¯˚¯˘°•·—.…__….—·•°˘¯˚¯˘°•·—.…__….—·•°˘¯˚¯˘°•·—.…__….—·•°˘¯˚¯˘°•·—.…__….—·•°˘¯˚¯˘°•·—.…__….—·•°˘¯˚¯˘°•·—.…_
# TODO:                       _….—·•°˘¯˚¯˘°•·—.…__….—·•°˘¯˚¯˘°•·—.…__….—·•°˘¯˚¯˘°•·—.…__….—·•°˘¯˚¯˘°•·—.…__….—·•°˘¯˚¯˘°•·—.…__….—·•°˘¯˚¯˘°•·—.…__….—·•°˘¯˚¯˘°•·—.…_
# TODO:                            _….—·•°˘¯˚¯˘°•·—.…__….—·•°˘¯˚¯˘°•·—.…__….—·•°˘¯˚¯˘°•·—.…__….—·•°˘¯˚¯˘°•·—.…__….—·•°˘¯˚¯˘°•·—.…__….—·•°˘¯˚¯˘°•·—.…_
# TODO:                       _….—·•°˘¯˚¯˘°•·—.…__….—·•°˘¯˚¯˘°•·—.…__….—·•°˘¯˚¯˘°•·—.…__….—·•°˘¯˚¯˘°•·—.…__….—·•°˘¯˚¯˘°•·—.…__….—·•°˘¯˚¯˘°•·—.…__….—·•°˘¯˚¯˘°•·—.…_
# TODO:                  _….—·•°˘¯˚¯˘°•·—.…__….—·•°˘¯˚¯˘°•·—.…__….—·•°˘¯˚¯˘°•·—.…__….—·•°˘¯˚¯˘°•·—.…__….—·•°˘¯˚¯˘°•·—.…__….—·•°˘¯˚¯˘°•·—.…__….—·•°˘¯˚¯˘°•·—.…_
# TODO:             _….—·•°˘¯˚¯˘°•·—.…__….—·•°˘¯˚¯˘°•·—.…__….—·•°˘¯˚¯˘°•·—.…__….—·•°˘¯˚¯˘°•·—.…__….—·•°˘¯˚¯˘°•·—.…__….—·•°˘¯˚¯˘°•·—.…__….—·•°˘¯˚¯˘°•·—.…_
# TODO:                 

# print(sol_arr[4, 5])

i=8
for coords in boxes_list[i]:
    print(sol_arr[coords[0], coords[1]])
