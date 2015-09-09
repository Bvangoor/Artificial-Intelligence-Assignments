from math import expm1
import math
import os
import sys

""" Global declaration of variables used in the program """

""" Total available words in the training data"""
repeatWords = {}

""" Dictionary to store the repeatition of each word once it has occurred """ 
dict = {}

""" This dictionary stores the emails declared as ham"""
globalDictHam = {}

""" This dictionary stores the emails declared as spam"""
globalDictSpam = {}

""" This dictionary stores all the emails"""
globalDict = {}

""" Calculates the total ham in the training data"""
totalHam = 0

""" Calculates the total spam in the training data"""
totalSpam = 0
c = 0

""" Input file for the training data"""
trainFileName = sys.argv[1]

""" Input file for the test data"""
testFileName = sys.argv[2]

""" Smoothing parameter used for the Naive Bayes Learner """ 
smoothingValue = 3


""" This method is used to split the emails separately from the training data set"""

def splitEmail():
    lines = open(trainFileName).read().splitlines()
    for x in lines:
        featuresOfEmail(x)

""" This method is used to extract the features of every email and then categorize it into ham and 
spam from the training data set. This also calculates the number of occurrences of every word occuring in
the emails and categorizes those. In preprocessing, non-word characters have been removed and the words are 
considered according to the paper given"""
def featuresOfEmail(lines):
    global totalHam
    global totalSpam
    features = lines.split(" ")
    for x in xrange(len(features)):
        if x == 0:
            continue
        if x == 1:
            if features[x] == "ham":
                totalHam = totalHam + 1
            if features[x] == "spam":
                totalSpam = totalSpam + 1
            # repeatWords.update({features[x]:"type"})
            continue
        if features[x].isalpha():
            if features[x] not in repeatWords:
                repeatWords.update({features[x]:features[x + 1]})
            else:
                temp = repeatWords[features[x]]
                repeatWords.update({features[x]:int(temp) + int(features[x + 1])})
                
        """If the email is ham, its words are extracted and stored"""       
        if features[1] == "ham":
            if features[x].isalpha():
                if features[x] not in globalDictHam:
                    globalDictHam.update({features[x]:features[x + 1]})
                else:
                    temp = globalDictHam[features[x]]
                    globalDictHam.update({features[x]:int(temp) + int(features[x + 1])})
                    
        """If the email is spam, its words are extracted and stored"""            
        if features[1] == "spam":
            if features[x].isalpha():
                if features[x] not in globalDictSpam:
                    globalDictSpam.update({features[x]:features[x + 1]})
                else:
                    temp = globalDictSpam[features[x]]
                    globalDictSpam.update({features[x]:int(temp) + int(features[x + 1])})
                    
        if features[x].isalpha():
                if features[x] not in globalDict:
                    globalDict.update({features[x]:features[x + 1]})
                else:
                    temp = globalDict[features[x]]
                    globalDict.update({features[x]:int(temp) + int(features[x + 1])})
                
    dict.update({features[0]:repeatWords})
    
  
""" This is the main function where the test data is taken as input and is tested for every word and segregated
into spam or ham based on the naive bayes theorm. """

def main():
    global c
    splitEmail()
    prob = 1
    ds = dh = 0
    """ Opens the test file"""
    linesTest = open(testFileName).read().splitlines()
    for z in linesTest:
        probListSpam = []
        probListHam = []
        featuresTest = z.split(" ")
        localDict = {}
        for y in xrange(len(featuresTest)):
            if y == 0 or y == 1:
                continue
            if featuresTest[y].isalpha():
                if featuresTest[y] not in localDict:
                    localDict.update({featuresTest[y]:featuresTest[y + 1]})
        """Every word in the data is taken into consideration """
        for x in repeatWords.keys():
            if x in localDict.keys():
                if x in globalDictSpam.keys():
                    if x not in globalDictHam:
                        th = 0
                        ts = globalDictSpam[x]
                        probWordInSpam = float(ts) / float(repeatWords[x])
                        probWordInHam = 0
                    else:
                        th = globalDictHam[x]
                        ts = globalDictSpam[x]
                        probWordInSpam = float(ts) / float(repeatWords[x])
                        probWordInHam = float(th) / float(repeatWords[x])
                    finalProbSpam = probWordInSpam / (probWordInSpam + probWordInHam)
                else:
                    finalProbSpam = 0
                if x in globalDictHam.keys():
                    if x not in globalDictSpam:
                        ts = 0
                        th = globalDictHam[x]
                        probWordInSpam = 0
                        probWordInHam = float(th) / float(repeatWords[x])
                    else:
                        th = globalDictHam[x]
                        ts = globalDictSpam[x]
                        probWordInSpam = float(ts) / float(repeatWords[x])
                        probWordInHam = float(th) / float(repeatWords[x])
                    finalProbHam = probWordInHam / (probWordInSpam + probWordInHam)
                else:
                    finalProbHam = 0
            else:
                finalProbSpam = 0
                finalProbHam = 0
            
            """Smoothing is also taken into consideration"""
            smoothFinalProbSpam = ((smoothingValue * 0.5) + (finalProbSpam * float(globalDict[x]))) / (smoothingValue + float(globalDict[x]))
            smoothFinalProbHam = ((smoothingValue * 0.5) + (finalProbHam * float(globalDict[x]))) / (smoothingValue + float(globalDict[x]))
            
            probListSpam.append(smoothFinalProbSpam)
            # print "smoothFinalProbSpam",smoothFinalProbSpam
            probListHam.append(smoothFinalProbHam)
            # print "smoothFinalProbHam",smoothFinalProbHam
    
        """Naive Bayes theorm is applied to calculate the spam. Log is applied to avoid the huge numbers.""" 
        sumSpam = 0
        for l in xrange(len(probListSpam)):
            sumSpam = sumSpam + math.log1p(1 - probListSpam[l]) - math.log1p(probListSpam[l])
            
        exponentialSpam = expm1(sumSpam)
        
        decisionSpam = 1.0 / (1.0 + float(exponentialSpam))
        
        # print decisionSpam
        
        sumHam = 0
        for l in xrange(len(probListHam)):
            sumHam = sumHam + math.log1p(1 - probListHam[l]) - math.log1p(probListHam[l])
            
        exponentialHam = expm1(sumHam)
        
        decisionHam = 1.0 / (1.0 + float(exponentialHam))
        
        # print decisionHam
        
            
        
        if decisionSpam >= decisionHam:
            # print "spam"
            ds = ds + 1
            if featuresTest[1].strip() == "spam":
                c = c + 1
        else:
            dh = dh + 1
            # print "ham",featuresTest[1]
            if featuresTest[1].strip() == "ham":
                c = c + 1
            
    ch = cs = 0
    for test in linesTest:
        testLine = test.split(" ")
        if testLine[1] == "ham":
            ch = ch + 1
            # print testLine[0]
        else:
            cs = cs + 1
            
    print "success Rate", math.ceil(float(c) * 100 / float((ch + cs)))

main() 
