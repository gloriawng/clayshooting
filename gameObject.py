class GameObject:
    
    def __init__(self, id, position, speed, img):
        self.id = id
        self.position = position
        self.speed = speed #For Bullet
        # Only CLAY uses this 3 variables
        self.frameCount = 0 #Need the frame count to control the top position that a CLAY can reach
        self.speedX = 0 #CLAY's X speed
        self.speedY = 0 #CLAY's Y speed
        self.position0 = [0,0] #The start position when throw this clay
        self.img = img
        self.Rotate = 0  #For Gun/Bullet angle, or for CLAY self rotation
        self.player = 0 #Which player's object
        self.xdir = 1 #Move RIGHT/LEFT
        self.ydir = 1 #Move UP/DOWN
        #for report purpose
        self.threwtime = None
        self.shotdownTime = None
        

    def show(self):
        pushMatrix()
        translate(self.position[0], self.position[1])
        rotate(radians(self.Rotate))
        image(self.img, -self.img.width/2, -self.img.height/2)
        popMatrix()
        
        
    def bulletShow(self):
        xpos=self.position[0]
        ypos=self.position[1]
        
        xspeed = self.speed * cos(radians(90 - abs(self.Rotate)))
        yspeed = self.speed * sin(radians(90 - abs(self.Rotate)))
        if self.player == 1:
            xdir = 1
            ydir = -1
        else:
            xdir = -1
            ydir = -1
        
                
        xpos += xspeed * xdir
        ypos += yspeed * ydir
        
        self.position = [xpos, ypos]
        self.show()

    def clayShow(self, screenFrameRate, screenFrameRateclayFlyingSeconds):
        xpos = self.position[0]
        ypos = self.position[1]
        
        if self.speedY != 0.0 :
            self.frameCount += 1
            self.Rotate += 3
            xpos += self.speedX  * self.xdir
            t = (1.0 * self.frameCount ) / ( 1.0 * screenFrameRate )
           
            freeFallDownConstAdj = 7.0 #Standard is 9.8 , but it's meter, so we need an adjustment
            ypos =  self.position0[1] -  int( self.speedY * t -  0.5 * 9.8 * freeFallDownConstAdj * ( pow( t, 2 ) ) )
                
        self.position = [xpos, ypos]
        self.show()
