import board
import copy
import time

#N queens and rows
n =5
start = time.time()
x = board.Board(n)

#Reseter if it gets stuck in a loop
restartCounter = 0
currentFitness = x.get_fitness()#our current fitness level
while currentFitness > 0:
    restartCounter += 1
    for row,i in enumerate(x.map):#look iterate through each row of the grid
        blockedIndex = 0#our blocked index for when we are checking all possibilities
        tempBoard = []
        for index,j in enumerate(i):#we are now looking through each row
            if j == 1:#if the location happens to be where the queen is, flip it over
                blockedIndex = index
                x.flip(row,index)
        for index,j in enumerate(i):#we will now create multiple grids of the possibilities of the row generation
            tempGrid = copy.deepcopy(x)#so we do not overwrite the current grid or any subsequent grid
            if index != blockedIndex:#if it is not the blocked index, we can flip that index to have a queen and add it to our list of possibilities
                tempGrid.flip(row,index)
                tempBoard.append(tempGrid)
        bestFitness = 10000000#best fitness here is to ensure that we get the lowest possible
        bestIndex = 0#keeps track of best index
        for index,i in enumerate(tempBoard):#iterate through the current boards to find best fitness
            if i.get_fitness()<bestFitness:#if the current fitness is better than the last, that will be our best board to continue the process
                bestFitness = i.get_fitness()
                bestIndex = index
        if(bestFitness<=currentFitness):#if the bestFitness board is better than the current fitness, we can ensure that this board will be the current board
            x = tempBoard[bestIndex]
            currentFitness= bestFitness
        else:#if it is not the best, we will unflip the queen from the original board and continue
            x.flip(row,blockedIndex)
    if restartCounter >= 100:#if this somehow iterates over 100 times SPECIFICALLY for n=5, then we reset the counter and generate a new board
        restartCounter=0
        x = board.Board(n)
print(f"Running time: {(time.time()-start)*1000}ms")
x.show_map()

    
