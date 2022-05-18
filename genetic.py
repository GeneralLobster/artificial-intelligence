import board
import time
import random as r

#declaration of the states for easier tracking and data manipulation
class State:
    gene = ""
    def __init__(self,Board) -> None:
        self.Board = Board
        self.fitness = self.Board.get_fitness()
        self.updateGene()
        self.survival = 0

    def updateGene(self):
        self.gene = ""
        for i in self.Board.map:
            for index,j in enumerate(i):
                if j == 1:
                    self.gene += str(index)
                    break
    def updateBoard(self,newGene):
        for row,i in enumerate(self.Board.map):
            for index,j in enumerate(i):
                if j == 1:
                    self.Board.flip(row,index)
        for row,index in enumerate(newGene):
            self.Board.flip(row,int(index))
        self.updateGene()
        self.fitness = self.Board.get_fitness()

#parameter declarations to be any size/state size we want
nStates=8
boardSize=5
states = []
start = time.time()
for i in range(0,nStates):
    states.append(State(board.Board(boardSize)))

#used for debugging
def displayAll(states):
    for i in states:
        print(f"Fitness: {i.fitness}\t Gene: {i.gene}\t Survival Chance: {i.survival}")
        i.Board.show_map()

#we won't stop until we find a fitness level of 0
found = False
while found==False:
    totalSum = 0
    for i in states:#accumulate and invert the probability, since we are looking for the lowest fitness, not the highest
        try:
            totalSum += 1/i.fitness
            i.fitness = 1/i.fitness
        except:#if the fitness level is already 0 from the randomly generated board, we go here and now we have our answer
            found=True
            print(f"Running time: {(time.time()-start)*1000}ms")
            i.Board.show_map()
            break
    if found!=True:
        for j in states:#calculates the survival rates
            j.survival = j.fitness/totalSum
        for k in states:#resets the fitness since we used it to invert the probabilities
            k.fitness = k.Board.get_fitness()
        

        tempStates = []#temp states to manipulate data
        #Selection Operation
        for k in range(len(states)):#this will determine our selection process
            select = r.random()#random float
            elseBranch = True#here to catch any potential issues with floating numbers
            trackingSum=0#tracking sum is the accumulative sum of everything
            for gene in states:
                trackingSum+=gene.survival
                #we did this in class, where if the trackingSum is greater than the random selection, then this "gene" will survive and be added to the next set of states
                if trackingSum> select:
                    tempStates.append(gene)
                    elseBranch = False
                    break
            if elseBranch == True:#if somehow, the trackingSum is never greater in the prior loop, we add another state to make sure we get N states total
                tempStates.append(states[r.randint(0,len(states)-1)])

        #Crossover and Mutation operations
        for i in range(0,len(tempStates),2):#we will be iterating in pairs to make the code a bit more efficient
            select = r.randint(1,len(tempStates)-2)#position of where we split the data; the reason it starts at 1 is because 0 would result in no crossover, and same for len(tempstate)-2
            #Crossover process
            firstCross = tempStates[i].gene[0:select] + tempStates[i+1].gene[select:len(tempStates[i+1].gene)]
            secondCross = tempStates[i+1].gene[0:select] + tempStates[i].gene[select:len(tempStates[i+1].gene)]
            #Mutation process, where we are selecting the position of the mutation(it can occur that the number is out of range, which means no mutation occurs)
            select1 = r.randint(0,len(tempStates[i].gene))
            select2 = r.randint(0,len(tempStates[i].gene))
            #Mutation numbers are here to determine where on the grid the mutation will occur
            mutation1 = r.randint(0,len(tempStates[i].gene)-1)
            mutation2 = r.randint(0,len(tempStates[i].gene)-1)
            if(select1 == len(tempStates[i].gene)):#if the position is out of range, we will simply move on
                tempStates[i].updateBoard(firstCross)
            else:#if the mutation is in range, we will concatenate the crossover gene and insert the mutation where the selection position is
                newCross = firstCross[0:select1] + str(mutation1) + firstCross[select1+1:]
                tempStates[i].updateBoard(newCross)
            #This process is the same, except for the second pair
            if(select2 == len(tempStates[i].gene)):
                tempStates[i+1].updateBoard(secondCross)
            else:
                newCross = secondCross[0:select2] + str(mutation2) + secondCross[select2+1:]
                tempStates[i+1].updateBoard(newCross)

        #Searching for the solution
        for index,i in enumerate(tempStates): #Iterate through the states to see if there is one with a fitness of 0
            if i.fitness == 0:#if there is, we can safely assume that the board has been solved for that specific one
                if found!=True:#if we already found a board at the start, then we do not need to display another board
                    found=True
                    print(f"Running time: {(time.time()-start)*1000}ms")
                    i.Board.show_map()
                    break
        #set the genetically altered boards into the states to continue the algorithm
        states = tempStates