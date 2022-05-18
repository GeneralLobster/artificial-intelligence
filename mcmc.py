from numpy import half
import random as r

#These classes are here so I don't lose my mind on just using numbers
class Cloudy:
    def __init__(self) -> None:
        self.chanceCloudy = .5

class Sprinker:
    def __init__(self) -> None:
        self.whenCloudy = 0.1
        self.whenNotCloudy = 0.5

class Rain:
    def __init__(self) -> None:
        self.whenCloudy = 0.8
        self.whenNotCloudy = 0.2

class WetGrass:
    def __init__(self) -> None:
        self.sprinkleRain = 0.99
        self.sprinkleNoRain = 0.95
        self.noSprinkleRain = 0.9
        self.noSprinkleNoRain = 0.05

clouds = Cloudy()
sprinklers = Sprinker()
rains = Rain()
wet = WetGrass()

#used to normalize using alpha on the probability vector result
def normalization(probVector):
    normalize = sum(probVector)
    return [x/normalize for x in probVector]

#used to halve the normalized probability vector for MCMC
def halfProb(probVector):
    tempVector = normalization(probVector)
    return [x/2 for x in tempVector]

#PART A
print("Part A. The sampling probabilities")
#Formulas were created based on handwritten breakdowns of the probability vectors
p = [clouds.chanceCloudy*(1-sprinklers.whenCloudy)*rains.whenCloudy,clouds.chanceCloudy*(1-sprinklers.whenNotCloudy)*rains.whenNotCloudy]
p = normalization(p)
print(f"P(C | -s, r) = <{format(p[0],'.4f')}, {format(p[1],'.4f')}>")

p = [clouds.chanceCloudy*(1-sprinklers.whenCloudy)*(1-rains.whenCloudy),clouds.chanceCloudy*(1-sprinklers.whenNotCloudy)*(1-rains.whenNotCloudy)]
p = normalization(p)
print(f"P(C | -s, -r) = <{format(p[0],'.4f')}, {format(p[1],'.4f')}>")

p = [rains.whenCloudy*wet.noSprinkleRain,(1-rains.whenCloudy)*wet.noSprinkleNoRain]
p = normalization(p)
print(f"P(R | c, -s, w) = <{format(p[0],'.4f')}, {format(p[1],'.4f')}>")

p = [rains.whenNotCloudy*wet.noSprinkleRain,(1-rains.whenNotCloudy)*wet.noSprinkleNoRain]
p = normalization(p)
print(f"P(C | -c, -s, w) = <{format(p[0],'.4f')}, {format(p[1],'.4f')}>\n")



#PART B
#We can store the transition states for S1 and S4, not necessarily S2 and S3, since S2 and S3 utilize the S1/S4 transition probs, except reversed
#S1 stays at index 0, goes to s2 or s3 on index 1
#S2 and S3 goes to S1 at index 0, stays at index 1
s1tos2 = [(rains.whenCloudy)*wet.noSprinkleRain,(1-rains.whenCloudy)*wet.noSprinkleNoRain]
s1tos2 = halfProb(s1tos2)
s1tos3 = [clouds.chanceCloudy*(1-sprinklers.whenCloudy)*rains.whenCloudy,clouds.chanceCloudy*(1-sprinklers.whenNotCloudy)*rains.whenNotCloudy]
s1tos3 = halfProb(s1tos3)


#S4 stays at index 0, goes to s2 or s3 on index 1
#S2 or S3 goes to S4 at index 0, stays at index 1
s4tos2 =[clouds.chanceCloudy*(1-rains.whenNotCloudy)*(1-sprinklers.whenNotCloudy),clouds.chanceCloudy*(1-rains.whenCloudy)*(1-sprinklers.whenCloudy)]
s4tos3 = [(1-rains.whenNotCloudy)*wet.noSprinkleNoRain,rains.whenNotCloudy*wet.noSprinkleRain]
s4tos2 = halfProb(s4tos2)
s4tos3 = halfProb(s4tos3)

print(f"Part B. The transition probability matrix\n\tS1\tS2\tS3\tS4")
print(f"S1\t{format(s1tos2[0]+s1tos3[0],'.4f')}\t{format(s1tos2[1],'.4f')}\t{format(s1tos3[1],'.4f')}\t0")
print(f"S2\t{format(s1tos2[0],'.4f')}\t{format(s1tos2[1]+s4tos2[1],'.4f')}\t0\t{format(s4tos2[0],'.4f')}")
print(f"S3\t{format(s1tos3[0],'.4f')}\t0\t{format(s1tos3[1]+s4tos3[1],'.4f')}\t{format(s4tos3[0],'.4f')}")
print(f"S4\t0\t{format(s4tos2[1],'.4f')}\t{format(s4tos3[1],'.4f')}\t{format(s4tos2[0]+s4tos3[0],'.4f')}\n")


#PART C
#Select num is to randomly calculate the RNG that determines which state we move to
def selectNum(transition):
    transitionRNG = r.random()
    accumulativeProb = 0
    for index,value in enumerate(transition):
        accumulativeProb+=value
        if(transitionRNG<accumulativeProb):#if this is the chosen state we move to based on prob vector, we return that number
            return index

#Main bulk
def simulationMCMC():
    state = r.randint(0,3) #our initial starting state
    transitions = [[s1tos2[0]+s1tos3[0],s1tos2[1],s1tos3[1]],
                    [s1tos2[0],s1tos2[1]+s4tos2[1],s4tos2[0]],
                    [s1tos3[0],s1tos3[1]+s4tos3[1],s4tos3[0]],
                    [s4tos2[1],s4tos3[1],s4tos2[0]+s4tos3[0]]]#this nested list stores all the state's transition probabilities
    cloudCount = 0#count the total number of Cloud = true states
    noCloudCount = 0 #count the total number of Cloud = false states
    for i in range(1000000):
        index = selectNum(transitions[state])#we grab the chosen index/transition state based on our previous state
        #Note: we do not need to worry about setting the states if the index happens to land on the index that lets the state stay the same
        if state == 0:#if the state is currently 0, we can go to S2/S3, which is either +1 or +2
            state+=index
        elif state == 1:#if the state is 1, we can go back to S1 or up to S4, which is either -1 or +2
            if index == 0:
                state-=1
            elif index == 2:
                state+=2
        elif state == 2:#if the state is 2, we can either go back to S1, or go to S4, which is either -2 or +1
            if index == 0:
                state-=2
            elif index == 2:
                state +=1
        else:#if we land on the last state, we can go back to S2/S3, hence why we either do (2-S2Index) or (2-S3Index), which S2 is 0, and S3 is 1, S4 would stay the same
            state-= (2-index)
        if(state == 0 or state == 1):#State 0 and State 1 are where Cloud = True, so we add there
            cloudCount+=1
        else:#State 2 and State 3 are where Cloud is False.
            noCloudCount+=1
    return [cloudCount,noCloudCount]

partCValue = normalization(simulationMCMC())
print(f"Parc C. The probability for the query\nP(C | -s, w) = <{format(partCValue[0],'.4f')},{format(partCValue[1],'.4f')}>")


    