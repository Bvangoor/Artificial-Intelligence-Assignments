import Queue as queue
import sys
import time 

filename = sys.argv[1]

class Node():
    def __init__(self):
        self.data = []
        self.depth = None
        self.name = None
        self.path = []
        self.stateCost = None
        self.heuristic = None
        self.function = None

root = Node()
file = open(filename,'r')
for line in file.readlines() :
    root.data.append(line.strip('\n'))
file.close()
root.depth = 0
root.name = "root"
root.stateCost = 0
root.heuristic = 0
root.function = root.stateCost + root.heuristic 

goal = Node()
goal.data = ["--000--",
             "--000--",
             "0000000",
             "000X000",
             "0000000",
             "--000--",
             "--000--"]
goal.name = "goal"
goal.stateCost = 0
goal.heuristic = 0
goal.function = goal.stateCost + goal.heuristic


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
    return True

def Depth(state) :
    return state.depth

#Manhattan Distance Divided by 2
def CalculateHeuristics(state) :
    count = 0
    value = 0
    for i in range(0,7) :
        for j in range(0,7) :
            if state.data[i][j] == "X" :
                value = abs(i-3) + abs(j-3)
                count = count + value
    return (count/2) 

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
                temp.stateCost = temp.depth
                temp.heuristic = CalculateHeuristics(temp)
                temp.function = temp.stateCost + temp.heuristic
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
                temp.stateCost = temp.depth
                temp.heuristic = CalculateHeuristics(temp)
                temp.function = temp.stateCost + temp.heuristic
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
                temp.stateCost = temp.depth
                temp.heuristic = CalculateHeuristics(temp)
                temp.function = temp.stateCost + temp.heuristic
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
                temp.stateCost = temp.depth
                temp.heuristic = CalculateHeuristics(temp)
                temp.function = temp.stateCost + temp.heuristic
                SuccessorList.append(temp)
    return SuccessorList

def compare(state1,state2) :
    for i in range(0,7) :
        if state1.data[i] != state2.data[i] :
            return False
    return True 

def check(state,list) :
    for node in list :
        if compare(state,node) :
            return True
    return False

priorityFringe = queue.PriorityQueue()
closedList = []

def Graph_Search(state) :
    global closedList
    priorityFringe.put((state.function,state))    
    while True :
        if priorityFringe.empty() : 
            return False
        node = (priorityFringe.get())[1]
        if Goal_Test(node) :
            return node
        if not check(node,closedList) :
            closedList.append(node)
            list = EXPAND(node)
            for node in list :
                priorityFringe.put((node.function,node))  

startTime = time.time()
result = Graph_Search(root)
endTime = time.time()
print "Number of Nodes Expanded : " + str(len(closedList))
if result == False :
    print "Solution Doesnot Exists"
else :
    print "Path to Goal State : ",
    print result.path
print "Time Taken : " + str(endTime - startTime)
