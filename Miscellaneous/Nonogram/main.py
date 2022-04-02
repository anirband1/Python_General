import numpy as np

# Top-down Left-right
# ! Flip everything sideways and then think

# region Once Only

# grid_size = int(input("Grid Size:   "))
grid_size = 6

def get_input() -> tuple:
    x_axis = []
    y_axis = []

    for _ in range(grid_size):
        tempL = input("x >    ").strip().split(' ')

        for i, e in enumerate(tempL):
            tempL.insert(i, int(tempL.pop(i)))
            
        x_axis.append(tuple(tempL))

    for _ in range(grid_size):
        tempL = input("y >    ").strip().split(' ')

        for i, e in enumerate(tempL):
            tempL.insert(i, int(tempL.pop(i)))
            
        y_axis.append(tuple(tempL))
    
    return x_axis, y_axis

# works
def zero_check():

    # idek

    for i, tup in enumerate(x_axis):
        if tup[0] == 0:
            for n in range(grid_size):
                img_grid[n, i] = 0

    for j, tup in enumerate(y_axis):
        if tup[0] == 0:
            for n in range(grid_size):
                img_grid[j, n] = 0

def all_no_and_gap_satisfy():
    for i, tup in enumerate(x_axis):
        if (sum(tup) + len(tup) - 1) == grid_size:

            img_grid[:grid_size, i] = 0 # zero setter

            # one setter
            temp = 0
            for num in tup:
                img_grid[temp:temp+num, i] = 1
                temp += num + 1
    
    for j, tup in enumerate(y_axis):
        if (sum(tup) + len(tup) - 1) == grid_size:
            img_grid[j, :grid_size] = 0
            temp = 0
            for num in tup:
                img_grid[j, temp:temp+num] = 1
                temp += num + 1

# endregion

# region Multiple Times

def overlap_check():
    # grid_x
    for i, tup in enumerate(x_axis):
        if tup[0] > grid_size//2:

            img_grid[ (grid_size - tup[0]) : ( - (grid_size - tup[0])), i] = 1 
    
    # grid_y
    for j, tup in enumerate(y_axis):
        if tup[0] > grid_size//2:

            img_grid[j,  (grid_size - tup[0]) : ( - (grid_size - tup[0]))] = 1 

    # grid_size - tup[0] # the gap from the top
                
# endregion

class CancelList:
    def __init__(self) -> None:
        self.cancel_list = np.zeros(shape=(grid_size, grid_size, 2)) # (x-coord, y-coord, 0 or 1 for null or possible)
    
    def cancel(self, *args):
        for pos in args:
            self[pos[0], pos[1]] = 0
    
    def get_y(pos):
        return y_axis[pos[1]]
        
# X axis represents the top numbers
# Y axis represents the left numbers
# * x_axis, y_axis = get_input() # print(f'{x_axis} \n{y_axis}')

x_axis =        [(1,), (5,), (2,), (5,), (1, 2), (2,)]
y_axis = [(2,1),
          (1,3),
          (1,2),
          (3,),
          (4,),
          (1,)]

img_grid = np.zeros(shape=(grid_size, grid_size))
for i in range(grid_size):
    for j in range(grid_size):
        img_grid[i, j] = None

zero_check() # -- once-only
all_no_and_gap_satisfy() # -- once-only
overlap_check()

print(img_grid)

# ! LEARN MERGE SORT FOR OVERLAP IN LISTS RECURSION