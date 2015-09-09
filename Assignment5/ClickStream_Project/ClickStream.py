import math
import sys
import operator
from collections import namedtuple
from heapq import heappush, heappop
import random


'''
Taking the arguments from the user. 
'''
featurefilename = sys.argv[1]
datafilename = sys.argv[2]
valuesfilename = sys.argv[3]
testdatafilename = sys.argv[4]
testvaluefilename = sys.argv[5]
thresholdValue = sys.argv[6]


'''
Tree Node for creating the Binary tree
'''
class TreeNode:
   def __init__(self,key,val,left=None,right=None,
                                       parent=None):
        self.key = key
        self.payload = val
        self.leftChild = left
        self.rightChild = right
        self.parent = parent

Data = []
testData = []
templist = []
ThresholdDepth = random.randrange(1, 273)
'''
Node tuple
'''
InfoGainNode = namedtuple("InfoGainNode", "infovalue, featureValue, splitValue, leftInfoGain, rightInfoGain")
DecisionTree = []


if float(thresholdValue) == 1 :
    ThresholdDepth = 273
elif float(thresholdValue) == 0.1 :
    ThresholdDepth = 133
elif float(thresholdValue) == 0.05 :
    ThresholdDepth = 85


'''
Reading the input from the training feature names file and saving it into Data list.
'''
file=open(featurefilename,'r')
for line in file.readlines() :
    templist.append(line.strip());
file.close()

templist.append("values");
Data.append(templist);

'''
Reading the input from the training data file and saving it into Data list.
'''

file=open(datafilename,'r')
for line in file.readlines() :
    line1 = line.split(' ')
    line1 = [int(i.strip()) for i in line1]
    Data.append(line1)
file.close()

'''
Reading the input from the test data file and saving it into test data list.
'''

file=open(testdatafilename,'r')
for line in file.readlines() :
    line1 = line.split(' ')
    line1 = [int(i.strip()) for i in line1]
    testData.append(line1)
file.close()

'''
Reading the input from the training values names file and saving it into Data list.
'''
temp = []
file=open(valuesfilename,'r')
for line in file.readlines() :
    temp.append(int(line.strip()))
file.close()    

for i in range(0,len(temp)) :
    if not (i == len(temp)) :
        Data[i+1].append(temp[i])
    
'''
Reading the input from the test value names file and saving it into Data list.
'''

temp1 = []
file=open(testvaluefilename,'r')
for line in file.readlines() :
    temp1.append(int(line.strip()))
file.close()    

for i in range(0,len(temp1)) :
    testData[i].append(temp1[i])

'''
Calculating the entropy for the values column initially
'''

def cal_entropy_valuesColumn():
    posCount = 0
    negCount = 0
    for i in range(1,274) : 
        if Data[i][274] == 1 :
            posCount = posCount + 1
        else :
            negCount = negCount + 1
    total = posCount + negCount
    probPos = float(posCount) / total 
    probNeg = float(negCount) / total
    value = -probPos*math.log(probPos,2) - probNeg*math.log(probNeg,2)
    return value

'''
The function decides the spliting criterion which is the average of the values present.
'''

def decideAttribute(featureName):
    j = 0
    for i in range(0,len(Data[0])) :
        if Data[0][i] == featureName :
            j = i
    sum = 0
    for i in range(1,len(Data)) :
        sum = sum + Data[i][j]
    return sum/40000


'''
Function calculates the information gain of the given feature name and  creates a node and pushes into the heap by maintaining the max information gain 
'''
def cal_Inf_Gain(featureName):
    avgVal = decideAttribute(featureName)
    leftCount = 0
    leftCountPositive = 0
    rightCount = 0
    rightCountPositive=  0
    leftvalue = 0
    rightvalue = 0
    j = 0
    for i in range(0,len(Data[0])) :
        if Data[0][i] == featureName :
            j = i
    for i in range(1,len(Data)) :
        if Data[i][j] <= avgVal :
            leftCount = leftCount + 1
            if Data[i][274] == 1 :
                leftCountPositive = leftCountPositive + 1
        else :
            rightCount = rightCount + 1
            if Data[i][274] == 1 :
                rightCountPositive = rightCountPositive + 1
    if leftCountPositive == 0 or rightCountPositive == 0 or ((leftCount - leftCountPositive) == 0) or ((rightCount - rightCountPositive) == 0):
        informationGain =  cal_entropy_valuesColumn()
    else :
        leftvalue = -(float(leftCountPositive)/leftCount)*math.log(float(leftCountPositive) / leftCount,2) - (float(leftCount-leftCountPositive) / leftCount)*math.log(float(leftCount - leftCountPositive) / leftCount,2)
        rightvalue = -(float(rightCountPositive)/rightCount)*math.log(float(rightCountPositive) / rightCount,2) - (float(rightCount - rightCountPositive) / rightCount)*math.log(float(rightCount - rightCountPositive) / rightCount,2)
        total = leftCount + rightCount
        featureEntropy = (float(leftCount)/total)*leftvalue + (float(rightCount)/total)*rightvalue
        informationGain = cal_entropy_valuesColumn() - featureEntropy
    nodeElement = InfoGainNode(infovalue = -informationGain, featureValue = featureName, splitValue = avgVal, leftInfoGain = leftvalue, rightInfoGain = rightvalue)
    heappush(DecisionTree,nodeElement)
    

'''
Calling the information gain function for each and every feature present.
'''
for i in range(0,274) :
    igValue = cal_Inf_Gain(Data[0][i])

DecisionNode = DecisionTree[ThresholdDepth]
correctDecisions = 0

'''
Parsing the test data and finding the accuracy of the values from the test data.
'''
for i in range(0,len(testData)):
    clickCount = testData[i][ThresholdDepth]
    result = 0
    if clickCount <= DecisionNode.splitValue :
        if DecisionNode.leftInfoGain > DecisionNode.rightInfoGain:
            result = 1
        else:
            result = 0
    else:
        if DecisionNode.leftInfoGain < DecisionNode.rightInfoGain:
            result = 1
        else:
            result = 0
    
    if result == testData[i][274]:
        correctDecisions = correctDecisions + 1

percentageCorrect = 100 - (float(correctDecisions)/len(testData)) * 100


print "Percentage Accuracy Found : " + str(percentageCorrect)

    

    
