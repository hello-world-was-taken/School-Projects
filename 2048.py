'''This is a 2048 clone game. If you have ever played 2048, this is just like that. If not, then the game mecahnics is as follows:
    you are expected to merge the tiles with similar numbers. But there is catch. You can only merge tiles which are right next to
    eachother be it vertically or horizontally.
    Author: Hailemariam Arega
    ID: UGR/7412/12
    Section: 3'''
import random
import os

#Our original BOX. It will be used as an input to our prepareforMerge function and and the launchGame. The rest will use the newList as instructed in the question.
box = [
    [0, 0, 0, 0],
    [0, 0, 0, 0],
    [0, 0, 0, 0],
    [0, 0, 0, 0]]

#########################################      CHECKS WHETHER OR NOT THE INPUT LISTS ARE EQUAL     ###################################################
def checkEquality(newList, box):
    '''This function is used to check whether or not the number on the box changed. If so we will use it to generate 2 if not 2 won't be generated'''
    itMoved = False # this is used to see whether or not the player's action (respose) actually moved the numbers around. This is later used when generating 2.
    for i in range(0, 4):
        for j in range(0, 4):
            if(newList[i][j] != box[i][j]):
                itMoved = True
    return itMoved

#########################################       PRINTS THE BOX IN A FORMATED WAY     ###################################################################
def printBox(newList):
    '''Formats the display for the 2048 box'''
    print("\n===============    2048    ===============")
    for i in range(0, 4):
        for j in range(0, 4):
            # print("|", end="")
            if(newList[i][j] == 0):
                print("|", " "*8, end="")
            elif(newList[i][j] < 10):
                print("|", " "*3, newList[i][j], " "*2, end="")
            elif(newList[i][j] < 100):
                print("|", " "*2, newList[i][j], " "*2, end="")
            elif(newList[i][j] < 1000):
                print("|", " "*2, newList[i][j], " "*1, end="")
            else:
                print("|", " ", newList[i][j], " ", end="")
        print("|")


#########################################       GENERATES TWO NUMBERS     ############################################################################## 
def generateTwoAt(emptyPlaces, newList, possibleMove, itMoved):
    '''Generates 2 on every move at the indexes with 0 value'''
    if(emptyPlaces == [] and possibleMove == False):
        return 2
    elif(emptyPlaces != [] and itMoved):
        position = random.choice(emptyPlaces)
        #reading the list saved in position and adusting the variables i use later on as indeces to print my random 2
        i = position[0]
        j = position[1]
        newList[i][j] = random.choice([2, 2, 2, 4]) # on average it returns 2 75% of the time and 25% of the time it returns 4
        return 0

#########################################       TRACKS THE EMPTY LISTS      #############################################################################
def trackEmptyAndScore(newList):
    '''Keeps track of which value in the current box is empty (occupied by zero) and the score of the current box. Meaning it saves the indexes of the LIST where the values are zero and returns a tuple containing the empties and the score'''
    empty = []
    score = 0

    for i in range(0, 4):
        for j in range(0, 4):
            if(newList[i][j] > score):
                score = newList[i][j]
            if(newList[i][j] == 0):
                empty.append([i, j])
            if(j < 3 and i < 3):
                #This is to keep track whether or not there are valid moves left
                if((newList[i][j] == newList[i][j + 1]) or(newList[i][j] == newList[i + 1][j])):
                    possibleMove = True
                else:
                    possibleMove = False
    return empty, score, possibleMove

############################  REVERSES THE ROWS OF THE INPUT  #############################################################################################
def reverseRow(newList):
    '''Reverses the row of the nested list it accepts'''
    for i in newList:
        i.reverse()

########################   PREPARES A COPY LIST WHERE THE MERGING HAPPENS    ################################################################################

def prepareForMerge(box, orientation = "horizontal"):
    '''This function copys the original nested list disregarding elements with zero value. It also transposes it if the orientation parameter was passed a 'vertical'           argumentThen finally it merges the values having similar value.'''
    
    #HERE I AM USING A NEWLIST AT YOUR (SIR KABILA) BEHEST. SINCE YOU ORDERED US TO NOT MANUPILATE THE INPUT BOX (NESTED LIST).
    newList = [[], [], [], []]

    #for the values different from zero, this iteration appends it to the respective nested list in the new List. And it transposes the list if the orientation is changed. 
    if(orientation == "horizontal"):
        for i in range(0, 4):
            for j in range(0,4):
                if(box[i][j] != 0):    
                    newList[i].append(box[i][j])
    
    if(orientation == "vertical"):
        for i in range(0, 4):
            for j in range(0, 4):
                newList[i].append(box[j][i])
   
    #appends zero to the end of the lists preparing it for the next and final merging step
    for i in range(0, 4):
        while(len(newList[i]) < 4):
            newList[i].append(0)
    return newList

########################   MERGES THE NESTED LOOPS TO THE LEFT    ############################################################################################

def mergeLeft(newList, box):
    '''merges the similar values and append zero to account for ones getting added and then poped'''
    
    for i in range(0, 4):
        for j in range(0, 3): # Not going to 4 since we check with the next element
            if(newList[i][j] != 0 and newList[i][j] == newList[i][j+1]): # adding a check for ZERO value may be doable. CHECK IT!
                newList[i][j] = newList[i][j] * 2
                newList[i].pop(j + 1)
                newList[i].append(0)
    

###############################     IMPLEMENTATION      ####################################################################################################

def launchGame(response, box):
    '''The main part of the game, where the player is asked to respond with letters to move the tiles around'''

    if(response == "w"):
        #merges the numbers upward
        newList = prepareForMerge(box, "vertical")
        newList = prepareForMerge(newList)
        mergeLeft(newList, box)
        newList = prepareForMerge(newList)
        newList = prepareForMerge(newList, "vertical")
        itMoved = checkEquality(newList, box)
        emptyAndScore = trackEmptyAndScore(newList) # Saves the list containing empty indexes from the function keeping track of the ZEROS
        boxIsFull = generateTwoAt(emptyPlaces=emptyAndScore[0], newList=newList, possibleMove=emptyAndScore[2], itMoved=itMoved)

    elif(response == "a"):
        #merges the numbers to the left
        newList = prepareForMerge(box)
        mergeLeft(newList, box)
        newList = prepareForMerge(newList) # the prep needs to be called everytime after merge to rearrange the box
        itMoved = checkEquality(newList, box)
        emptyAndScore = trackEmptyAndScore(newList)
        boxIsFull = generateTwoAt(emptyPlaces=emptyAndScore[0], newList=newList, possibleMove=emptyAndScore[2], itMoved=itMoved)

    elif(response == "d"):
        #merges the numbers to the right
        newList = prepareForMerge(box)
        reverseRow(newList)
        mergeLeft(newList, box)
        newList = prepareForMerge(newList)
        reverseRow(newList)
        itMoved = checkEquality(newList, box)
        emptyAndScore = trackEmptyAndScore(newList)
        boxIsFull = generateTwoAt(emptyPlaces=emptyAndScore[0], newList=newList, possibleMove=emptyAndScore[2], itMoved=itMoved)

    elif(response == "s"):
        #merges the numbers downwards
        newList = prepareForMerge(box, "vertical")
        newList = prepareForMerge(newList)
        reverseRow(newList)
        mergeLeft(newList, box)
        newList = prepareForMerge(newList)
        reverseRow(newList)
        newList = prepareForMerge(newList, "vertical")
        itMoved = checkEquality(newList, box)
        emptyAndScore = trackEmptyAndScore(newList)
        boxIsFull = generateTwoAt(emptyPlaces=emptyAndScore[0], newList=newList, possibleMove=emptyAndScore[2], itMoved=itMoved)
    elif(response == "q"):
        print("YOU QUIT?! WHAT A WUSS ...")
        return 1
    
    try:
        _ = os.system("cls")
        #Prints the box after each move
        print("\nFor those who aren't Gamers: w = upward move  a = left move  d = right move  s = downward move   q = quit")
        print("Score: ",emptyAndScore[1], "\n")
        printBox(newList)
        if(boxIsFull == 2):
            print("BOX IS FULL BETTER LUCK NEXT TIME HAHA!")
            return 2 # return code for our of moves
        return newList
    except:
        print("INVALID MOVE")
        return 1 # return code for invalid move


# This part initializes the game and runs only once
emptyAndScore = trackEmptyAndScore(box)
boxIsFull = generateTwoAt(emptyPlaces=emptyAndScore[0], newList=box, possibleMove=emptyAndScore[2], itMoved=True)
emptyAndScore = trackEmptyAndScore(box)
boxIsFull = generateTwoAt(emptyPlaces=emptyAndScore[0], newList=box, possibleMove=emptyAndScore[2], itMoved=True)
print("\nFor those who aren't Gamers: w = upward move  a = left move  d = right move  s = downward move   q = quit")
printBox(box)

################################       GAME'S MAINLOOP      ##################################################################################################
while(True):
    response = input("Enter your move: ")
    box = launchGame(response, box) #Finally updating the box list for next move
    if(box == 1 or box == 2):
        break