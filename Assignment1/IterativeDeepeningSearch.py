import sys
import time 


filename = sys.argv[1]

class Node():
    def __init__(self):
        self.data = []
        self.depth = None
        self.name = None
        self.path = []

root = Node()
file = open(filename,'r')
for line in file.readlines() :
    root.data.append(line.rstrip('\n'))
file.close()
root.depth = 0
root.name = "root"

goal = Node()
goal.data = ["--000--",
             "--000--",
             "0000000",
             "000X000",
             "0000000",
             "--000--",
             "--000--"]
goal.name = "goal"

matrixNumbers = [[-1,-1,0,1,2,-1,-1],
                 [-1,-1,3,4,5,-1,-1],
                 [6,7,8,9,10,11,12],
                 [13,14,15,16,17,18,19],
                 [20,21,22,23,24,25,26],
                 [-1,-1,27,28,29,-1,-1],
                 [-1,-1,30,31,32,-1,-1]]

#rowi,columnj --> columnk
def genColumnShift(i,j,k) :
    tempList = []
    tempList.append(matrixNumbers[i][j])
    tempList.append(matrixNumbers[i][k])
    return tempList

#columni, rowj --> rowk
def genRowShift(i,j,k) :
    tempList = []
    tempList.append(matrixNumbers[j][i])
    tempList.append(matrixNumbers[k][i])
    return tempList

def Goal_Test(state) :
    for i in range(0,7) :
        if state.data[i] != goal.data[i] :
            return False
    print "Goal State Found"
    return True

def Depth(state) :
    return state.depth

def EXPAND(state) :
    SuccessorList=[]
    for i in range(0,7):
        for j in range(0,5):
            temp=Node()
            if ((state.data[i][j]=="0")and(state.data[i][j+1]=="X")and(state.data[i][j+2]=="X")):
                for k in range(0,i):
                    temp.data.append(state.data[k])
                if j == 4 :
                    temp.data.append(state.data[i][:j]+"X00")
                else :
                    temp.data.append(state.data[i][:j]+"X00"+state.data[i][(j+3):])
                for k in range(i+1,7):
                    temp.data.append(state.data[k])
                temp.depth = state.depth + 1
                temp.name = "child at depth " + str(temp.depth)
                if len(state.path) != 0 :
                    for k in range(0,len(state.path)) :
                        temp.path.append(state.path[k])
                temp.path.append(genColumnShift(i,j+2,j))
                SuccessorList.append(temp)
            if ((state.data[i][j]=="X")and(state.data[i][j+1]=="X")and(state.data[i][j+2]=="0")):
                for k in range(0,i):
                    temp.data.append(state.data[k])
                if j == 4 :
                    temp.data.append(state.data[i][:j]+"00X")
                else :
                    temp.data.append(state.data[i][:j]+"00X"+state.data[i][(j+3):])
                for k in range(i+1,7):
                    temp.data.append(state.data[k])
                temp.depth = state.depth + 1
                temp.name = "child at depth " + str(temp.depth)
                if len(state.path) != 0 :
                    for k in range(0,len(state.path)) :
                        temp.path.append(state.path[k])
                temp.path.append(genColumnShift(i,j,j+2))
                SuccessorList.append(temp)
            if ((state.data[j][i]=="0")and(state.data[j+1][i]=="X")and(state.data[j+2][i]=="X")):
                if (j>0) :
                    for k in range(0,j):
                        temp.data.append(state.data[k])
                temp.data.append(state.data[j][:i]+"X"+state.data[j][(i+1):])
                temp.data.append(state.data[j+1][:i]+"0"+state.data[j+1][(i+1):])
                temp.data.append(state.data[j+2][:i]+"0"+state.data[j+2][(i+1):])
                for k in range(j+3,7):
                    temp.data.append(state.data[k])
                temp.depth = state.depth + 1
                temp.name = "child at depth " + str(temp.depth)
                if len(state.path) != 0 :
                    for k in range(0,len(state.path)) :
                        temp.path.append(state.path[k])
                temp.path.append(genRowShift(i,j+2,j))
                SuccessorList.append(temp)
            if ((state.data[j][i]=="X")and(state.data[j+1][i]=="X")and(state.data[j+2][i]=="0")):
                if (j>0) :
                    for k in range(0,j):
                        temp.data.append(state.data[k])
                temp.data.append(state.data[j][:i]+"0"+state.data[j][(i+1):])
                temp.data.append(state.data[j+1][:i]+"0"+state.data[j+1][(i+1):])
                temp.data.append(state.data[j+2][:i]+"X"+state.data[j+2][(i+1):])
                for k in range(j+3,7):
                    temp.data.append(state.data[k])
                temp.depth = state.depth + 1
                temp.name = "child at depth " + str(temp.depth)
                if len(state.path) != 0 :
                    for k in range(0,len(state.path)) :
                        temp.path.append(state.path[k])
                temp.path.append(genRowShift(i,j,j+2))
                SuccessorList.append(temp)
    return SuccessorList

count = 0
def Recursive_DLS(state,i) :
    limit=i
    global count
    cutoffOccurred=False
    if Goal_Test(state) :
        return state
    elif (Depth(state) == limit) :
        return "cutoff"
    else :
        for successor in EXPAND(state) :
            count = count + 1
            result=Recursive_DLS(successor,limit)
            if result == "cutoff" :
                cutoffOccurred=True
            elif (result != False) :
                return result
    if cutoffOccurred :
        return "cutoff"
    else :
        return False

def Depth_Limited_Search(state,i) :
    return Recursive_DLS(state,i)

def Iterative_Deepening_Search(state) :
    i=0;
    while (i>=0):
        print "Iteration " + str(i)
        result=Depth_Limited_Search(state,i)
        if result != "cutoff" :
            return result
        if result == "cutoff" :
            print "Cut off occurred"
        if result == False :
            return False
        i=i+1

startTime = time.time()
result = Iterative_Deepening_Search(root)
endTime = time.time()
if result == False :    
    print "Number of nodes expanded : " + str(count) 
    print "Solution Doesnot Exists"
else :    
    print "Number of nodes expanded : " + str(count) 
    print "Path to Goal : " ,
    print result.path
print "Time Taken : " + str(endTime - startTime)
