from Tkinter import *
import os
import urllib
import random

#Images of Game of Life owned by Hasbro
#Images retrieved from http://blog.nicoledelsenno.com/?p=212
#http://recruiterpoet.files.wordpress.com/2011/07/life2.gif
#Images of Mario and Koopa ownership of Nintendo
#Images retrieved from http://www.spriters-resource.com

##From 15-112
#We use both to store the points created in GameOfLifePoints in the function
#points.txt
def readFile(filename, mode="rt"):
    # rt stands for "read text"
    fin = contents = None
    try:
        fin = open(filename, mode)
        contents = fin.read()
    finally:
        if (fin != None): fin.close()
    return contents

def writeFile(filename, contents, mode="wt"):
    # wt stands for "write text"
    fout = None
    try:
        fout = open(filename, mode)
        fout.write(contents)
    finally:
        if (fout != None): fout.close()
    return True

def sizeChanged(event):
    canvas = event.widget.canvas
    canvas.width = event.width - 4
    canvas.height = event.height - 4
    redrawAll(canvas)
#From 15 112 ^
    
class GameOfLifePoints(object): #purpose is to refer to every space on the
    #game of life board to be represented by a point

    def mousePressed(self, event): 
        canvas = self.canvas
        canvas.pressedAt.append((event.x, event.y)) # append the (x,y) tuple
        print "Our locations:", canvas.pressedAt
        canvas.storedPoints = writeFile( "\\GameOfLife\\points.txt", repr(
            canvas.pressedAt)) #every space on the board is from the coordinates
        #represented in canvas.PressedAt
        canvas.newLocations = eval(readFile( "\\GameOfLife\\points.txt"))
        print canvas.newLocations

    def keyPressed(self, event):
        canvas = self.canvas
        if (event.char == "d"): #deleting the last point in the board(undo)
            if len(canvas.pressedAt) > 0:
                canvas.pressedAt = canvas.pressedAt[0:-1]
##    class Cells:
##        def init(self):
##            for i in canvas.data.newLocations:
##                print "this location", i 
        
    def timerFired(self):
        canvas = self.canvas
        delay = 250 # milliseconds

    def redrawAll(self):
        canvas = self.canvas
        thirdImage = canvas.thirdImage
        canvas.delete(ALL)
        r = canvas.r
        canvas.create_image(canvas.width/2, canvas.height/2,
                            image = thirdImage) #displays the board
        for (x,y) in canvas.pressedAt: #each point represented by a black point
            canvas.create_oval(x-r, y-r, x+r, y+r, fill="black")

    def init(self):
        canvas = self.canvas
        canvas.pressedAt = []
        canvas.index = 0
        # from 112 notes
        image = PhotoImage(file="GameOfLifeBoardFinal.gif")
        canvas.image = image #printing the board out to play
        canvas.width = canvas.winfo_reqwidth()-4
        canvas.height = canvas.winfo_reqheight()-4
        thirdImage = image.subsample(3,3) #resizing image to fit screen
        canvas.thirdImage = thirdImage
        # from 112 notes ^
        canvas.r = 3 # 3 pixel radius

     # Call app.run(width,height) to get your app started
    def run(self, width=1200, height=850):
        # create the root and the canvas
        root = Tk()
        self.width = width
        self.height = height
        self.canvas = Canvas(root, width=width, height=height)
        self.canvas.pack(fill=BOTH, expand=YES)#from 112 
        # set up events
        def redrawAllWrapper():
            self.canvas.delete(ALL)
            self.redrawAll()
        def mousePressedWrapper(event):
            self.mousePressed(event)
            redrawAllWrapper()
        def keyPressedWrapper(event):
            self.keyPressed(event)
            redrawAllWrapper()
        root.bind("<Button-1>", mousePressedWrapper)
        root.bind("<Key>", keyPressedWrapper)
        # set up timerFired events
        self.timerFiredDelay = 250 # milliseconds
        def timerFiredWrapper():
            self.timerFired()
            redrawAllWrapper()
            # pause, then call timerFired again
            self.canvas.after(self.timerFiredDelay, timerFiredWrapper)
        # init and get timerFired running
        self.init()
        timerFiredWrapper()
        # and launch the app
        root.mainloop()  # This call BLOCKS (so your program waits until
        #you close the window!)

class Player(object): #all the info needed for the players
    def __init__(self):
        self.font = ("Helvetica", 24, "bold")
        (self.positionX,self.positionY) = (200,200) #for stats
        self.lifeMsg = "Hi! Welcome to the Game of Life!"
        self.displayStatus = False #you can control if or not to display status
        self.indexStatus = False #of player
        self.newLocations = eval(readFile( "\\GameOfLife\\points.txt"))
        self.cells = Cell() #everything that happens when you pass/land on a
        #point on the board is caused by the list caused in the cells (sub)class
        (self.Money, self.Babies, self.LifeCard, self.LifeEvent) = (Money(),
         Babies(),LifeCard(),LifeEvent()) #specific cells have their own class
        (self.DoSomething, self.OtherPoint) = (DoSomething(), OtherPoint())
        self.otherPos = self.cells.otherPos
        self.playerMoney = self.cells.playerMoney #money
        self.marriedStatus = self.LifeEvent.marriedStatus
        self.homeStatus = self.LifeEvent.homeStatus
        self.salary = self.Money.salary #salary
        self.playerBabyCount = self.Babies.playerBabyCount #children
        self.occupation = self.LifeEvent.occupation
        self.occupations = self.LifeEvent.occupations
        self.degreeStatus = self.LifeEvent.degreeStatus
        self.message = "Moving 0 Places"

class GameOfLifeData(GameOfLifePoints):
    #What creates the players on the board and allows you to move around
    def init(self): #holds all the stats of the player, the marriageStatus,
        #whether the player has a home, how many babies does the player have
        #the amount money the player has
        super(GameOfLifeData, self).init()
        canvas = self.canvas
        self.font = ("Helvetica", 24, "bold")
        (self.positionX,self.positionY) = (200,200)
        self.lifeMsg = "Welcome to the Game of Life!"
        self.displayStatus = False
        self.indexStatus = False
        self.cells = Cell() #everything that happens when you pass/land on a
        #point on the board is caused by the list caused in the cells class
        #and it's subclasses
        (self.Money, self.Babies, self.LifeCard, self.LifeEvent) = (Money(),
         Babies(),LifeCard(),LifeEvent())
        (self.DoSomething, self.OtherPoint) = (DoSomething(), OtherPoint())
        self.players()

    def players(self):#deals with how many players in the game
        self.playerOne = Player() #we have two players right now
        self.playerTwo = Player()
        self.players = [self.playerOne, self.playerTwo] # a list of players
        self.currentPlayer = 0 #and the index for whose turn and the other...
        self.otherPlayer = 1 #player
        self.playerTwo.positionX = self.width - self.playerOne.positionX
        self.player = self.players[self.currentPlayer]
        self.isGameOver = False
        self.startScreen = True
        self.instruction = False
        
    def keyPressed(self, event):
        if event.char == "h": self.instruction = True
        if event.char == "j": self.instruction = False
        if self.startScreen == False:
            if event.char == "d":#press d to make your move!
                self.makeMove()#make Move evaluates the functions stored in the
                #list made by cells for when you land/pass a space
            if event.char == "a": #show status of player
                self.displayStatus = True
            if event.char == "s": #turn ofus stat
                self.displayStatus = False
            if event.char == "i": #show index of player
                self.indexStatus = True
            if event.char == "o": #turn of index
                self.indexStatus = False
            if event.char == "x": #call automatic game over
                self.gameOver(self.players[self.currentPlayer],
                              self.players[self.otherPlayer])
        else:
            if event.char == "s":
                self.startScreen = False
            
    def redrawAll(self):
        (canvas,cells) = (self.canvas,self.cells)
        if self.startScreen == True:self.startPage()
        elif self.instruction == True: self.instructions()
        else:
            super(GameOfLifeData, self).redrawAll()
            self.viewPlayer(self.playerOne,imagePlayer = PhotoImage(
                file = "MarioStill.gif")) #player one's avatar
            self.viewPlayer(self.playerTwo,imagePlayer = PhotoImage(
                file = "koopaTest.gif")) #player two's avatar
            if self.displayStatus == True: #displays status of player
                self.status(self.playerOne)
                self.status(self.playerTwo)
            if self.indexStatus == True: #displays index of player
                self.index(self.playerOne)
                self.index(self.playerTwo)
            self.displayLifeStatus(self.lifeMsg) #for misc. spots, this is what
            #the text on that cell says
            self.playerTurn() #display who's turn it is
            if self.isGameOver == True:
                self.winner() #displays who won

    def startPage(self):
        self.startImage()
        self.canvas.create_text(self.width/2, self.height/2,
            text = "Welcome to the Game of Life! Press s to start!", font =
            self.font, fill = "black")
        self.canvas.create_text(self.width/2, self.height/2 + 50,
            text = "Press h during game to see instructions", font =
            self.font, fill = "black")

    def startImage(self):
        canvas = self.canvas
        image = canvas.image
        canvas.gameOfLifeImage = PhotoImage(file = "GameOflife2.gif")
        self.canvas.create_image(self.width/2,self.height/2, image =
                                 canvas.gameOfLifeImage)
        
        
    def instructions(self): #how to play!
        self.instructionImage() #image for instructions
        self.instructionSet() #text for instructions
        

    def instructionSet(self):
        self.canvas.create_text(self.width/2, self.height/2 - 150,
            text = "Hello!" , font = self.font, fill = "black")
        self.canvas.create_text(self.width/2, self.height/2 - 100,
            text = "press d to make your move!",
                    font = self.font, fill = "black") 
        self.canvas.create_text(self.width/2, self.height/2 - 50,
            text = "Press i to show index, o to turn off!",
                                font = self.font, fill = "black")
        self.canvas.create_text(self.width/2, self.height/2,
            text = "Press a to show status of player, s to turn off!" ,
                                font = self.font, fill = "black")
        self.canvas.create_text(self.width/2, self.height/2 + 50,
            text = "Get to the end of board with the most money!",
                                font = self.font, fill = "black")
        self.canvas.create_text(self.width/2, self.height/2 + 100,
            text = "Check shell to see when you need to make a decision!",
                                font = self.font, fill = "black")
        self.canvas.create_text(self.width/2, self.height/2 + 150,
            text = "Good Luck! press j to resume",
            font = self.font, fill = "black")

    def instructionImage(self):
        self.startImage()
        
    def viewPlayer(self,currentPlayer, imagePlayer): #display player X avatar
        #at their index
        canvas = self.canvas
        image = canvas.image
        cells = currentPlayer.cells
        currentPlayer.imagePlayer = imagePlayer
        #takes the initial position from points.txt to print out player's piece
        (currentPlayer.playerPositionX, currentPlayer.playerPositionY
         )  = currentPlayer.newLocations[cells.index]
        self.canvas.create_image(currentPlayer.playerPositionX,
            currentPlayer.playerPositionY, image = currentPlayer.imagePlayer)

    def status(self, player): #displaying status of the player(s)
        self.canvas.create_text(player.positionX, player.positionY,
            text = player.message , font = self.font, fill = "white")
        self.canvas.create_text(player.positionX, player.positionY + 50,
            text = "Player Money = %s" %(str(player.Money.playerMoney)) ,
                    font = self.font, fill = "white") 
        self.canvas.create_text(player.positionX, player.positionY + 100,
            text = "Marriage Status = %s" %(str(player.LifeEvent.marriedStatus)),
                                font = self.font, fill = "white")
        self.canvas.create_text(player.positionX, player.positionY + 150,
            text = "Home = %s" %(str(player.LifeEvent.houseChoice)) ,
                                font = self.font, fill = "white")
        self.canvas.create_text(player.positionX, player.positionY + 200,
            text = "Career = %s" %(str(player.LifeEvent.occupation)),
                                font = self.font, fill = "white")
        self.canvas.create_text(player.positionX, player.positionY + 250,
            text = "Children = %s" %(str(player.Babies.playerBabyCount)),
                                font = self.font, fill = "white")
        self.canvas.create_text(player.positionX, player.positionY + 300,
            text = "Salary = %s" %(str(player.LifeEvent.salary)),
                                font = self.font, fill = "white")
        
    #rework of 112 boardGame
    def switchCurrentPlayer(self): #switches whose turn it is
        if self.currentPlayer < (len(self.players) - 1):
            self.currentPlayer += 1
            self.otherPlayer -= 1
        else: (self.currentPlayer,self.otherPlayer) = (0,1)
    #rework of 112 boardGame ^

    def playerTurn(self):
        self.canvas.create_text(self.width/2, self.positionY,
            text = "Player %s turn" %(str(self.currentPlayer + 1)),
                                font = self.font, fill = "white")

    def index(self, player):
        self.canvas.create_text(player.positionX, player.positionY - 50,
            text = "player position = %s" %(str(player.cells.index)),
            font = self.font, fill = "white")
        
    def mousePressed(self, event):
        pass

    def makeMove(self): #function that deals what happens when it's your turn
        currentPlayer = self.players[self.currentPlayer]
        otherPlayer = self.players[self.otherPlayer]
        currentPlayer.cells.makeList() #makes the list that holds the data
        #of what happens at each point in a string (which is why we eval)
        (cells,othercells) = (currentPlayer.cells,otherPlayer.cells)
        # ^ index of the currentPlayer and other player
        self.randomCounter = random.randint(1, 10) #spin to see how far you
        #move!
        #cells.index += self.randomCounter
        #print currentPlayer.cells.Spaces
        print "player one money", self.playerOne.Money.playerMoney
        print "player two money", self.playerTwo.Money.playerMoney
        currentPlayer.counter = self.randomCounter
        #randomCounter determines how far player moves
        currentPlayer.message = "Moving %s Places" % str(self.randomCounter)
        if self.isGameOver == False:
            self.makeMoveGame(currentPlayer,otherPlayer)
        self.switchCurrentPlayer()
        
    def makeMoveGame(self, currentPlayer,otherPlayer):#while the game isn't over
        (cells,othercells) = (currentPlayer.cells,otherPlayer.cells)
        if currentPlayer.cells.index + self.randomCounter <= (len(
            cells.newLocations) - 1): #no one has hit end of board
            while (currentPlayer.counter > 0):
                self.makeMoveTurn(currentPlayer,otherPlayer)
                #what happens while it's player x's turn
            self.landPoint(currentPlayer) #eval what happens at point you
            #land at
            currentPlayer.Money.playerMoney -= (
                currentPlayer.Babies.playerBabyCount * 5000) #cost for
            #children...
        elif currentPlayer.cells.index + self.randomCounter > (len(
            cells.newLocations) - 1): #one player hit end of board but game
            #goes on
            (cells.index,currentPlayer.counter) = ((len(cells.newLocations)
                                                    - 1),0)
            if otherPlayer.cells.index == (len(cells.newLocations) - 1):
                self.gameOver(currentPlayer,otherPlayer) # both
                    #hit end of board so game over
                
    def makeMoveTurn(self, currentPlayer,otherPlayer): #what happens
        #at player x's turn
        (cells,othercells) = (currentPlayer.cells,otherPlayer.cells)
        if len(cells.Spaces[currentPlayer.cells.index][3]) < 2: 
            cells.index = cells.Spaces[currentPlayer.cells.index][3][0]
            currentPlayer.counter -= 1 #evaluate at each point
        else: #you've hit a fork in the road! choose your direction!
            self.Options(currentPlayer)
            if currentPlayer.cells.index == 1:
                currentPlayer.LifeEvent.career()
        self.passedPoint(currentPlayer)
        #what happens when you pass a point 
        
    def passedPoint(self,currentPlayer):#3 points, when married,job,get a house
        cells = currentPlayer.cells 
        #some things happen when you pass a point! Not just
        #when you land ((ex, paydays and stopping points)
        # they either call fn for new home, job, or marriage
        #or function for payday (green spots)
        if cells.index == currentPlayer.LifeEvent.marriedPos: #stop!Married!
            eval(self.LifeEvent.Spaces[currentPlayer.LifeEvent.marriedPos][2])
            cells.index = currentPlayer.LifeEvent.index
            currentPlayer.counter = 0 #you stop at this point
        elif cells.index == currentPlayer.LifeEvent.homePos:#stop!new house!
            self.passedPointHome(currentPlayer)
        elif cells.index == self.LifeEvent.jobPos:
            self.passedPointJob(currentPlayer) #you get a job!
        self.payDay(currentPlayer)

    def passedPointHome(self,currentPlayer): #you buy a home!
        cells = currentPlayer.cells 
        currentPlayer.LifeEvent.playerMoney = (
                currentPlayer.Money.playerMoney) #set money in lifeEvent
        #where home function is to your money, and then back when evaluating
        #ie calling the function
        eval(self.LifeEvent.Spaces[currentPlayer.LifeEvent.homePos][2])
        currentPlayer.Money.playerMoney = (
            currentPlayer.LifeEvent.playerMoney)
        cells.index = currentPlayer.LifeEvent.index
        currentPlayer.counter = 0 #the player must stop at this spot
            
    def passedPointJob(self, currentPlayer): #new job!
        cells = currentPlayer.cells 
        currentPlayer.LifeEvent.playerMoney = currentPlayer.Money.playerMoney
        eval(self.LifeEvent.Spaces[self.LifeEvent.jobPos][2])
        currentPlayer.Money.playerMoney = (
            currentPlayer.LifeEvent.playerMoney)
        cells.index = currentPlayer.LifeEvent.index 
        currentPlayer.counter = 0 #the player must stop at this spot

    def payDay(self,currentPlayer): #payday spots are in a list for each player
        #so when you land at that point, add to your money your salary (the fn
        #that's being eval, and take that index out of th list 
        cells = currentPlayer.cells
        #print currentPlayer.Money.payDaySpots
        if len(currentPlayer.Money.payDaySpots) >= 1:
            if cells.index == min(currentPlayer.Money.payDaySpots):
                eval(cells.Spaces[min(currentPlayer.Money.payDaySpots)][2])
                currentPlayer.Money.payDaySpots = (
                    currentPlayer.Money.payDaySpots[1:len(cells.payDaySpots)])
            if (cells.index in [55,88]):
                currentPlayer.Money.payDaySpots = (
                    currentPlayer.Money.payDaySpots[1:len(cells.payDaySpots)])
                
    def landPoint(self,currentPlayer): #only happens when you land on this space
        cells = currentPlayer.cells
        #newBaby, lifeCard, taxes, or miscellaneous (otherPos)
        if cells.index in cells.babyPos: eval(cells.Spaces[cells.index][2])
        elif cells.index in cells.lifePos: eval(cells.Spaces[cells.index][2])
        elif cells.index in cells.salTradePos:
            eval(cells.Spaces[cells.index][2])
        elif cells.index in cells.taxPos: eval(cells.Spaces[cells.index][2])
        elif cells.index in cells.newCareerPos:
            eval(cells.Spaces[cells.index][2])
        elif cells.index in cells.otherPos:
            currentPlayer.OtherPoint.index = cells.index
            currentPlayer.OtherPoint.playerMoney = (
                currentPlayer.Money.playerMoney)
            #keeping playerMoney all the same ^
            eval(cells.Spaces[cells.index][2])
            currentPlayer.Money.playerMoney = (
                currentPlayer.OtherPoint.playerMoney)
        if cells.index in cells.gameOfLifeSpaces:
            self.lifeEventStatuses(currentPlayer)
        else: self.lifeMsg = "Game of Life!" #default message

    def lifeEventStatuses(self,currentPlayer):
        self.lifeEventStatus(currentPlayer) #the text at spot player lands at
        self.moreEventStatus(currentPlayer) #at the said index player lands on
        self.evenMoreEventStatus(currentPlayer)
        self.lastEventStatus(currentPlayer)
        #else: eval(cells.Spaces[cells.index][2])

    def lifeEventStatus(self,currentPlayer): #text at space x
        cells = currentPlayer.cells
        if (cells.index == 2): self.lifeMsg = "Rent, Pay $5k"
        elif (cells.index == 3): self.lifeMsg = "Raffle prize! Collect $10k!"
        elif (cells.index == 4): self.lifeMsg = "Scholarship, collect $20k!"
        elif (cells.index == 5): self.lifeMsg = "Buy books, pay $5k"
        elif (cells.index == 7): self.lifeMsg = "Part-time Job, collect $5k"
        elif (cells.index == 10): self.lifeMsg = "Spring break!, pay $5k"
        elif (cells.index == 20): self.lifeMsg = "Marathon! collect $20k"
        elif (cells.index == 26): self.lifeMsg = "Honeymoon! pay $10k"
        elif (cells.index == 28): self.lifeMsg = "Buy furniture! pay $10k"
        elif (cells.index == 29): self.lifeMsg = "Car insurance, pay $10k"
        elif (cells.index == 30): self.lifeMsg = "Moving! pay $10k"
        elif (cells.index == 31): self.lifeMsg = "Night School, pay $20k"
        elif (cells.index in cells.taxPos): self.lifeMsg = "Taxes!"
        elif (cells.index == 38): self.lifeMsg = "Fired! New Career"
        elif (cells.index == 40): self.lifeMsg = "Buy baby crib! pay $5k"
        elif (cells.index == 42): self.lifeMsg = "Win talent show collect $20k"
        elif (cells.index == 45): self.lifeMsg = "At World Series! pay $20k"
        elif (cells.index == 47): self.lifeMsg = "Hollywood premeir! pay $5k"
        elif (cells.index == 48): self.lifeMsg = "House flood! pay $40k"
        
    def moreEventStatus(self,currentPlayer): #text at space x
        cells = currentPlayer.cells
        if (cells.index in cells.salTradePos): self.lifeMsg = "Trade Salaries!"
        elif (cells.index == 49): self.lifeMsg = "Family checkup! pay $5k"
        elif (cells.index == 54): self.lifeMsg = "Tree falls on house, pay $15k"
        elif (cells.index == 56): self.lifeMsg = "Buy big screen TV, pay $5k"
        elif (cells.index == 61): self.lifeMsg = "Car stolen!!! pay $15k"
        elif (cells.index == 67): self.lifeMsg = "Vacation!, pay $25k"
        elif (cells.index == 68): self.lifeMsg = "Night School, pay $20k"
        elif (cells.index == 68): self.lifeMsg = "Night School, pay $20k"
        elif (cells.index == 70): self.lifeMsg = "Art auction, pay $20k"
        elif (cells.index == 73): self.lifeMsg = "Beauty Pageant! collect $20k"
        elif (cells.index == 77): self.lifeMsg = "Tennis camp! Pay $25k"
        elif (cells.index == 78): self.lifeMsg = "African Safari! Pay $25k"
        elif (cells.index == 82): self.lifeMsg = "Day Care! Pay $5k"
        elif (cells.index == 83): self.lifeMsg = "Write bestseller! Collect 80k"
        elif (cells.index == 85): self.lifeMsg = "Fund Police Ball! Pay $15k"
        elif (cells.index == 87): self.lifeMsg = "Find treasure! Collect $80k"
        elif (cells.index == 89): self.lifeMsg = "Invest in Broadway! Pay $15k"
        elif (cells.index == 92): self.lifeMsg = "Build a barn! Pay $70k"
        elif (cells.index == 94): self.lifeMsg = "Buy a sports car! Pay $25k"

    def evenMoreEventStatus(self,currentPlayer): #text at space x
        cells = currentPlayer.cells
        if (cells.index == 95): self.lifeMsg = "Tax Break! Collect $75k"
        elif (cells.index == 97): self.lifeMsg = "Give to art inst.! Pay $25k!"
        elif (cells.index == 99): self.lifeMsg = "Game Show! Collect $95k"
        elif (cells.index == 100): self.lifeMsg = "Summer School. Pay $5k!"
        elif (cells.index == 103): self.lifeMsg = "Buy cabin on lake! Pay $90k"
        elif (cells.index == 105): self.lifeMsg = "Burglary! Pay $50k"
        elif (cells.index == 106): self.lifeMsg = "Nobel Prize! Win $100k!!!"
        elif (cells.index == 108): self.lifeMsg = "Buy gym equipment! Pay $30k!"
        elif (cells.index == 110): self.lifeMsg = "Tornado! Pay $125k!"
        elif (cells.index == 112): self.lifeMsg = "Mooshoo flu attk! Pay $25k!"
        elif (cells.index == 114): self.lifeMsg = "Buy sailboat! Pay $30k"
        elif (cells.index == 115): self.lifeMsg = "Golf Tourney! Pay $35k"
        elif (cells.index == 119): self.lifeMsg = "Produce rock vid! Pay $100k"
        elif (cells.index == 123): self.lifeMsg = "Remove tattoes! Pay $100k"
        elif (cells.index == 124): self.lifeMsg = "Kids to college! Pay $50k"
        elif (cells.index == 129): self.lifeMsg = "Sponsor an exhibit.Pay $125k"
        elif (cells.index == 135): self.lifeMsg = "Race horse! Pay $65k"
        elif (cells.index == 141): self.lifeMsg = "Tour Europe! Pay $45k"
        
    def lastEventStatus(self,currentPlayer): #text at space x
        cells = currentPlayer.cells
        if (cells.index == 144): self.lifeMsg = "Party for grammy winners!-$35k"
        elif (cells.index == 145): self.lifeMsg = "Luxury Cruise! Pay $5k"
        elif (cells.index == 146): self.lifeMsg = "Pension, Collect $100k"

    def displayLifeStatus(self,lifeMsg): #displays message at point x
        self.canvas.create_text(self.width/2, self.positionY + 350,
            text = lifeMsg, font = self.font, fill = "white")
        
#(19,-5000) doctor, (28,-10000)salesman, (31, -20000) teacher, (45, -20000)
#Athlete (49, -5000) doctor (56, 5000) salesman (68, -20000) teacher 
#(77, -25000) Athlete Teacher (82, -5000) Police (85,-15000)
#is insured (optional)
# 38 newCareer 116

    def Options(self,currentPlayer): #choose which direction you're going!
        cells = currentPlayer.cells
        self.value = int(raw_input("Choose next spot %d or %d" % (1,2)))
        if self.value not in [1,2] : print "Try again! Must be one or two!"
        #elif type(self.value) != int: print "Needs to be an integer!"
        else:
            if self.value == 1:
                cells.index = cells.Spaces[cells.index][3][0]
            if self.value == 2:
                cells.index = cells.Spaces[cells.index][3][1]
                currentPlayer.Money.payDaySpots = (
                    currentPlayer.Money.payDaySpots[1:len(cells.payDaySpots)])
                
    def gameOver(self, currentPlayer,otherPlayer): #add to the player's money
        #all their life cards(which is just numbers with money) the one who
        #has the most money at the end wins!
        currentLifeCards = currentPlayer.LifeCard.playerLifeCards
        otherLifeCards = otherPlayer.LifeCard.playerLifeCards
        for i in xrange(len(currentPlayer.LifeCard.playerLifeCards)):
            currentPlayer.Money.playerMoney += currentLifeCards[i]
        for i in xrange(len(otherPlayer.LifeCard.playerLifeCards)):
            otherPlayer.Money.playerMoney += otherLifeCards[i]
        self.playersMoney = [self.playerOne.Money.playerMoney,
                              self.playerTwo.Money.playerMoney]
        self.isGameOver = True

    def winner(self): #who won!
        winningPlayer = self.playersMoney.index(max(self.playersMoney))
        self.canvas.create_text(self.width/2, self.height/2,
            text = "Player %s Wins!!!" %(str(winningPlayer + 1)),
                                font = self.font, fill = "black")
                                   
class Cell(object): #class that determines what happens when you land/pass
    #a position
    def __init__(self): #holds the indexes of the points that either
        #add money, give a life card, add a baby, etc.
        self.Spaces = []
        self.salary = 0 
        self.newLocations = eval(readFile( "\\GameOfLife\\points.txt"))
        #gets all the points from the file we created in gameOfLifePoints
        self.playerLifeCards = []
        self.playerMoney = 0
        self.listPos()
        self.gameOfLifePos()
        self.playerBabyCount = 0
        self.playerLifeCards = []
        self.index = 0 #start at point 0
        self.occupation = "Nothing"
        self.degreeStatus = False
        self.houseChoice = "Nothing"
        #if the player went to college, it subtracts 150k then you have
        #to select jobs but if you hit work, you pick a job

    def listPos(self): #lists positions of payday spots, lifecard positions,
        #places where one would have a baby, and stopping spots (lifePosition)
        self.payDaySpots = [1,15,23,32,37,43,52,60,66,71,79,86,90,96,104,111,
                            118,125,132,137,143] 
        self.lifePos = [6,9,11,13,16,18,21,22,27,35,55,58,59,63,64,69,72,81,
                        91,92,98,101,102,121,128,130,133,136,138,140,142]
        self.babyPos = [39,41,44,46,51,53,65,84]
        self.otherPos = [2,3,4,5,7,10,20,26,28,29,30,31,34,40,47,48,49,
                         54,56,61,67,68,70,73,77,78,82,83,85,87,89,92,94,95,
                         97,99,100,103,105,106,108,110,112,114,115,119,123,
                         124,129,135,141,144,145,146]
        self.salTradePos = [50, 62, 75, 93, 107, 120, 131]
        self.newCareerPos = [38,116]
        self.taxPos = [33,76,88,113,126]
        self.lifePosition = [(14, False), (25, False), (36, False)]
        (self.jobStatus, self.jobPos) = (self.lifePosition[0][1],
                                         self.lifePosition[0][0])
        (self.marriedStatus, self.marriedPos) = (self.lifePosition[1][1],
                                               self.lifePosition[1][0])
        (self.homeStatus, self.homePos) = (self.lifePosition[2][1],
                                           self.lifePosition[2][0])
    def gameOfLifePos(self):
        self.listPos()
        self.gameOfLifeSpaces = []
        for i in (self.payDaySpots): self.gameOfLifeSpaces.append(i)
        for i in (self.lifePos): self.gameOfLifeSpaces.append(i)
        for i in (self.babyPos): self.gameOfLifeSpaces.append(i)
        for i in (self.otherPos): self.gameOfLifeSpaces.append(i)
        for i in (self.salTradePos): self.gameOfLifeSpaces.append(i)
        for i in (self.newCareerPos): self.gameOfLifeSpaces.append(i)
        for i in (self.taxPos): self.gameOfLifeSpaces.append(i)
        for i in ([14,25,36]): self.gameOfLifeSpaces.append(i)
        return self.gameOfLifeSpaces
    
    def makeList(self):
        for self.i in xrange(len(self.newLocations)): #like said in init,
            #this stores in the list indexes, a string that will be
            #evaluated of what happens when you land at/pass a point,
            #and split decisions on the board
            i = self.i #indexes
            self.functions() #the functions
            self.splitDecisions() #which index you go to for split index
            self.Spaces.append([i, self.newLocations[i], self.function,
                                self.nextCell]) #so self.spaces 0 = index
                    #1 = coordinates of index #2 is function of what happens
                    #when you land/pass point #nextcell, where player goes next
        return self.Spaces
        #to add to the tuple of coordinates
        #    do you have two choices?
        #    what happens at that point (a function)
        
    def functions(self): #stores all the functions in a string
        #format based on index to be evaluate in GameOfLifeData
        i = self.i #index (again)
        if (i in (self.payDaySpots) or i in [14,25,36] or i in self.lifePos or
            i in self.taxPos or i in self.babyPos or i in self.salTradePos or
            i in self.otherPos or i in self.newCareerPos):
            #these indexes do something
            self.listOfFunctions() #split for style reasons
            self.moreListOfFunctions()
        else: #indexes do nothing
            self.function = "currentPlayer.DoSomething.doSomething()"
                    
    def listOfFunctions(self):
        i = self.i #index (again)
        if i in self.payDaySpots: #getting paid!
            self.function = (
                "currentPlayer.Money.money(currentPlayer.LifeEvent.salary)")
        elif i in [14,25,36]: #marriage,career,or a new house
            if i == 14: self.function = (
                "currentPlayer.LifeEvent.stoppingPoint('career')" )
            elif i == 25: self.function = (
                "currentPlayer.LifeEvent.stoppingPoint('marriage')")
            else: self.function = (
                "currentPlayer.LifeEvent.stoppingPoint('newHouse')")
        elif i in self.lifePos: #draw lifecard
            self.function = "currentPlayer.LifeCard.lifeCard()"
        elif i in self.newCareerPos:
            self.function = "currentPlayer.LifeEvent.newCareer()"
                    
    def moreListOfFunctions(self):
        i = self.i #index (again)
        if i in self.taxPos: #pay taxes
            self.function = (
                "currentPlayer.Money.taxes(currentPlayer.LifeEvent.salary)")
        elif i in self.babyPos:
            if (i == 44 or i == 84): #points where you get a twin instead of
                    #one baby
                self.function = "currentPlayer.Babies.babyCount(2)"
            else:
                self.function = "currentPlayer.Babies.babyCount(1)"
        elif i in self.salTradePos: #trade salaries
            self.function ="currentPlayer.LifeEvent.salTrade(self.playerOne.LifeEvent, self.playerTwo.LifeEvent)"
        elif i in self.otherPos: #misc
            self.function = "currentPlayer.OtherPoint.otherPoints(cells.index)"
        

    def splitDecisions(self):
        #split decisions in the game, example at point 0, whether to
        #go to college or job
        i = self.i
        if (i == 0 or i == 48 or i== 84): #the three split decisions
                if i == 0 : self.nextCell = [1,4]#where you'll land based off
                    #of choice made in Options()
                elif i == 48: self.nextCell = [49,56]
                elif i == 84: self.nextCell = [85,89]
        elif (i == 3 or i == 55 or i == 88): #go back to regular list if
                    #you chose the alternative route
            if i==3: self.nextCell = [15]
            elif i == 55: self.nextCell = [62]
            elif i == 88: self.nextCell = [96]
        else: self.nextCell = [i+1]

class Money(Cell): #called when you pass a payday spot, you get money!
    #or when land on a tax spot, paying taxes :(
    
    def __init__(self):
        super(Money, self).__init__()
        #self.playerOne = player()
        #self.playerTwo = player()
        
    def money(self, value): #get paid
        self.playerMoney += value

    def taxes(self,salary): #pay taxes
        self.playerMoney -= int(round(salary/4))

    

class LifeCard(Cell): #draw a life card that adds/subtracts money at the end
    #of the game. Life Cards stored in list self.playerLifeCards

    def __init__(self):
        super(LifeCard, self).__init__()
        
    def lifeCardValues(self):
        self.lifeCards = []
        for i in xrange(-50000,51000,1000):
            self.lifeCards += [i]
        return self.lifeCards

    def lifeCard(self):
        self.lifeCardValues()
        self.playerLifeCards += [self.lifeCards[random.randint(
            0,(len(self.lifeCards)-1))]]

class Babies(Cell): #add a newborn! Babies take 5K from player's money per turn
    
    def __init__(self):
        super(Babies, self).__init__()
        
    def babyCount(self, babies):
        self.playerBabyCount += babies

class LifeEvent(Cell): #stopping points in the game, marriage, new home, or
    #when you chose the college route, a new job
    
    def __init__(self):
        super(LifeEvent, self).__init__()
        super(LifeEvent, self).makeList()
        self.occupations = [(0,"Police Officer", 40000),(1,"Firefighter",60000),
                            (2,"Artist", 30000), (3,"Entertainer", 50000),
                            (4,"Teacher", 55000), (5,"Athlete", 100000),
                             (6,"Architect",50000), (7,"Psychologist", 60000),
                            (8,"Doctor", 100000),(9,"Accountant", 40000),
                            (10,"Engineer", 100000),
                            (11,"Computer Scientist",100000)]
        # Above ^ index of occupation, occupation, salary of occupation
        self.houses = [(0, "Victorian", 150000),(1, "Condo", 80000),
                       (2, "Town House", 120000), (3, "Mansion", 400000),
                       (4, "New School Home", 300000)]
        #above ^ choices of homes
                    
    def stoppingPoint(self, lifeEvent):
        if lifeEvent == 'marriage': #married!
            self.marriedStatus = True
            self.index = self.marriedPos
            print "Hi"
        elif lifeEvent =='newHouse': #new house so pick home!
            self.homeStatus = True
            self.newHouse()
            self.index = self.homePos
            print "Hi"
        elif lifeEvent == 'career':
            self.jobStatus = True
            self.degreeStatus = True
            self.playerMoney -= 150000 #only happens when person goes to college
                    #college fees!
            self.career()
            print "Hi"
            print self.playerMoney
            print "Salary", self.salary
            self.index = self.jobPos
                    
    def career(self): #choose a career
        print self.occupations
        while self.occupation == "Nothing":
            self.careerChoice = int(raw_input(
            "Choose your career by #(indexes 6+ for those with degrees!)"))
            if 11 >= self.careerChoice > 5 and self.degreeStatus == False:
                print "Try again! Need a degree for this career!"
            elif self.careerChoice > 11 or self.careerChoice < 0:
                print "Try again! Out of bounds!"
            #elif type(self.careerChoice) != int:
                #print "Not an integer!"
            else:
                self.salary = self.occupations[self.careerChoice][2]
                self.occupation = self.occupations[self.careerChoice][1]
                    
    def newHouse(self):#choose a home!
        print self.houses
        while self.houseChoice == "Nothing":
            self.homeChoice = int(raw_input("Choose your home!"))
            if 4 < self.homeChoice or 0 > self.homeChoice:
                print "Try Again! Out of Bounds!"
            else:
                self.playerMoney -= self.houses[self.homeChoice][2]
                self.houseChoice = self.houses[self.homeChoice][1]

    def salTrade(self,playerOne,playerTwo): #trade salaries
        (playerOne.salary,playerTwo.salary) = (playerTwo.salary,
        playerOne.salary)
        print "hello"
        #51, 62, 75, 93, 107, 120, 131

    def newCareer(self):
        self.occupation = "Nothing"
        self.salary = "Nothing"
        self.career()

class OtherPoint(Cell):
    
    def __init__(self):
        super(OtherPoint, self).__init__()
        self.otherPos = [(2, -5000),(3,10000),(4,20000),(5,-5000),(7,5000),
                        (10,-5000),(20,20000),(26, -10000),(28,-10000),
                        (29, -10000),(30, -10000), (31, -20000),
                        (34,50000), (40, -5000),(42,20000), (45, -20000),
                        (47,-5000), (48,-40000), (49, -5000),(54, -15000),
                        (56, -5000),(61, -15000), (67,-25000), (68, -10000),
                        (70,-20000), (73,20000), (77,-25000), (78,-25000),
                        (82, -5000),(83,80000),(85,-15000),(87,80000),
                        (89,-15000),(92,-70000),(94,-25000),(95,75000),
                        (97,-25000),(99,95000), (100,-5000),(103,-90000),
                        (105,-50000),(106,100000),(108,-30000),(110, -125000),
                        (112,-25000),(114,-30000),(115,-35000),(119,-100000),
                        (123,-100000),(124,-50000),(129,-125000),(135,-60000),
                        (141,-45000),(144,-35000), (145,-5000),(146,100000)]
        (self.cashPos,self.cashValue)  = ([],[])
        for i in xrange(len(self.otherPos)):
            self.cashPos += [self.otherPos[i][0]]
        for i in xrange(len(self.otherPos)):
            self.cashValue += [self.otherPos[i][1]]
           
    def otherPoints(self, index):
        #other points add money to player's money
        #otherPos holds index of point and how much you must pay/get
        #cashPos is just the index
        #cash value is his how much you pay/get
        cells = Cell()
        self.playerMoney += self.cashValue[self.cashPos.index(self.index)]
        print "index", self.index
        #self.cashValue[self.cashPos.index(self.index)]
      
class DoSomething(Cell): #other spots on the board

    def __init__(self):
        super(DoSomething, self).__init__()

    def doSomething(self):
        print "Merry Christmas!"

app = GameOfLifeData()
app.run()
        
##app =  GameOfLifeData()
##app.run()

#check to see if the player has hit the end point,
#switch player until end game

#Thing's to do this week
#RESIZABLE IMAGE
#Ability to deal with split places
#storage of character info
#things that happen at point X

#Make move in Game of Life
#GameOfLifeData = boardGame
#Subclasses of Cell (money, lifeCard) all inherit from cell.

#Have a function that is called passed at that is called every time
#with payday it will have to check if passed at AND 
#Have a function that is called for split decisions

