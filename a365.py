# Natu Myers 100068437
# Assignment 1 CISC 365
# The algorithm is as follows,
"""
First, find initial tuple that has the initial start time
if it doesn't have the initial start, keep subtracting by one until that's found


For the first value, 
#Find the best starting element by checking if it's start value equals the
# start value from the text file. If not, keep checking by lowering the target by one
# when we get to 0 we use our mergesort by difference to find the best one to choose as first in answer

For subsequent values

While i < EndTime (from text file)

    Reset the target to path[i][1]
    if there's a tupple with it's finish value equal to target
        add it to the temp list.
    else, target = target-1

    when target = 0, A merge sort will list these
    tupples by the difference between each pair in
    descending order. The top of temp (temp[0]) will be added to answers.
    i increases.


    
 
""" 


#TEXT EXTRACTION----------------
#open the text file
with open("SpaceStation.txt") as f:
    textLineList = f.readlines()

#--textLine ONE of SpaceStation.txt---|||
#the first line gives S and F
topRowSandF = list(map(int, (textLineList[0]).split()))
#  there is a time period in the near future,
#starting at time S and ending at time F,
# where ships will be easily visible from the ABQSS.

#S
visibleStartTime = topRowSandF[0]
#F
visibleFinishTime = topRowSandF[1]

#--textLine TWO---|||
#the second line gives bumber of projects
numberOfProjects = (textLineList[1])

#--textLine 3 to n---|||
#each subsequent line gives the project number,
# and start and finish time of a potential project.
project = []
for i in range(len(textLineList)):
    if i > 1: #for the subsequent lines only (ignore the info we already aquired)
        
        #split up a text line for each text line that has project start/finish
        #project[i] = (splitUpTextLine[0],splitUpTextLine[1])
        #i is the project number,  splitUpTextLine[0] is the start,
        #  splitUpTextLine[1] is the finish of that project.
        splitUpTextLine = list(map(int, (textLineList[i]).split()))
        project.append((splitUpTextLine[1],splitUpTextLine[2]))
        #this will mean for example project[5][0] gets the start time for project 5.
        #this will mean for example project[7][1] gets the finish time for project 7.
        
# first 2 lines have been removed because we already dealt w/ the 1st 2 elements of this array

#in a nutshell, the alg is find all diffs between pairs, 
# order the elements by diffs,
# try to get them to match the prescribed interval with no gaps
# or as small gaps as possible

#keep track of the differences in the list of tuples

for i in range(len(project)):
    project[i] =project[i] + ((project[i][1]-project[i][0]),)

# sort for the finish time. This is important in finding the best answers
def mergeSort(alist):
    if len(alist)>1:
        mid = len(alist)//2
        lefthalf = alist[:mid]
        righthalf = alist[mid:]

        mergeSort(lefthalf)
        mergeSort(righthalf)

        i=0
        j=0
        k=0
        while i < len(lefthalf) and j < len(righthalf):

            #we are ordering by diff between finish and start
            if lefthalf[i][2] > righthalf[j][2]:
                alist[k]=lefthalf[i]
                i=i+1
            else:
                alist[k]=righthalf[j]
                j=j+1
            k=k+1

        while i < len(lefthalf):
            alist[k]=lefthalf[i]
            i=i+1
            k=k+1

        while j < len(righthalf):
            alist[k]=righthalf[j]
            j=j+1
            k=k+1

#now that it's sorted,
#repeatedly choose the next tupples either fit perfectly, or overlap.
#the overlapping facter increase each time by one unit if nothing was found
#with the ones already chosen

mergeSort(project)
#step one, find initial tuple that has the initial start time or earlier

path=[]
firstInPath=[]
sub=0

#Find the best starting element by checking if it's start value equals the
# start value from the text file. If not, keep checking by lowering the target by one
# when we get to 0 we use our mergesort to find the best one to choose as first in answer
while (visibleStartTime-sub)>=0:
    #if there's no match for tuples in project[..] that equal visibleStartTime
    #subtract one because we're allowed to have intersections, not gaps
    if ([tupl for tupl in project if tupl[0] == visibleStartTime-sub] == []):
        sub=sub+1
    else:#if successful
        firstInPath = (  [tupl for tupl in project if tupl[0] == visibleStartTime-sub]  )
        break

#sort by differences, then get the biggest difference tuple  and put it in path
mergeSort(firstInPath)
path.append(firstInPath[0])




#do the same thing but for previous tuple in lists' final value
#also, check for finish value so you know when to stop

sub=0#the higher, the more the next possible answer (aka shift) intersects

#targetStart starts at visibleStartTime then grows
targetStart = visibleStartTime
nextSolutions = []

#at most, it'll be i long.
for i in range(visibleFinishTime):
    #Pushing the targeted Start to the next tuple's finish value
    targetStart=path[i][1]


    #find next path value
    while (targetStart-sub)>=0:
        #if there's no match for starting (tup[] is starting) values tuples in project[..] that equal visibleStartTime
        #subtract one because we're allowed to have intersections, not gaps
        if ([tup for tup in project if tup[0] == targetStart-sub] == []):
            sub=sub+1#we have to keep subtracting to find all tuples
            #we don't know where the big ones are at
           
        else:#if successful
            #one of the starting tupples will eventually equal 
            nextSolutions = (  [tup for tup in project if tup[0] == targetStart-sub]  )
            break


    
    #sort by tuple difference to get the best choice
    #in tuple (a,b), b-a is the diff

    #for the final value
    mergeSort(nextSolutions)
    path.append(nextSolutions[0])
    #if there's a value greater than the finish value
    #and we are at an i equal or less than 100...add it as well, because
    #we won't do this outside the loop.
    lookAhead = ([tup for tup in project if tup[0] == path[i+1][1]]) 
    if lookAhead != None and lookAhead != []:
        mergeSort(lookAhead)

        if (lookAhead[0][1] > 100):
            #to get the last
            path.append(lookAhead[0])
            break

#now to divide the path answers into 2 roughly equal groups
#to create 2 equal subset in a list
def equalSubset(lis):
    avg = len(lis) / float(2)
    ans = []
    last = 0.0

    while last < len(lis):
        ans.append(lis[int(last):int(last + avg)])
        last += avg
    return ans
halves=(equalSubset(path))

#printing---------------------
print("Selected Projects:")
for i in range(len(path)):
    print (i+1)#we add one because output counts 0th as 1st 

group1Sum = sum(halves[0][2])
group2Sum = sum(halves[1][2])

print("\nGroup 1 Total:  %i \nGroup 1 Projects:" % group1Sum)
for i in range(len(path)):
    if path[i] in halves[0]: #if in the first subset
        print (i+1)#we add one because output counts 0th as 1st

print("\nGroup 2 Total: %i \nGroup 2 Projects:"  % group2Sum)
for i in range(len(path)):
    if path[i] in halves[1]: #if in the second subset
        print (i+1)#we add one because output counts 0th as 1st
