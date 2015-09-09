import sys
import Queue as queue

"""Reading the input file from command line""" 
filename = sys.argv[1]


"""The course Node containing the required data fields :
1.courseName   
2.courseTimings
3.courseRecitations
4.studentsEnrolled
5.taAttendance : whether TA needs to attend the class
6.courseRequirements : required  skills for the course
7.tasRequired : number of TA's required depending on the students enrolled
8.taAssigned : list of TA's that are assigned initially empty
9.domainList : list of TA Assignments initially"""
class Course():
    def __init__(self):
        self.courseName=None
        self.courseTimings=[]
        self.courseRecitations=[]
        self.studentsEnrolled=None
        self.taAttendance=None
        self.courseRequirements=[]
        self.tasRequired=0
        self.taAssigned=[]
        self.domainList=[]

"""The TA Node containing the required data fields :
1.taName   
2.taCapacity : maximum number he can be act as TA , it is 1 for every TA
3.taRecitations
4.taClasses
5.taSkills : skills that are possessed by TA 
"""
class TA():
    def __init__(self):
        self.taName=None
        self.taCapacity=1
        self.taRecitations=[]
        self.taClasses=[]
        self.taSkills=[]

dummyTA = TA()
dummyTA.taName="dummyTA"
dummyTA.taCapacity=1
dummyTA.taRecitations=[]
dummyTA.taClasses=[]
dummyTA.taSkills=[]

"""Global list for holding all the courses nodes"""
courseVariablesList=[]
"""Global list for holding all the TA nodes"""
TADomainList=[]
file=open(filename,'r')
emptyCountList=[]
count=0
readLines=[]
"""Reading inputs from the given file and storing it in a list"""
for line in file.readlines() :
    readLines.append(line)
    if line.strip('\n') == '' :
        emptyCountList.append(count)
    count=count+1
"""Closing the file counter"""
file.close()

"""Processing the lines before the first space and updating the course nodes"""
for i in range(0,emptyCountList[0]) :
    temp = Course()
    j=1
    items = (readLines[i].strip('\n')).split(',')
    temp.courseName = items[0].strip()
    while(j < len(items)) :
        temp.courseTimings.append([items[j].strip(),items[j+1].strip()])
        j = j+2     
    courseVariablesList.append(temp)

"""Processing the lines between the first space and second space updating the course nodes with recitations list"""
def updateRecitations(list,courseName,recitationList) :
    for node in list :
        if (node.courseName == courseName) :
            node.courseRecitations = recitationList 

"""Processing the lines between the first space and second space updating the course nodes with classes list"""
for i in range(emptyCountList[0]+1,emptyCountList[1]) :
    j=1
    items = (readLines[i].strip('\n')).split(',')
    courseName = items[0].strip()
    recitationList=[] 
    while(j < len(items)) :
        recitationList.append([items[j].strip(),items[j+1].strip()])
        j = j+2
    updateRecitations(courseVariablesList,courseName,recitationList)

"""Processing the lines  updating the course nodes with total students enrolled and total required for the class"""
def updateStudentsEnrolled(list,courseName,students,taAttendance) :
    for node in list :
        if (node.courseName == courseName) :
            node.studentsEnrolled = students
            node.taAttendance = taAttendance
            node.tasRequired = 0
            if (int(students) >= 60) :
                node.tasRequired = 2
            if (int(students) < 60) and (int(students) >= 40) :
                node.tasRequired = 1.5
            if (int(students) < 40) and (int(students) >= 25) :
                node.tasRequired = 0.5
            
"""Processing the lines  updating the course nodes with course skills"""
for i in range(emptyCountList[1]+1,emptyCountList[2]) :
    items = (readLines[i].strip('\n')).split(',')
    updateStudentsEnrolled(courseVariablesList,items[0].strip(),items[1].strip(),items[2].strip())

def updateCourseRequirements(list,courseName,requirements) :
    for node in list :
        if (node.courseName == courseName) :
            node.courseRequirements = requirements  

for i in range(emptyCountList[2]+1,emptyCountList[3]) :
    items = (readLines[i].strip('\n')).split(',')
    items1=[]
    for j in range(1,len(items)) :
        items1.append(items[j].strip())
    updateCourseRequirements(courseVariablesList,items[0].strip(),items1)

"""Processing the lines  updating the TA nodes with details like TA names"""
for i in range(emptyCountList[3]+1,emptyCountList[4]) :
    temp = TA()
    j=1
    items = (readLines[i].strip('\n')).split(',')
    temp.taName = items[0].strip()
    while(j < len(items)) :
        temp.taClasses.append([items[j].strip(),items[j+1].strip()])
        j = j+2
    TADomainList.append(temp)    

"""Processing the lines  updating the TA nodes with details like TA skills"""
def updateTASkills(list,taName,skills) :
    for node in list :
        if (node.taName == taName) :
            node.taSkills = skills

for i in range(emptyCountList[4]+1,len(readLines)) :
    items = (readLines[i].strip('\n')).split(',')
    items1=[]
    for j in range(1,len(items)) :
        items1.append(items[j].strip())
    updateTASkills(TADomainList,items[0].strip(),items1)     

"""
The main logic of ForwardChecking is done here , initially we pass the course Lists and TA lists
1. We check whether the assignments is complete or not 
2. If it is not complete we select the next un-assigned variable course 
3. For the course that we selected we check for each and every domain(TA Nodes) and check the consistency if they pass we assign it
4. After assigning we will check whether other domain list for courses becomes empty 
5. If step 4 is success we will call the forwardChecking function
6. If any consistency fails we remove the assignment and check for other variables and TA nodes   
"""
def ForwardChecking(list1) :
    if checkCompleteAssignment(list1) :
        return list1
    var = selectUnassignedVariable(list1)    
    for value in var.domainList :
        if checkConsistent(value,var) :
            assignValue(var,value)
            if checkDomainEmpty(var,list1) :
                result = ForwardChecking(list1)
                if result != "Fail" :
                    return result
                if result == "Fail" and diffTAReq > 0 :
                    return "Fail"
            removeAssignment(var,value)   
    return "Fail" 

"""
The function returns the total TA capacity of the TA list
"""
def calculateTotalTACapacity(list) :
    sum = 0
    for item in list :
        sum = sum + item.taCapacity
    return sum

"""
The function returns the total TA required of the course list
"""
def calculateTotalTARequired(list) :
    sum = 0
    for item in list :
        sum = sum + item.tasRequired
    return sum

"""The function returns True or False depending on the total capacity that is available on the domainList"""
def checkDomainEmpty(var,list) :
    for item in list :
        if (not (item.courseName == var.courseName)) :
            if (not (item.tasRequired == 0)) :
                val = calculateTotalTACapacity(item.domainList)
                if val == 0:
                    return False
    return True            

"""
The function returns domain values for each variable course depending on the skills that matched ,
we used priority queue here
"""
def orderDomainValues(var,list) :
    priorityFringe = queue.PriorityQueue()
    for item in list :
        if not (item.taCapacity == 0) :
            temp = compareSkills(var.courseRequirements,item.taSkills)
            if not temp == 0 :
                priorityFringe.put((-temp,item))
    h=[]
    while(not priorityFringe.empty()) :
        h.append((priorityFringe.get())[1])
    return h        
"""
The function assigns the given TA to the course and updated the course list and TA list 
"""
def assignValue(var,value) :
    if var.tasRequired == 0.5 :
        value.taCapacity = (value.taCapacity) - 0.5
        var.tasRequired = 0
        var.taAssigned.append([value,0.5])
        if var.taAttendance == "yes" :
            for item in var.courseTimings :
                value.taClasses.append(item)
            for item in var.courseRecitations :
                value.taRecitations.append(item)    
    else :
        var.taAssigned.append([value,value.taCapacity])
        if var.taAttendance == "yes" :
            for item in var.courseTimings :
                value.taClasses.append(item)
            for item in var.courseRecitations :
                value.taRecitations.append(item)
        var.tasRequired = var.tasRequired - value.taCapacity
        value.taCapacity = 0 

"""
The function removes the given TA from the course Assignment and updates the course list and TA list
"""
def removeAssignment(var,value) :
    temp = var.taAssigned.pop()
    var.tasRequired = (var.tasRequired) + temp[1]
    value.taCapacity = (value.taCapacity) + temp[1]
    if var.taAttendance == "yes" :
        for item in var.courseTimings :
            value.taClasses.pop()
        for item in var.courseRecitations :
            value.taRecitations.pop()

"""
The function checks the completeness of assignments by checking whether there are any unassigned TA's for the courses
"""
def checkCompleteAssignment(list) :
    for item in list :
        if (item.tasRequired > 0) :
            return False 
    return True

"""
The Function returns the unassigned course 
"""
def selectUnassignedVariable(list) :
    for item in list :        
        if (item.tasRequired > 0 ) :
            return item

"""
Using a simple convention for converting the given times
"""
def calculateValue(time) :
    temp = time.split(' ')
    temp1 = temp[0].split(':')
    value = (int(temp1[0]) * 60) + int(temp1[1])
    if ((temp[1] == 'PM') and (temp1[0] != '12') ) :
        value = value + (12*60)
    return value

"""
The function checks whether the given recitation will be a clash for the TA nodes by using TA class list and TA recitation List
"""
def checkAvailabilityRecitations(list1,list2,list3) :
    recitationDay = list1[0] 
    recitationStartTime = calculateValue(list1[1])
    recitationEndTime = recitationStartTime + 90
    for item in list2 :
        taClassDay = item[0]
        if taClassDay == recitationDay :
            taClassStartTime = calculateValue(item[1])
            taClassEndTime = taClassStartTime + 80
            if ((taClassStartTime >= recitationStartTime) and (taClassStartTime <= recitationEndTime)) or ((taClassEndTime >= recitationStartTime) and (taClassEndTime <= recitationEndTime)) :
                return False
    for item in list3 :
        taRecitationDay = item[0]
        if taRecitationDay == recitationDay :
            taRecitationStartTime = calculateValue(item[1])
            taRecitationEndTime = taRecitationStartTime + 90
            if ((taRecitationStartTime >= recitationStartTime) and (taRecitationStartTime <= recitationEndTime)) or ((taRecitationEndTime >= recitationStartTime) and (taRecitationEndTime <= recitationEndTime)) :
                return False   
    return True 


"""
The function checks whether the given course class  will be a clash for the TA nodes by using TA class list and TA recitation List
"""
def checkAvailabilityCourses(list1,list2,list3) :
    courseDay = list1[0]
    courseStartTime = calculateValue(list1[1])
    courseEndTime = courseStartTime + 80
    for item in list2 :
        taClassDay = item[0]
        if taClassDay == courseDay :
            taClassStartTime = calculateValue(item[1])
            taClassEndTime = taClassStartTime + 80
            if ((taClassStartTime >= courseStartTime) and (taClassStartTime <= courseEndTime)) or ((taClassEndTime >= courseStartTime) and (taClassEndTime <= courseEndTime)) :
                return False
    for item in list3 :
        taRecitationDay = item[0]
        if taRecitationDay == courseDay :
            taRecitationStartTime = calculateValue(item[1])
            taRecitationEndTime = taRecitationStartTime + 90
            if ((taRecitationStartTime >= courseStartTime) and (taRecitationStartTime <= courseEndTime)) or ((taRecitationEndTime >= courseStartTime) and (taRecitationEndTime <= courseEndTime)) :
                return False
    return True


"""
The function returns the maximum skills match count
"""
def compareSkills(list1,list2) :
    if len(list1) == 0 :
        return len(list2)
    return len(set(list1).intersection(list2))

"""
The function checks the consistency of the assignment by calling the time clash functions mentioned above
"""
def checkConsistent(value,var) :
    if value.taCapacity == 0 :
        return False
    if var.tasRequired == 0 :
        return False
    if var.taAttendance == "yes" :
        if (len(var.courseRecitations) > 0) :
            for recitation in var.courseRecitations :
                if not (checkAvailabilityRecitations(recitation,value.taClasses,value.taRecitations)) :
                    return False
        if (len(var.courseTimings) > 0) :
            for course in var.courseTimings :
                if not (checkAvailabilityCourses(course,value.taClasses,value.taRecitations)) :
                    return False
    return True
    

def assignDomainList(list1,list2):
    tempList=[]
    list3 = [] #TAreqList
    list4 = [] #NoTAreqList
    list5 = [] #DummyTAList
    for item in list1 :
        if item.tasRequired == 0 :
            list4.append(item)
        else :
            tempList.append(item)    
            
    for item in tempList :
        item.domainList = orderDomainValues(item,list2)
        if (len(item.domainList) == 0) :
            list5.append(item)
        else :
            list3.append(item)
         
    return list3,list4,list5

TAreqList,NoTAreqList,DummyTAList = assignDomainList(courseVariablesList,TADomainList)    

intialtasRequired = calculateTotalTARequired(TAreqList)
initialtaCapacity = calculateTotalTACapacity(TADomainList)

diffTAReq = intialtasRequired - initialtaCapacity

result1 = ForwardChecking(TAreqList)

for item in TAreqList :
    print item.courseName,
    for ta in item.taAssigned :
        print ", ",
        print ta[0].taName,
        print ", " ,
        print ta[1],
        if item.tasRequired > 0 :
            print ", needed " + str(item.tasRequired)
    print ""
if len(NoTAreqList) :        
    print "=================================================="
    print "Courses which doesn't require TA's"
    print "=================================================="
    for item in NoTAreqList :
        print "course : " + item.courseName + " doesn't require TA"
        
if len(DummyTAList) :        
    DummyTAList.sort(key=lambda x: x.tasRequired)
    for item in DummyTAList :
        for val in TADomainList :
            if val.taCapacity > 0 :
                assignValue(item,val)
if len(DummyTAList) :        
    print "=================================================="
    print "Courses which doesn't match all the given TA Skills"
    print "=================================================="
    for item in DummyTAList :
        print item.courseName,
        for ta in item.taAssigned :
            print ", ",
            print ta[0].taName,
            print ", " ,
            print ta[1],
            if item.tasRequired > 0 :
                print ", needed " + str(item.tasRequired)
        print ""  
             
        