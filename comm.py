import os
import webbrowser
from datetime import datetime

def getCurTime():
    # current date and time
    curDT = datetime.now()
    date_time = curDT.strftime('%Y-%m-%d %H:%M:%S')
    return date_time

def getTimeDiff(s1, s2):
    t1=datetime.strptime(s1,'%Y-%m-%d %H:%M:%S')
    t2=datetime.strptime(s2,'%Y-%m-%d %H:%M:%S')
    delta = t2 - t1
    return delta.total_seconds()
    
def getShortName(name):
    if len(name) > 5 and name != "Computer":
        return name[0:5]
    else:
        return name

def Ignore0(data):
    if data == 0 :
        return ""
    else:
        return str(data)
        
def getMin(data):
    if len(data) < 1 :
        return 0
    wkData=[]
    for d in data:
        if d > 0:
            wkData.append(d)
    return min(wkData)

def getMax(data):
    if len(data) < 1 :
        return 0    
    return max(data)

def getSum(data):
    if len(data) < 1 :
        return 0    
    return sum(data)
          
def openFileByOS(filePath):
    errorMsg = ""
    try:
        print("webbrowser,filePath=" + filePath)
        #os.system(filePath)  
        #os.startfile(filePath)
        #open(filePath)
        #subprocess.Popen(filePath)
        webbrowser.open_new(filePath)
        print("subprocess done")
    except:
        errorMsg = "File Not Found"
        print(errorMsg)
        
    return errorMsg
        
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            
                    
                                
