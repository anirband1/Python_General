peg1 = []
peg2 = []
peg3 = []

peg_t = (peg1, peg2, peg3)

NUM_OF_BLOCKS = 8

def initialize():
    for i in range(NUM_OF_BLOCKS):
        peg1.insert(0, i)

# one block logic:

focus = 0

def add_on_top(peg, block):
    which_peg(block).remove(block)

    peg.insert(len(peg), block)


def which_peg(block):
    for peg in peg_t:
        if block in peg:
            return peg




def move_block(block):
    available_moves = list(peg_t)
    available_moves.remove(which_peg(block)) # removes the peg on which the block is currently on as a possibility

    # removes any peg with top lower than the current block
    for peg in available_moves:

        if len(peg) > 0 and peg[-1] < block:
            available_moves.remove(which_peg(peg[-1]))
    
    # move the block according to possibilities in available_moves
    if len(available_moves) == 1:
        add_on_top(available_moves[0], block) # if only 1 valid move, move to that peg
        
    else:
        empty_pegs = sum(len(i) == 0 for i in available_moves)

        if empty_pegs == 2: # blank blocks case
            add_on_top(available_moves[0], block) # here 0 is chosen randomly as it doesn't matter which empty peg you go to

        elif empty_pegs == 1: #  one blank, one filled, go to the one with the odd difference, else, empty
            for peg in available_moves:
                if len(peg) != 0:
                    if (peg[-1] - block) & 1:
                        add_on_top(peg, block)
                    else:
                        for peg in available_moves:
                            if len(peg) == 0:
                                add_on_top(peg, block)
                                break
        else: # all filled, place it on the one with the odd difference
            for peg in available_moves:
                if (peg[-1] - block) & 1:
                        add_on_top(peg, block)
                        break

# takes care of 1 recursion cycle
def cycle(block):
    move_block(block)

    if block != 0:
        cycle(block - 1)

    return

initialize()

# start a cycle for each successively bigger block
for block in peg1:
    cycle(block)


print(peg1)
print(peg2)
print(peg3)


        
            


    
