import os, random, pickle, sys, math, copy

import comm
import report
from gameObject import GameObject

screenW = 1000
screenH = 1000
screenFrameRate = 60
#GameInstructionFilePath = "C:\\Users\\marke\\Downloads\\hunting\\clayshooting\\data\\GameInstruction.pdf"
GameInstructionFilePath = "GameInstruction.pdf"
resultFilePath = "gameHistoyData.dat"
rowsPerReport = 5
curReportPageIndex = 1
nTotalReportPages = 0

flyingAreaBottomH = 50  #The RECT on Screen bottom
flyingAreaTopH = 100  #The RECT on Screen bottom
boothWidth = 100
playerHeight = 100
bulletsNum = 5
claysNum = 5
claySize = 40
bulletSize = [8, 40]
gunSize = [100, 20]  

bulletSpeed = 20
screenFrameRateclayFlyingSeconds = 3

# All targeted bullets and the clays that are shot down  
shootdownClays = {1: [], 2: []} 
bullets = {1: [], 2: []} 
clays = {1: [], 2: []} 
flyingBullets = []
flyingClays = []

#1: Homescreen 2: Instructions 3: nameScreen 4: scores 8: Game Type Selection screen;
#10->Welcome; 12->Name input screens; 13-17-> Game report  
#20->Game Init Screen;  21->playing; 22-> show game result
screenShow = 1

playWithComputerOption = 0  # 1 -> Play with computer; 2 -> Two players 
playerAwinsNum = 0
playerBwinsNum = 0
playerAName = ""
playerBName = ""
gameResultSaved = False
gameStart = False
gameReportData = []
gameHistoryData = []
FileNotFoundMessage = ""
drop = False
p1Turn = True

#Dropdown menu
#main windows  
def dropMenu():
    global drop
    fill(40)
    strokeWeight(1)
    rect(800, 30, 170, 100)
    fill("#dc2f06")
    textSize(width / 20)
    text("MENU", 885, 95)
    if mouseX >= 800 and mouseX <= 970 and mouseY >= 30 and mouseY <= 130:
        drop = True
    if drop and mouseX >= 800 and mouseX <= 970 and mouseY >= 30 and mouseY <= 400:
        fill(100)
        rect(800, 130, 170, 270)
        fill(40)
        rect(825, 150, 120, 50)
        rect(825, 210, 120, 50)
        rect(825, 270, 120, 50)
        rect(825, 330, 120, 50)
        fill("#dc2f06")
        textSize(width / 40)
        text("HELP", 885, 185)
        text("SCORES", 885, 245)
        text("HOME", 885, 305)
        text("QUIT", 885, 365)
        
        
def startScreen():
    textSize(150)
    fill(255, 0, 0)
    rect(350, 550, 300, 60)
    rect(410, 650, 170, 60)
    playButton("PLAY")
    text("Instructions", width / 2, width / 2 + 100)
    text("Scores", width / 2, width - (width / 2.5) + 100)

#choose to play with Computer or 2 players
def gameOptionScreen():
    global screenW, screenH, playerBName, playWithComputerOption, reportImage, reportImage2, reportImage3
    background(0)
    image(reportImage3, 0, 0)  
    fill(255, 255, 255) 
    textSize(60)
    text("How to play?", screenW / 2, 200)   
    textSize(40)    
    fill(255,0,0)
    rect(screenW / 2 - 230, screenW / 3 -35, 470,45)    
    fill(255,255,255)        
    text("Play with Computer", screenW / 2, screenW / 3)
    
    fill(255,0,0)
    rect(screenW/2 - 230, screenW / 3 + 65, 470,45)    
    fill(255,255,255)        
    text("Play with another player", screenW / 2, screenW / 3 + 100)
    
def nameScreen():
    global screenW, screenH, playerAName, playerBName, playWithComputerOption, reportImage, reportImage2, reportImage3
    background(0)
    image(reportImage3, 0, 0)  
    fill(255, 255, 255) 
    textSize(40)
    msglabel = "Input Name1,press ENTER to input Name"
    if playWithComputerOption == 1:
        textSize(50)
        msglabel = "Input your Name and Press PLAY"
    text(msglabel, screenW / 2, 200)
    
    text("Player 1: " + playerAName, screenW / 2, screenW / 3)
    if not playWithComputerOption == 1:
        text("Player 2: " + playerBName, screenW / 2, screenW / 3 + 100)
    playButton("PLAY")
              
def gameEndScreen():
    global screenW, screenH, gun1, gun2, claySize
    global reportImage,reportImage2,reportImage3
    global shootdownClays, playerAName, playerBName, playerAwinsNum, playerBwinsNum

    background(255,255,255)
    image(reportImage3, 0, 0)  
    fill(255, 255, 255) 
    textSize(50)
    label1 = playerAName + " and " + playerBName + " are tie !"   
    playerAwinsNum = len(shootdownClays[1])
    playerBwinsNum = len(shootdownClays[2])
    if playerAwinsNum > playerBwinsNum :
        label1 = playerAName + " Win !"    
    if playerBwinsNum > playerAwinsNum :
        label1 = playerBName + " Win !"
    text(label1, screenW/2, 100)     
    
    textSize(15) 
    label2 = playerAName + " ( " + str(playerAwinsNum) + " : " + str(playerBwinsNum) + " ) " +  playerBName            
    text(label2, screenW/2, 140)

    if True:
        textSize(40)
        text("Shotdown Clays" , screenW/2 -50, gun1.position[1] - 300)
        textSize(30)
        text(playerAName, 100, gun1.position[1] - 200)
        idx = 0
        for shootdownClay in shootdownClays[1]:
            shootdownClay.speedY = 0
            shootdownClay.speed = 0
            shootdownClay.Rotate = 0
            shootdownClay.position = [claySize/2 + idx * claySize, gun1.position[1] - 150]
            shootdownClay.show()
            idx += 1    
        text(playerBName, screenW - len(playerBName) * 15, gun1.position[1] - 200)    
        idx = 0    
        for shootdownClay in shootdownClays[2]:
            shootdownClay.speedY = 0
            shootdownClay.speed = 0
            shootdownClay.Rotate = 0
            shootdownClay.position = [screenW - (claySize/2 + idx * claySize), gun2.position[1] - 150]
            shootdownClay.show() 
            idx += 1  
            
    playButton("REPLAY")        
            
def scoreScreen():
    global screenW, screenH, screenFrameRate, boothWidth, flyingAreaBottomH, flyingAreaTopH, screenShow, gun1, gun2, playerHeight, bullets, flyingBullets, bulletSpeed, bulletSize, gunSize, claySize, clays, flyingClays, screenFrameRate, screenFrameRateclayFlyingSeconds
    global shootdownClays,  flyingBullets, flyingClays
    global reportImage
    
    menuSpace = 80
    menuLeft1 = 100             
    menuLeft2 = 120      
    barWidth = 20
                
    background(0, 0, 255)
    image(reportImage, 0, 0)  
    image(reportImage, 0, 680)  
    textAlign(CENTER)
    
    textSize(50)
    text("Scores", screenW/2, 60 )

    textAlign(LEFT)
    
    textSize(20)
    fill(255,0,0)
    yAdj=100
    rect(menuLeft2, menuSpace * 3-122, 370,30)    
    fill(255)         
    text("1. Show All(Order By Player1 Name)  ", menuLeft2, menuSpace * 3-yAdj)

    fill(255,0,0)
    rect(menuLeft2, menuSpace * 4-122, 370,30)    
    fill(255)        
    text("2. Show All(Order By Player2 Name)  ", menuLeft2, menuSpace * 4-yAdj)
    
    fill(255,0,0)
    rect(menuLeft2, menuSpace * 5-122, 500,30)    
    fill(255)      
    text("3. Show All(Order By The Shot down Clay Number)  ", menuLeft2, menuSpace * 5-yAdj)
    
    fill(255,0,0)
    rect(menuLeft2, menuSpace * 6-122, 450,30)    
    fill(255)    
    text("4. Show All(Order By The Average Shoot Time)  ", menuLeft2, menuSpace * 6-yAdj)   
    
    fill(255,0,0)
    rect(menuLeft2, menuSpace * 7-122, 410,30)    
    fill(255)        
    text("5. Show All(Order By The Fastest Shoot)  ", menuLeft2, menuSpace * 7-yAdj)

                                
def showReportScreen(OrderBy):
    global screenW, screenH, screenFrameRate, boothWidth, flyingAreaBottomH, flyingAreaTopH, screenShow, gun1, gun2, playerHeight, bullets, flyingBullets, bulletSpeed, bulletSize, gunSize, claySize, clays, flyingClays, screenFrameRate, screenFrameRateclayFlyingSeconds
    global shootdownClays,  flyingBullets, flyingClays
    global gameReportData, gameHistoryData 
    global reportImage,reportImage3
    global rowsPerReport, curReportPageIndex, nTotalReportPages

    menuSpace = 80
    menuLeft1 = 100             
    menuLeft2 = 120      
    barWidth = 20
        
    background(0, 0, 255)
    image(reportImage3, 0, 0)  
    image(reportImage3, 0, 660)  

    #Show report paging buttons
    nTotalReportPages = int(math.ceil((1.0 * len(gameReportData)) / (1.0 * rowsPerReport)))    
    if nTotalReportPages > 1:
        if curReportPageIndex > 1:
            report.pagingButton("<",[screenW/2 - 200,55])
              
        if curReportPageIndex < nTotalReportPages:
            report.pagingButton(">",[screenW/2 - 100,55])
        
    textAlign(LEFT)
    fill(255,0,0)
    fill(255,255,255)    
    textSize(40)     
            
    if OrderBy == "By Name1":        
        text("Report- Order By Player1 Name", 20,40)  
        #print(gameReportData)
              
        gameReportData.sort(key = lambda x:x[1])
               
    elif OrderBy == "By Name2":        
        text("Report- Order By Player2 Name", 20,40)
        gameReportData.sort(key = lambda x:x[2])   

    elif OrderBy == "By Clay Number":
        #print(" By Clay Number")       
        text("Report- Order By The Clay Number", 20,40)
        gameReportData.sort(key = lambda x:x[13]) 
        
    elif OrderBy == "By The Average Shoot Time":        
        text("Report- Order By The Average Shoot Time", 20,40)
        gameReportData.sort(key = lambda x:x[15])   

    elif OrderBy == "By The Fastest Shoot":        
        text("Report- Order By The Fastest Shoot", 20,40)
        gameReportData.sort(key = lambda x:x[16])        
                                   
    textSize(13)
    lineNum = 4
    lineSpace = 30
    colWidthUnit = 39
    textAlign(LEFT)

    #REPORT HEAD
    text("ID",3,lineSpace * lineNum)
    text("PlayA",20 ,lineSpace * lineNum)
    text("Result",colWidthUnit*2.5 ,lineSpace * lineNum)
    #text("",colWidthUnit * 2 ,lineSpace * lineNum)
    text("PlayB",colWidthUnit * 4 ,lineSpace * lineNum)        
    text("Total(Secs)",colWidthUnit * 6 ,lineSpace * lineNum)
    text("Min",colWidthUnit * 8.5 ,lineSpace * lineNum)
    text("Average",colWidthUnit * 10 ,lineSpace * lineNum)
    text("TotalA",colWidthUnit * 11.5 ,lineSpace * lineNum)
    text("MinA",colWidthUnit * 13 ,lineSpace * lineNum)
    text("AvgA",colWidthUnit * 14.5 ,lineSpace * lineNum)
    text("TotalB",colWidthUnit * 16 ,lineSpace * lineNum)
    text("MinB",colWidthUnit * 17.5 ,lineSpace * lineNum)
    text("AvgB",colWidthUnit * 19 ,lineSpace * lineNum)
    
    rowid = 0
    for row in gameReportData:
        rowid += 1        
        if rowid > rowsPerReport * (curReportPageIndex - 1) and rowid <= rowsPerReport * curReportPageIndex :
            lineNum += 1
            text(row[0],3,lineSpace * lineNum)
            text(row[1],20 ,lineSpace * lineNum)
            text(str(row[3]) + ":" + str(row[4]),colWidthUnit * 3 ,lineSpace * lineNum)
            text(row[2],colWidthUnit * 4 ,lineSpace * lineNum)        
            text(str(row[14]),50 + colWidthUnit * 6 ,lineSpace * lineNum)
            text(str(row[16]),colWidthUnit * 9 ,lineSpace * lineNum)
            text(str(row[15]),colWidthUnit * 10 ,lineSpace * lineNum)
            text(comm.Ignore0(row[5]),colWidthUnit * 11.5 ,lineSpace * lineNum)
            text(comm.Ignore0(row[7]),colWidthUnit * 13 ,lineSpace * lineNum)
            text(comm.Ignore0(report.format(row[6])),colWidthUnit * 14.5 ,lineSpace * lineNum)
            text(comm.Ignore0(report.format(row[9])),colWidthUnit * 16 ,lineSpace * lineNum)
            text(comm.Ignore0(report.format(row[11])),colWidthUnit * 17.5 ,lineSpace * lineNum)
            text(comm.Ignore0(report.format(row[10])),colWidthUnit * 19 ,lineSpace * lineNum)
    
    textAlign(CENTER)
                                                                                                                
def playButton(btnCaption):
    fill(255, 0, 0)
    rect(430, 765, 140, 60)
    fill(0)
    strokeWeight(5)
    if btnCaption == "REPLAY":
        textSize(40)
    else:
        textSize(50)
        
    text(btnCaption, width / 2, width - (width / 3.5) + 100)
   
   
#Recursive "AI"
def bulletTowardToClay(clay, bullet, frameCount):
    global screenFrameRate
    ret = frameCount
    if abs(bullet.position[0] - clay.position[0]) <= 15 :
         return ret
     
    if bullet.position[0] < 0 or bullet.position[0] > screenW or clay.position[0] < 0 or clay.position[0] > screenW :
        return ret
    
    bullet.position[0] = 1.0 * bullet.position0[0] - 1.0 * bullet.speedX *  bullet.xdir * ret
    clay.position[0] = clay.position0[0] + int((1.0 * clay.speedX) / (1.0 * screenFrameRate) * (1.0* clay.xdir * ret))  
    ret += 1

    return bulletTowardToClay(clay, bullet, ret)
      
def computerShoot():
    global screenW, screenH, screenFrameRate, boothWidth, flyingAreaBottomH, flyingAreaTopH, screenShow, gun1, gun2, playerHeight, bullets, flyingBullets, bulletSpeed, bulletSize, gunSize, claySize, clays, flyingClays, screenFrameRate, screenFrameRateclayFlyingSeconds
    global shootdownClays,  flyingBullets, flyingClays
    #,bulletSpeed
    
    if len(bullets[2]) > 0:
        bullet2 = copy.copy(bullets[2][0])       
        bullet2.position = [ gun2.position[0] - (gunSize[0]/2) * cos(radians(abs(gun2.Rotate))) , gun2.position[1] - (gunSize[0]/2) * sin(radians(abs(gun2.Rotate))) - 5 ]
        bullet2.position0 = [ gun2.position[0] - (gunSize[0]/2) * cos(radians(abs(gun2.Rotate))) , gun2.position[1] - (gunSize[0]/2) * sin(radians(abs(gun2.Rotate))) - 5 ]
        bullet2.Rotate = abs(gun2.Rotate) - 90
        bullet2.speed = bulletSpeed
        bullet2.speedX= bullet2.speed * cos(radians(90 - abs(bullet2.Rotate)))
        
        #Computer shoot 
        bComputerShoot = True
        for flyingBullet in flyingBullets:
            if flyingBullet.player == 2:
                bComputerShoot = False;
        
        if bComputerShoot == True:                        
            for flyingClay in flyingClays : 
                if flyingClay.ydir > 0: #Computer only shoot after the clay reached the TOP position (Otherwise is's not fair to a human)
                    #in this frame count, both bullet and clay will have same X position
                    clay = copy.copy(flyingClay)
                    clay.position0=[flyingClay.position0[0],flyingClay.position0[1]]
                    clay.position=[flyingClay.position[0],flyingClay.position[1]]
                    timeCounter = 0
                    timeCounter = bulletTowardToClay(clay,bullet2,timeCounter)                    
                    
                    if flyingClay.player == 1:
                        adj = 10
                    else:
                        adj = 33
                        
                    if  flyingClay.frameCount  == int(timeCounter * 2.5) + adj:
                        fire(2)

            
def checkResult():
    global screenW, screenH, screenFrameRate, boothWidth, flyingAreaBottomH, flyingAreaTopH, screenShow, gun1, gun2, playerHeight, bullets, flyingBullets, bulletSpeed, bulletSize, gunSize, claySize, clays, flyingClays, screenFrameRate, screenFrameRateclayFlyingSeconds, shootdownClays, flyingBullets, flyingClays
    global playWithComputerOption
    if screenShow == 21:
        if playWithComputerOption == 1:
            computerShoot()
        
        for bullet in flyingBullets:
            if bullet.player == 1:
                bulletX = bullet.position[0] + (bulletSize[1] / 2.0) * cos(radians(90 - abs(bullet.Rotate)))
            else:
                bulletX = bullet.position[0] - (bulletSize[1] / 2.0) * cos(radians(90 - abs(bullet.Rotate)))
            
            bulletY = bullet.position[1] - (bulletSize[1] / 2.0) * sin(radians(90 - abs(bullet.Rotate)))
            
            for flyingClay in flyingClays:                
                if pow(bulletX - flyingClay.position[0], 2 ) +  pow( bulletY - flyingClay.position[1], 2 ) < pow( claySize / 2.0, 2):
                    flyingClay.shotdownTime = comm.getCurTime()
                    if bullet.player == 1:
                        shootdownClays[1].append(flyingClay)
                    else:
                        shootdownClays[2].append(flyingClay) 
                
                    flyingClays.remove(flyingClay)
                    flyingBullets.remove(bullet)
          
        #show all shutdown clays in each player's side
        idx = 0
        for shootdownClay in shootdownClays[1]:
            shootdownClay.speedY = 0
            shootdownClay.speed = 0
            shootdownClay.Rotate = 0
            shootdownClay.position = [claySize/2 + idx * claySize, gun1.position[1] + 80]
            shootdownClay.show()
            idx += 1
            
        idx = 0    
        for shootdownClay in shootdownClays[2]:
            shootdownClay.speedY = 0
            shootdownClay.speed = 0
            shootdownClay.Rotate = 0
            shootdownClay.position = [screenW - (claySize/2 + idx * claySize), gun1.position[1] + 80]
            shootdownClay.show() 
            idx += 1        

        #Game is over once all bullets went out, and the flying clay was shotdown or fell down on ground            
        if len(bullets[1]) + len(bullets[2]) == 0 and len(flyingClays) == 0: 
            screenShow = 22
                                                                                                                                                                                                                                                                                                                                                                                                
def loadClays(player):
    global screenW, screenH, claysNum, clays, claySize, bulletSize, gunSize
    
    if player < 1 or player > 2 :
        loadClays(1)
        loadClays(2)
    else:
        wlClays = []
        clay_img1 = loadImage("clay1.png")
        clay_img = loadImage("clay.png")
        clay_img1.resize(claySize, claySize)
        clay_img.resize(claySize, claySize)
        
        ypos = screenH - flyingAreaBottomH - claySize/2
        
        idx = 0    
        for i in range(claysNum):    
            if player == 1:
                idx =  i + 1     
                xpos = int(screenW / 2) - ( int(claySize / 2) +   i  * claySize)
                clay = GameObject(idx, [xpos , ypos], 0, clay_img1)
            else:
                idx = claysNum + i + 1   
                xpos = int(screenW / 2) + (claySize/2 +   i * claySize )
                clay = GameObject(idx, [xpos , ypos], 0, clay_img)
                
            
            clay.player = player
            wlClays.append(clay)

        clays[player] = wlClays
                
def loadBullets(player):
    global bulletsNum, bullets, bulletSize, gunSize
    
    if player < 1 or player > 2 :
        loadBullets(1)
        loadBullets(2)
    else:    
        bullet_img = loadImage("bullet.png")
        bullet_img.resize(bulletSize[0], bulletSize[1])
        xpos = 10
        ypos = screenH - flyingAreaBottomH - playerHeight/2
        if player == 1:
            bullets[1] = []
        else:
            bullets[2] = []
            xpos = screenW - 10
        
        idx = 0    
        for i in range(bulletsNum):
            idx = i * bulletsNum + i + 1
            if player == 1:
                bullet = GameObject(idx, [xpos + i * (bulletSize[0]) , ypos], 0, bullet_img)
            else:
                bullet = GameObject(idx, [xpos - i * (bulletSize[0]) , ypos], 0, bullet_img)
            bullet.player = player
                        
            if player == 1:                
                bullets[1].append(bullet)
            else:
                bullets[2].append(bullet)

             
#Decide the Initial Speed V0(Vx, Vy). Make sure it only flys some seconds
#The highest position should be within the screen, and not lower than 70% of ScreenH
#The clay must fall down on the floor of screen                                                                               
def setClayInitialSpeed(clay):
    global screenW, screenH, screenFrameRate, boothWidth, flyingAreaBottomH, flyingAreaTopH, screenShow, gun1, gun2, playerHeight,bullets, flyingBullets, bulletSpeed, bulletSize, gunSize, clays, flyingClays, screenFrameRate, screenFrameRateclayFlyingSeconds
    
    clay.speedX = random.randint(1, 1)
    
    maxFlyingHeigh = screenH #- clay.position[1]
    minFlyingHeigh = int(0.95 * maxFlyingHeigh)    
    flyingHeigh = random.randint(minFlyingHeigh, maxFlyingHeigh)
    
    #The average Y change rate /screenframe
    #clay.speedY = int (5.5 * flyingHeigh / (clayFlyingTime * screenFrameRateclayFlyingSeconds )) 
    clay.speedY =   ((1.000000) * flyingHeigh) / (1.0 * screenFrameRateclayFlyingSeconds) 
    print("clay.speedY=" + str(clay.speedY))
    
                                            
def throwClay():
    global screenW, screenH, screenFrameRate, boothWidth, flyingAreaBottomH, flyingAreaTopH, screenShow, gun1, gun2, playerHeight,bullets, flyingBullets, bulletSpeed, bulletSize, gunSize, clays, flyingClays, screenFrameRateclayFlyingSeconds
    #print(random.randint(1, 2))
    wkClay = None
    
    #Randomly pickup the first clay, after then pickup a different color
    if ( len(clays[2]) > len(clays[1]) ) :
        wkClay = clays[2].pop()
    elif len(clays[2]) == len(clays[1]) and len(clays[2]) > 0 :    
        wkClay = clays[random.randint(1, 2)].pop()
    elif len(clays[1]) > 0:
        wkClay = clays[1].pop()            
    
    if wkClay != None:
        wkClay.speed = random.randint(7, 9)
        wkClay.threwtime = comm.getCurTime()    

        #Flying from left to right
        if wkClay.player == 1:
            wkClay.position[0] = int(0.25 * screenW)
            wkClay.xdir = 1
        
        #Flying from right to left
        else:
            wkClay.position[0]  = int(0.75 * screenW)
            wkClay.xdir = -1
        
        #throw from the middle of each side
        wkClay.ydir = 1

        wkClay.position0 = [wkClay.position[0],wkClay.position[1]]
        
        #How far away this clay will be
        setClayInitialSpeed(wkClay) 
                   
        
        #Throw it
        flyingClays.append(wkClay)
        
def fire(gunId):
    global screenW, screenH, boothWidth, flyingAreaBottomH, flyingAreaTopH, screenShow, gun1, gun2, playerHeight,bullets, flyingBullets, bulletSpeed, bulletSize, gunSize    
    
    if gunId == 1:
        if len(bullets[1]) > 0 :            
            flyingBullet = bullets[1].pop()
            flyingBullet.position = [gun1.position[0] + (gunSize[0]/2) * cos(radians(abs(gun1.Rotate))) , gun1.position[1] - (gunSize[0]/2) * sin(radians(abs(gun1.Rotate))) - 5 ]
            flyingBullet.position0 = [gun1.position[0] + (gunSize[0]/2) * cos(radians(abs(gun1.Rotate))) , gun1.position[1] - (gunSize[0]/2) * sin(radians(abs(gun1.Rotate))) - 5 ]
            flyingBullet.Rotate = 90 - abs(gun1.Rotate)
            flyingBullet.speed = bulletSpeed
            flyingBullets.append(flyingBullet)
    if gunId == 2:
        if len(bullets[2]) > 0 :            
            flyingBullet = bullets[2].pop()
            flyingBullet.position = [ gun2.position[0] - (gunSize[0]/2) * cos(radians(abs(gun2.Rotate))) , gun2.position[1] - (gunSize[0]/2) * sin(radians(abs(gun2.Rotate))) - 5 ]
            flyingBullet.Rotate = abs(gun2.Rotate) - 90
            flyingBullet.speed = bulletSpeed
            flyingBullets.append(flyingBullet)            

def showGuns():
    global screenW, screenH, boothWidth, flyingAreaBottomH, flyingAreaTopH, screenShow, gun1, gun2, playerHeight,bullets, flyingBullets, bulletSize, gunSize
    
    gun1_img = loadImage("gun.png")
    gun1_img.resize(gunSize[0], gunSize[1])
    gun1 = GameObject(101, [50, screenH - flyingAreaBottomH - playerHeight], 0, gun1_img)
    gun1.Rotate = -45
    
    gun2_imge = loadImage("gun2.png")
    gun2_imge.resize(gunSize[0], gunSize[1])
    gun2 = GameObject(102, [screenW - 50,  screenH - flyingAreaBottomH - playerHeight], 0, gun2_imge)
    gun2.Rotate = 45
    
def setup():
    global screenW, screenH, screenFrameRate, boothWidth, flyingAreaBottomH, flyingAreaTopH, screenShow, gun1, gun2, playerHeight,bullets, flyingBullets
    global backgroundImage,reportImage,reportImage2, reportImage3
    
    backgroundImage = loadImage("main.png")  
    reportImage = loadImage("report.jpg") 
    reportImage2 = loadImage("report2.jpg") 
    reportImage3 = loadImage("report3.jpg")  
    size(screenW, screenH)
    fill(255,255,255)
    frameRate(screenFrameRate)
    textAlign(CENTER)   
    
def drawPlayGround():
    global screenW, screenH, boothWidth, flyingAreaBottomH, flyingAreaTopH, screenShow, gun1, gun2, playerHeight,bullets, flyingBullets, playerAName, playerBName, shootdownClays
    noFill()      
    rect(0, 0, screenW , flyingAreaTopH) #Player2 Screen TOP BAR
    rect(0, screenH - flyingAreaBottomH, screenW , flyingAreaBottomH) #Player2 Screen BOTTOM BAR
    rect(0, flyingAreaTopH, boothWidth , screenH - flyingAreaBottomH - flyingAreaTopH ) #Player1 bench
    rect(screenW - boothWidth  , flyingAreaTopH, screenW - 2 * boothWidth , screenH - flyingAreaBottomH - flyingAreaTopH ) #Player2 bench

    gun1.show()
    gun2.show()
    
    #Draw trigger area
    stroke(255,0,0)
    noFill()
    rect(gun1.position[0] - 10 , gun1.position[1] + 5, 15,15)
    rect(gun2.position[0] - 5 , gun2.position[1] + 5, 15,15)

        
    for bullet in bullets[1]:
        bullet.show()
    for bullet in bullets[2]:
        bullet.show()

    if screenShow >= 20:
        
        textAlign(CENTER) 
        fill(0,0,0)
        
        if screenShow == 20:
            fill(255, 0, 0)
            rect(450, 10, 100, 40)
            fill(0)
            strokeWeight(5)
            textSize(30)
            text("START", screenW/2, 40)
            #textSize(30)            
            #label = "START"            
            #text(label, screenW/2, 40)
        
        elif screenShow == 22:
            textSize(50)
            label1 = playerAName + " and " + playerBName + " are tie !"             
            layerAwinsNum = len(shootdownClays[1])
            layerBwinsNum = len(shootdownClays[2])
            if layerAwinsNum > layerBwinsNum :
                label1 = playerAName + " Win !"    
            if layerBwinsNum > layerAwinsNum :
                label1 = playerBName + " Win !"
            text(label1, screenW/2, 100)        
               
            textSize(15) 
            label2 = playerAName + " ( " + str(layerAwinsNum) + " : " + str(layerBwinsNum) + " ) " +  playerBName            
            text(label2, screenW/2, 140)           
                        
        textSize(18)
        
        fill(0,0,255)
        text( comm.getShortName(playerAName), 40, gun1.position[1] - 40)
        fill(255,0,0)
        text( comm.getShortName(playerBName), screenW - boothWidth + 40, gun2.position[1] - 40)
        fill(255,255,255)


def drawFlyingClaysAndBullets():
    global screenW, screenH, boothWidth, flyingAreaBottomH, flyingAreaTopH, screenShow, gun1, gun2, playerHeight,bullets, flyingBullets, clays, flyingClays, gameStart, screenFrameRate, screenFrameRateclayFlyingSeconds

    for flyingBullet in flyingBullets:
        if  flyingBullet.position[1] <= 0 or flyingBullet.position[0] >= screenW :
            flyingBullets.remove(flyingBullet)
            
    for flyingBullet in flyingBullets:
        flyingBullet.bulletShow()
    
    for i in range(2):     
        for clay in clays[ i+ 1 ]:
            clay.clayShow(screenFrameRate, screenFrameRateclayFlyingSeconds)

    for flyingClay in flyingClays:
        if  flyingClay.position[0] <= 0 or flyingClay.position[0] >= screenW or flyingClay.position[1] > screenH :
            flyingClays.remove(flyingClay)
    
    for flyingClay in flyingClays:
        flyingClay.clayShow(screenFrameRate, screenFrameRateclayFlyingSeconds)
    
    if gameStart == True and len(clays) == 0 and len(bullets) > 0:
        loadClays(3) 
                     
    if gameStart == True and (len(bullets[1]) + len(bullets[2])) > 0  and len(flyingClays) == 0:
        throwClay()
        
    elif gameStart == True and (len(bullets[1]) + len(bullets[2])) == 0:       
        gameStart = False
        
    if screenShow == 21 and (len(bullets[1]) + len(bullets[2])) == 0:
        screenShow = 21
        
      
def initGame():
    global screenW, screenH, screenFrameRate, boothWidth, flyingAreaBottomH, flyingAreaTopH, screenShow, gun1, gun2, playerHeight, bullets, flyingBullets, shootdownClays, clays, flyingClays, gameStart

    shootdownClays = {1: [], 2: []} 
    bullets = {1: [], 2: []} 
    clays = {1: [], 2: []} 
    flyingBullets = []
    flyingClays = []
    gameStart = False
        
    showGuns()
    
    # 1 -> Load Gun1; 2 -> Load Gun2; 3 -> Load both guns;
    loadBullets(3) 
      
    # 1 -> Load Play1 side; 2 -> Load Play2 side; 3 -> Load both side;    
    loadClays(3)

def gamingScreen():
    global screenW, screenH, boothWidth, flyingAreaBottomH, flyingAreaTopH, screenShow
    background(255,255,255)
    drawPlayGround()
    drawFlyingClaysAndBullets()
    
    checkResult()
 
def helpScreen():
    global GameInstructionFilePath
    comm.openFileByOS( GameInstructionFilePath)                                                                                                                                                                                                                                                 
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                
def draw():
    global screenW, screenH, boothWidth, flyingAreaBottomH, flyingAreaTopH, screenShow, drop
    global reportImage,reportImage3
    
    if screenShow < 10:
        background(255)
        image(backgroundImage, screenW - 949, 0)        
        
        if screenShow == 1:
            startScreen()
        elif screenShow == 2:
            helpScreen()            
        elif screenShow == 3:
            nameScreen()
        elif screenShow == 4:
            scoreScreen()    
        elif screenShow == 8:
            gameOptionScreen()                         
 
    #Report 2.1. Show All(Order By Name) 
    elif screenShow >= 13 and screenShow <= 18:                
        background(0)
        
        if screenShow == 13:
            showReportScreen("By Name1")                  
        elif screenShow == 14:
            showReportScreen("By Name2")  
        elif screenShow == 15:
            showReportScreen("By Clay Number")
        elif screenShow == 16:
            showReportScreen("By The Average Shoot Time")  
        elif screenShow == 17:
            showReportScreen("By The Fastest Shoot")  
            
    elif screenShow == 22:
        gameEndScreen()
    
    elif screenShow >= 20:
        gamingScreen()

    textAlign(CENTER)
    
    dropMenu()

# Adjust gun's angle (10 - 80 degree)        
def mouseDragged(): 
    global screenShow, gun1, gun2, playWithComputerOption

    if screenShow >= 20:
        
        if mouseX > gun1.position[0] - 20  and mouseX <  gun1.position[0] + 40 and mouseY > gun1.position[1] - 30  and  mouseY < gun1.position[1] + 5:
            if  gun1.Rotate > -80 and gun1.Rotate < -10:
                gun1.Rotate -= pmouseY - mouseY            
            else:
                gun1.Rotate = -45
    
        if playWithComputerOption != 1 and mouseX > gun2.position[0] - 40 and mouseX <  gun2.position[0] + 20 and mouseY > gun2.position[1] - 30  and  mouseY < gun2.position[1] + 5:   
            if  gun2.Rotate < 80 and gun2.Rotate > 10:
                gun2.Rotate += pmouseY - mouseY
            else:
                gun2.Rotate = 45


def mouseClicked():
    global screenW, screenH, boothWidth, flyingAreaBottomH, flyingAreaTopH, screenShow, gun1, gun2, playerHeight, bullets, flyingBullets, playerAName, playerBName, gameStart, shootdownClays,drop, playWithComputerOption
    global gameHistoryData, gameReportData, resultFilePath, FileNotFoundMessage
    global rowsPerReport, curReportPageIndex, nTotalReportPages
    print("mousePressed mouseX=" + str(mouseX) + "; mouseY=" + str(mouseY) + ";screenShow=" + str(screenShow) + ";drop=" + str(drop) + ";playWithComputerOption=" + str(playWithComputerOption) )
        
    if screenShow == 1:
        if mouseX >= 350 and mouseX <= 650 and mouseY >= 550 and mouseY <= 610:
            helpScreen()
            
        elif mouseX >= 410 and mouseX <= 580 and mouseY >=650 and mouseY <= 710:
            screenShow = 4
            data = report.loadGameHistry(resultFilePath)
            FileNotFoundMessage = data[0]
            gameHistoryData = data[1]
            #for data in gameHistoryData:
            #    print("data=" + str(data))
            curReportPageIndex = 1    
            gameReportData = report.createReportData(gameHistoryData)
        
        elif mouseX > 450 and mouseX < 550 and mouseY >= 765 and mouseY <= 825:
            playerAName=""
            playerBName=""
            playWithComputerOption = 2
            screenShow = 8
        
    elif screenShow == 3:# Name window
        if mouseX >= 456 and mouseX <= 547 and mouseY >= 770 and mouseY <= 820: # Clicked PLAY
            print("playerAName="  + playerAName + ";playerAName=" + playerBName)
            if len(playerAName) > 1 and len( playerBName) > 1:
                initGame()  
                screenShow = 20
            
    elif screenShow == 8:# Game type option window
        if mouseX >= 270 and mouseX <= 730 and mouseY >= 300 and mouseY <= 340: # Clicked Play With Computer
            print("Selected PLAY WITH COMPUTER")
            playerBName = "Computer"
            playWithComputerOption = 1
            screenShow = 3
        elif mouseX >= 270 and mouseX <= 730 and mouseY >= 400 and mouseY <= 440: # Clicked Play With Another Player
            print("Clicked Play With Another Player")
            playerBName = ""
            playWithComputerOption = 2
            screenShow = 3
                            
    if drop:
        if mouseX >= 825 and mouseX <= 945 and mouseY >= 150 and mouseY <= 200:
            helpScreen()
        if mouseX >= 825 and mouseX <= 945 and mouseY >= 210 and mouseY <= 260:
            screenShow = 4
            data = report.loadGameHistry(resultFilePath)
            FileNotFoundMessage = data[0]
            gameHistoryData = data[1]
            
        if mouseX >= 825 and mouseX <= 945 and mouseY >= 270 and mouseY <= 320:
            screenShow = 1
        if mouseX >= 825 and mouseX <= 945 and mouseY >= 330 and mouseY <= 380:
            if screenShow == 22 :
                report.saveGameHistry(resultFilePath, playerAName, playerBName, shootdownClays)
            exit()    
        drop = False      

    if screenShow == 4: #Score Screen
        yAdj=100
        menuSpace = 80
        menuLeft1 = 100
        menuLeft2 = 120
        barWidth = 20
    
        if mouseX >= menuLeft2 and mouseY >=  menuSpace * 3 - 20 - yAdj and mouseX <= menuLeft2 + 280 and mouseY <= menuSpace * 3 - yAdj: #Show All (Order by Name)
           print("Order By Player1 Name")
           screenShow = 13
           curReportPageIndex = 1
           
        elif mouseX >= menuLeft2 and mouseY >=  menuSpace * 4 - 20-yAdj and mouseX <= menuLeft2 + 280 and mouseY <= menuSpace * 4-yAdj: #Show All (Order by Date)
           print("Order By Player2 Name")
           screenShow = 14
           curReportPageIndex = 1
           
        elif mouseX >= menuLeft2 and mouseY >= menuSpace * 5 - 20-yAdj and mouseX <= menuLeft2 + 640 and mouseY <= menuSpace * 5-yAdj: #Show All (Order by The Smartest Round)
           print("Order By Clay Number")
           screenShow = 15
           curReportPageIndex = 1
           
        elif mouseX >= menuLeft2 and mouseY >= menuSpace * 6 - 20-yAdj and mouseX <= menuLeft2 + 640 and mouseY <= menuSpace * 6-yAdj: #Show All (Order by The Smartest Player)
           print("By The Average Shoot Time")
           screenShow = 16
           curReportPageIndex = 1
           
        elif mouseX >= menuLeft2 and mouseY >= menuSpace * 7 - 20-yAdj and mouseX <= menuLeft2 + 640 and mouseY <= menuSpace * 7-yAdj: #Show All (Order by The fastest Round)
           print("Report- Order By The Fastest Shoot")
           screenShow = 17
           curReportPageIndex = 1
           
    elif screenShow == 12: #Initialize a game
       
       if len(playerAName) < 1 or len(playerBName) < 1:
           for i in range(len(players)):
               if mouseX >= menuLeft1 and mouseY >= menuSpace * 3 + i * 30 - 20 and mouseX <= menuLeft1 + len(players[i]) * 20 and mouseY <= menuSpace * 3 + i * 30 and players[i] !=playerAName and players[i] !=playerBName: #Selected an player
                   playerName=players[i]                   
                   
                   if len(playerAName)<1:
                       playerAName=playerName
                   elif len(playerBName)<1:
                       playerBName=playerName
                       
    elif screenShow >= 13 and screenShow <=17: #Click report paging button
        if mouseX >= screenW/2 - 200 and mouseX < screenW/2 - 160 and mouseY> 55 and mouseY < 85 :
            if curReportPageIndex > 1:
                curReportPageIndex -= 1
                print("< curReportPageIndex=" + str(curReportPageIndex) + ";nTotalReportPages=" + str(nTotalReportPages))

        elif mouseX >= screenW/2 - 100 and mouseX < screenW/2 - 60 and mouseY> 55 and mouseY < 85 :
            if curReportPageIndex < nTotalReportPages:
                curReportPageIndex += 1
                print("> curReportPageIndex=" + str(curReportPageIndex) + ";nTotalReportPages=" + str(nTotalReportPages))
                  
    elif screenShow == 20:
        #Start game -> Begin to throw clay        
        if mouseX >= screenW/2 - 50 and mouseX <= screenW/2 + 50 and mouseY >= 20 and  mouseY <= 40 :
            if gameStart == False:
                screenShow = 21
                gameStart = True
                                                                    
    elif screenShow == 21:
        #Gun1 triggered
        if gameStart == True and mouseX > gun1.position[0] - 10 and mouseX < gun1.position[0] + 5 and mouseY > gun1.position[1] + 5  and  mouseY < gun1.position[1] + 20  :
            fire(1)
            
        #Gun2 triggered    
        if gameStart == True and mouseX > gun2.position[0] - 5 and mouseX < gun2.position[0] + 10 and mouseY > gun2.position[1] + 5  and  mouseY < gun2.position[1] + 20  :
            fire(2)

    elif screenShow == 22:
        #ReStart game
        if mouseX > 430 and mouseX < 570 and mouseY >= 765 and  mouseY <= 820 :
            initGame() 
            #if gameStart == False:
            screenShow = 20
            #gameStart = True
                            
def keyPressed():
    global screenShow, playerAName, playerBName, gameStart, p1Turn, playWithComputerOption

    #Name input screen
    if screenShow == 3:
        if p1Turn:
            if keyCode == 10:
                p1Turn = False
            elif keyCode == 8:
                if len(playerAName) > 0:
                    playerAName = playerAName[:-1]
            elif (keyCode >= 65 and keyCode <= 90) or (keyCode >= 97 and keyCode <= 122):
                playerAName += key

        elif playWithComputerOption == 2:
            if keyCode == 10:
                p1Turn = True
            elif keyCode == 8:
                if len(playerBName) > 0:
                    playerBName = playerBName[:-1]
            elif (keyCode >= 65 and keyCode <= 90) or (keyCode >= 97 and keyCode <= 122):
                playerBName += key
    
    #Clay shooting screen                        
    elif screenShow == 21:                
        if gameStart == True and ( keyCode == 37 or keyCode == 68 ):
            fire(1)
        elif playWithComputerOption !=1 and gameStart == True and keyCode == 39:
            fire(2)


          
