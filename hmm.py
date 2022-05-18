import sys
import copy

file = sys.argv[1]
newLines = [x.replace("\n","").split(",") for x in open(file).readlines()] 

#Normalization function was from MCMC assignment
def normalization(probVector):
    normalize = sum(probVector)
    return [x/normalize for x in probVector]

for data in newLines:
    probabilities = [float(x) for x in data[0:5]]#our probability states
    observedStates = [x for x in data[5:len(data)]]#our evidence variables
    accumProd = [1,1]#we set this to accumulate data
    for i in range(0,len(observedStates)): 
        tempAccumProd = copy.deepcopy(accumProd)#make a deep copy of the products since we are multiplying our probs by this
        if(observedStates[i]=='t' and i==0):#if the case is the X0 case and it's true, we perform this
            accumProd[0]*= ((probabilities[3])*(probabilities[1]*probabilities[0]+probabilities[2]*(1-probabilities[0])))
            accumProd[1]*= ((probabilities[4])*((1-probabilities[1])*probabilities[0]+(1-probabilities[2])*(1-probabilities[0])))
        elif(observedStates[i]=='t' and i!=0): #if the case is not X0 and true, we do this
            accumProd[0] = ((probabilities[3])*(probabilities[1]*tempAccumProd[0] + probabilities[2]*tempAccumProd[1]))
            accumProd[1] = probabilities[4]*((1-probabilities[1])*tempAccumProd[0]+(1-probabilities[2])*(tempAccumProd[1])) 
        elif(observedStates[i] == 'f' and i==0):# if the case is X0 and false, this
            accumProd[0]*= ((1-probabilities[3])*(probabilities[1]*probabilities[0]+probabilities[2]*(1-probabilities[0])))
            accumProd[1]*= ((1-probabilities[4])*((1-probabilities[1])*probabilities[0]+(1-probabilities[2])*(1-probabilities[0])))
        elif(observedStates[i]== 'f' and i!=0):#if the case is not X0 and false, we do this
            accumProd[0] = ((1-probabilities[3])*(probabilities[1]*tempAccumProd[0] + probabilities[2]*tempAccumProd[1]))
            accumProd[1] = (1-probabilities[4])*((1-probabilities[1])*tempAccumProd[0]+(1-probabilities[2])*(tempAccumProd[1])) 
        accumProd = normalization(accumProd)#normalize
    print(f"{','.join(x for x in data)}--><{format(accumProd[0],'.4f')},{format(accumProd[1],'.4f')}>")#output

    