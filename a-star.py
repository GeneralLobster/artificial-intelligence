import re
import math
import sys

#used as a metric to generate the cities provided
class City:
    #each city needs a parent city in order to figure out the optimal path to the destination from the target
    parentCity = None

    def __init__(self,name,coordinates,neighbors) -> None:
        self.cityName = name #name of the city as an identifier
        self.location = coordinates #this is the coordinate location of the city
        self.neighbors = neighbors #these are dictionaries that store the different cities and their cost values
        self.straight = 0 #straight is the straight-line distance called h(n)
        self.costPrior=0 #this is the total cost to travel to the specific city of a path called g(n)

    def getFCost(self):
        return self.straight + self.costPrior #calculates the f(n) given the straight line distance and cost

    #haversine formula calculation
    def calculateStraight(self,target):
        rad = math.pi/180
        self.straight = 2*3958.8*math.asin(math.sqrt(math.sin((target.location[0]*rad-self.location[0]*rad)/2)**2+
        (math.cos(self.location[0]*rad)*math.cos(target.location[0]*rad)*math.sin((target.location[1]*rad-self.location[1]*rad)/2)**2)))

#convert neighbors on map to a dictionary for easier search
def toDict(costs):
    costs = costs.replace(')','').split(",") #used to split and remove the unnecessary characters to get the travel costs
    dictCosts = {} #dictionary to store city to cost
    for cost in costs:
        cost = cost.split("(")#split by ( because the strings are city(number
        dictCosts[cost[0]] = float(cost[1])#append to dictionary
    return dictCosts


#finds the city we are looking for
def findCity(cities,target):
    for city in cities:
        if(city.cityName == target):
            return city


def aStar(cities,start,target):
    #cities that have to be looked at
    queue = []
    #cities that have already been looked at
    finished =[]
    queue.append(start) #add the starting location to begin the process
    while len(queue)>0:
        #this section determines the lowest F cost amongst all of the cities that we need to look at
        currentCityIndex = 0
        for i in range(len(queue)):
            if(queue[currentCityIndex].getFCost()>queue[i].getFCost()):
                currentCityIndex=i
            elif(queue[currentCityIndex].getFCost()==queue[i].getFCost()):
                if(queue[currentCityIndex].straight > queue[i].straight):
                    currentCityIndex=i
        #lowest F cost in the queue will be the current city we are looking at
        currentCity = queue[currentCityIndex]
        queue.remove(currentCity) #we can safely remove this from the queue, since we are looking at it
        finished.append(currentCity)#this node/city is now technically finished as soon as we finish the loop

        #base case check to determine if we have successfully reached the destination city
        if currentCity.cityName == target.cityName:
            path = []
            while currentCity.cityName != start.cityName: #we are working from destination to starting point here, since each destination has a parent
                path.append(currentCity)#we add the current city to the path/route
                currentCity = findCity(cities,currentCity.parentCity.cityName)#we now convert the currentCity node to its parent node
            path.append(currentCity)#append this here because this is our starting location
            return path

        #determining which of the neighbors will be added to the queue, and whose parent it is    
        for neighborCity in currentCity.neighbors:
            neighbor = findCity(cities,neighborCity) #find the city class of the neighbor
            costToNeighbor = currentCity.costPrior + currentCity.neighbors[neighborCity] #this is the computation of the g(n) cost
            if neighbor in finished:#if the neighborCity has already been computed, we can entirely ignore this 
                continue
            elif (neighbor not in queue) or (costToNeighbor < neighbor.costPrior):#with the assumption that the neighborCity has not been added to the queue
                #or that the g(n) of the neighbor is less than the cost prior, we can continue. This is useful when we already overwrote the costPrior from another currentCity that has this neighbor
                try:#try block in order to prevent an error where there is no parentCity in the currentCity to catch an infinite loop that occurs in the base case
                    if(currentCity.parentCity.cityName != neighbor.cityName):
                        neighbor.costPrior = costToNeighbor #set the cost of the current neighbor to the total cost taken
                        neighbor.parentCity = currentCity #set the parent city to the current city being used
                        if neighbor not in queue:#with the assumption the neighbor is not already in the queue, we can add them to the list
                            queue.append(neighbor)
                except:#except block does the same as the try, except the if statement needed to see if the parentCity is the same as the neighboring city of a current city
                    neighbor.costPrior = costToNeighbor
                    neighbor.parentCity = currentCity
                    if neighbor not in queue:
                        queue.append(neighbor)

#establish input 
coords = open("coordinates.txt").readlines()
costMap = open("map.txt").readlines()
cities = [] #this stores all the cities that will be from the text files

#Creation of the cities
for cost,location in zip(costMap,coords):
    tempCost = cost.replace('\n','').split("-") #split the values
    tempCost[1] = toDict(tempCost[1]) #convert the costs to a dictionary
    tempLocation = location.replace('\n','').split(":")#parses the locations and converts them into true x/y coords
    tempLocation[1] = re.sub("[()]", "",tempLocation[1]).split(",")#removes unnecessary parenthesis that occur from parsing
    coordinates = []#coordinates here to create a bonefide list
    for i in tempLocation[1]:
        coordinates.append(float(i))#convert string to float
    cities.append(City(tempCost[0],coordinates,tempCost[1]))#create the specific instance of a city

#command line arguments
start = sys.argv[1]
target = sys.argv[2]
#find our target class
for index, city in enumerate(cities):
    if(city.cityName == target):#if we find the string matches the destination, we make the target it
        target = cities[index]
    if(city.cityName == start):#if we find the string that matches the starting point, we make the start it
        start = cities[index]

#updates all the straight line distances dependent on target
for i in cities:
    i.calculateStraight(target)
    
#gives us our desired path
pathing = aStar(cities,start,target)
pathing.reverse() #reverse the path since the list is currently from destination to start
cityPath = []#used to properly output what we want
for i in pathing:
    cityPath.append(i.cityName)
#terminal output
print(f"From city: {start.cityName}\nTo city: {target.cityName}")
print("Best Route:", ' - '.join(cityPath))
print(f"Total distance: {round(pathing[len(pathing)-1].costPrior,2):.2f} mi")