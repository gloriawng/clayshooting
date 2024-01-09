import os
import pickle
import comm

def pagingButton(btnCaption,position):
    fill(255, 0, 0)
    rect(position[0], position[1], 40, 40)
    fill(0)
    strokeWeight(5)
    textSize(40)
    text(btnCaption, position[0] + 20 ,position[1] + 30)
    
def createReportData(historyData):
    reportData = []
    idx = 0
    for gameData in historyData:
        idx += 1
        reportLine = []
        clays = gameData[2]
        
        claysA = clays[1]
        claysB = clays[2]
        
        targetedTimesA = []
        targetedTimesB = []

        for clay in claysA:
            targetedTimesA.append(abs(comm.getTimeDiff(clay.shotdownTime,clay.threwtime)))
            
        for clay in claysB:
            targetedTimesB.append(abs(comm.getTimeDiff(clay.shotdownTime,clay.threwtime)))
            
        reportLine.append(idx)  # IDX   
        reportLine.append(gameData[0])  # player1
        reportLine.append(gameData[1])  # player2
        reportLine.append(len(claysA))  # player1Num
        reportLine.append(len(claysB))  # player2Num
        
        if len(targetedTimesA) > 0 :
            reportLine.append(sum(targetedTimesA))    # player1TotalT -> reportLine[5]  
            if len(targetedTimesA) > 0:
                reportLine.append((1.0 * comm.getSum(targetedTimesA)) / (1.0 * len(targetedTimesA))) # player1AveT -> reportLine[6]  
            else:
                reportLine.append(0)
                
            reportLine.append(comm.getMin(targetedTimesA))    # player1MinT  -> reportLine[7] 
            reportLine.append(comm.getMax(targetedTimesA))    # player1MaxT  -> reportLine[8] 
        else:
            reportLine.append(0)    # player1TotalT
            reportLine.append(0)    # player1AveT
            reportLine.append(0)    # player1MinT
            reportLine.append(0)    # player1MaxT
            
        if len(targetedTimesB) > 0 :
            reportLine.append(sum(targetedTimesB))    # player2TotalT  -> reportLine[9]   
            if len(targetedTimesB) > 0:
                reportLine.append((1.0 * comm.getSum(targetedTimesB)) / (1.0 * len(targetedTimesB))) # player2AveT   -> reportLine[10]   
            else:
                reportLine.append(0)
                
            reportLine.append(comm.getMin(targetedTimesB))    # player2MinT   -> reportLine[11]   
            reportLine.append(comm.getMax(targetedTimesB))    # player2MaxT   -> reportLine[12]   
        else:
            reportLine.append(0)    # player2TotalT
            reportLine.append(0)    # player2AveT
            reportLine.append(0)    # player2MinT
            reportLine.append(0)    # player2MaxT
                
        reportLine.append(comm.getMax([len(claysA), len(claysB)]))             #reportLine[13]   -> Clay Num
        reportLine.append(format(comm.getMax([comm.getSum(targetedTimesA), comm.getSum(targetedTimesB)])))        #reportLine[14]    -> Total Shooting time      
        reportLine.append(format(comm.getMax([reportLine[5], reportLine[9]])))        #reportLine[15]       -> Min Average Shooting time         
        reportLine.append(format(comm.getMin([comm.getMin(targetedTimesA), comm.getMin(targetedTimesB)])))        #reportLine[16]       -> Min Shooting time
        reportLine.append(format(comm.getMax([comm.getMax(targetedTimesA), comm.getMax(targetedTimesB)])))        #reportLine[17]       -> Max Shooting time
           
        #print(reportLine)
        #Only show the best record
        reportData.append(reportLine)
        
    return reportData

def loadGameHistry(path):
    FileNotFoundMessage = ""
    data = []
    db={}
    try:
        dbfile = open(path, 'rb')    
        db = pickle.load(dbfile)
        dbfile.close()
        FileNotFoundMessage=""
    except:
        #print("Error: " + path + " not found")
        FileNotFoundMessage="File Not Found"
        
    for keys in db:
        if keys=='1':
            data = db['1']
            
    #print("loadGameHistory data:" + str(data))
    return [FileNotFoundMessage, data]
       
def format(d):
    return round(d,2)

def saveGameHistry(path, name1, name2, shootdownClays):
    db={}   
    data1 = [] #All lines are here
    data1 = loadGameHistry(path)[1]
    dbfile = open(path, 'wb')
    
    #Remvoe image before saving
    for i in range(2):
        for shootdownClay in  shootdownClays[ i + 1 ]:
            shootdownClay.img = None
    
    data1.append([name1, name2, shootdownClays])

    db['1']= data1   
    pickle.dump(db, dbfile)   
    dbfile.close()  
