# ======================================================================
# FILE:        MyAI.py
#
# AUTHOR:      Abdullah Younis
#
# DESCRIPTION: This file contains your agent class, which you will
#              implement. You are responsible for implementing the
#              'getAction' function and any helper methods you feel you
#              need.
#
# NOTES:       - If you are having trouble understanding how the shell
#                works, look at the other parts of the code, as well as
#                the documentation.
#
#              - You are only allowed to make changes to this portion of
#                the code. Any changes to other portions of the code will
#                be lost when the tournament runs your code.
# ======================================================================

from Agent import Agent

class MyAI ( Agent ):

    def __init__ ( self ):
        self.board = [["","","","","","",""],["","","","","","",""],["","","","","","",""],["","","","","","",""],["","","","","","",""],["","","","","","",""],["","","","","","",""]]
        self.x = 6
        self.y = 0
        self.agentDir = 0 #0:right 1:up 2:left 3:down
        self.gold = False #before crab
        self.get = False  #after crab
        self.lastAction = ""
        self.Action   = Agent.Action.FORWARD
        self.path = []
        self.walked = []
        self.avail = []
        self.destination = [6,0]
        self.graph = {}
        self.findW = False
        self.killW = False
        self.count = 0
        self.shot = False
        
    def getAction( self, stench, breeze, glitter, bump, scream ):
        
        self.board[self.x][self.y] = self.board[self.x][self.y].replace('@','')
            
        if self.lastAction == "FORWARD" and self.agentDir == 0 and not bump:
                self.y += 1
        elif self.lastAction == "FORWARD" and self.agentDir == 1 and not bump:
                self.x -= 1
        elif self.lastAction == "FORWARD" and self.agentDir == 2 and not bump:
                self.y -= 1
        elif self.lastAction == "FORWARD" and self.agentDir == 3 and not bump:
                self.x += 1
        elif self.lastAction == "TURN_LEFT" and self.agentDir < 3:
                self.agentDir += 1
        elif self.lastAction == "TURN_LEFT" and self.agentDir == 3:
                self.agentDir = 0
        elif self.lastAction == "TURN_RIGHT" and self.agentDir > 0:
                self.agentDir -= 1
        elif self.lastAction == "TURN_RIGHT" and self.agentDir == 0:
                self.agentDir = 3

        self.board[self.x][self.y] += "@"

        if stench:
            self.__stench()
            
        if breeze:
            self.__breeze()

        if bump:
            self.__bump()
            
        if glitter:
            self.Action = Agent.Action.GRAB
            self.gold = True

        """
        if self.x==6 and self.y==0:
            if scream:
                print("Scream!!!!!!!!!!!!!!!!!!!!!")
                self.killW = True
            else:
                self.board[6][1] = "W"
                self.Shot = True
        """
        if scream:
                print("Scream!!!!!!!!!!!!!!!!!!!!!")
                self.killW = True
        
        


        
        self.__renewBoard()
            # search M and D
            # if there are 2 S near M or 2 B near D, change D to P and M to W
            # if no B or S, mark 4 ways K
            
        self.__destination()
        #print("get out __dest function")
            
        #save action as last action 
        self.__getLast()

        """
        self.__printBoard()        
        print ("x  " + str(self.x) + " " + "y  " + str(self.y))
        print ("info  " + self.board[self.x][self.y] )
        print ("diretion " + str(self.agentDir))
        
        print("graph")
        print(self.graph)
        print("path")
        print(self.path)
        print("avail")
        
        print(self.avail)
        print("walked")
        print(self.walked)
        input(self.Action)
        """
        self.count += 1
        return self.Action


        
    def __printBoard(self):
        for i in range(7):
            for j in range(7):
                print (self.board[i][j] + str(i) +str(j))
            print("")

    def __stench(self):
        if "S" not in self.board[self.x][self.y]:
            self.board[self.x][self.y] += "S"
            if self.x+1 < 7 and "O" not in self.board[self.x+1][self.y] and "M" not in self.board[self.x+1][self.y] and "-" not in self.board[self.x+1][self.y]:
                self.board[self.x+1][self.y] += "M"
            if self.x-1 >= 0 and "O" not in self.board[self.x-1][self.y] and "M" not in self.board[self.x-1][self.y] and "-" not in self.board[self.x-1][self.y]:    
                self.board[self.x-1][self.y] += "M"
            if self.y+1 < 7 and "O" not in self.board[self.x][self.y+1] and "M" not in self.board[self.x][self.y+1] and "-" not in self.board[self.x][self.y+1]:    
                self.board[self.x][self.y+1] += "M"
            if self.y-1 >= 0 and "O" not in self.board[self.x][self.y-1] and "M" not in self.board[self.x][self.y-1] and "-" not in self.board[self.x][self.y-1]:
                self.board[self.x][self.y-1] += "M"

    def __breeze(self):
        if "B" not in self.board[self.x][self.y]:
            self.board[self.x][self.y] += "B"
            if self.x+1 < 7 and "O" not in self.board[self.x+1][self.y] and "D" not in self.board[self.x+1][self.y] and "-" not in self.board[self.x+1][self.y]:
                self.board[self.x+1][self.y] += "D"
            if self.x-1 >= 0 and "O" not in self.board[self.x-1][self.y] and "D" not in self.board[self.x-1][self.y] and "-" not in self.board[self.x-1][self.y]:    
                self.board[self.x-1][self.y] += "D"
            if self.y+1 < 7 and "O" not in self.board[self.x][self.y+1] and "D" not in self.board[self.x][self.y+1] and "-" not in self.board[self.x][self.y+1]:    
                self.board[self.x][self.y+1] += "D"
            if self.y-1 >= 0 and "O" not in self.board[self.x][self.y-1] and "D" not in self.board[self.x][self.y-1] and "-" not in self.board[self.x][self.y-1]:
                self.board[self.x][self.y-1] += "D"
                
    def __bump(self):
        if self.agentDir == 0:   #face right
            if self.y+1 < 7:
            #make x > x to "-"
                j = self.y+1
                for i in range(7):
                    self.board[i][j] = "-"
                    
        if self.agentDir == 1:   #face up
            if self.x-1 >= 0:
                i = self.x-1
                for j in range(7):
                    self.board[i][j] = "-"

    


    # search M and D
    # if there are 2 S near M or 2 B near D, change D to P and M to W
    def __renewBoard(self):
        if [6,0] not in self.walked:
            self.walked.append([6,0])

        
        if self.gold == False:# and self.count < 60:
            for i in range(7):
                for j in range(7):
                    if "O" in self.board[i][j]:
                        self.board[i][j] = self.board[i][j].replace("D","")
                        self.board[i][j] = self.board[i][j].replace("M","")
                        
                        
                    if "D" in self.board[i][j]:
                        if self.__isPit(i,j):
                            self.board[i][j] = "P"

                    if self.findW == False:
                        if "M" in self.board[i][j]:
                            if self.__isWumpus(i,j):
                                """
                                print("find it")
                                self.board[i][j] = "W"
                                print(i,j)
                                self.__printBoard()        
                                print ("x  " + str(self.x) + " " + "y  " + str(self.y))
                                print ("info  " + self.board[self.x][self.y] )
                                print ("diretion " + str(self.agentDir))
                                print (self.killW)
                                input(self.Action)
                                """
                                self.findW = True

                    if self.killW == True:
                        self.board[i][j] = self.board[i][j].replace("S","")
                        self.board[i][j] = self.board[i][j].replace("M","")
                        self.board[i][j] = self.board[i][j].replace("W","")
            
                    if ("B" not in self.board[i][j]) and ("S" not in self.board[i][j]) and ("@" in self.board[i][j]):
                        self.__handleOK(i,j)
        

                        
                        
        else:
            for i in range(7):
                    for j in range(7):
                        if "K" in self.board[i][j]:
                            self.board[i][j] = self.board[i][j].replace("K","")

        
                            
                        
    def __isPit(self,x,y):
        counter = 0
        if (x+1 < 7 and "B" in self.board[x+1][y]) or (x+1 == 7) or (x+1 < 7 and "-" in self.board[x+1][y]):
                counter += 1
        if (x-1 >= 0 and "B" in self.board[x-1][y]) or (x-1 == -1) or (x-1 >= 0 and "-" in self.board[x-1][y]):    
                counter += 1
        if (y+1 < 7 and "B" in self.board[x][y+1]) or (y+1 == 7) or (y+1 < 7 and "-" in self.board[x][y+1]):    
                counter += 1
        if (y-1 >= 0 and "B" in self.board[x][y-1]) or (y-1 == -1) or (y-1 >= 0 and "-" in self.board[x][y-1]):
                counter += 1 


        if counter == 4:
            return True;
        return False;
        
    def __isWumpus(self,x,y):
        counter = 0
        if (x+1 < 7 and "S" in self.board[x+1][y]) or (x+1 == 7) or (x+1 < 7 and "-" in self.board[x+1][y]):
                counter += 1
        if (x-1 >= 0 and "S" in self.board[x-1][y]) or (x-1 == -1) or (x-1 >= 0 and "-" in self.board[x-1][y]):    
                counter += 1
        if (y+1 < 7 and "S" in self.board[x][y+1]) or (y+1 == 7) or (y+1 < 7 and "-" in self.board[x][y+1]):    
                counter += 1
        if (y-1 >= 0 and "S" in self.board[x][y-1]) or (y-1 == -1) or (y-1 >= 0 and "-" in self.board[x][y-1]):
                counter += 1 
        if counter == 4:
            return True;
        elif counter == 3:
            countS = 0
            if (x+1 < 7 and "S" in self.board[x+1][y]):
                countS += 1
            if (x-1 >= 0 and "S" in self.board[x-1][y]):    
                countS += 1
            if (y+1 < 7 and "S" in self.board[x][y+1]):    
                countS += 1
            if (y-1 >= 0 and "S" in self.board[x][y-1]):
                countS += 1
            if countS >= 3:
                return True
            
        
        
            
            
        return False;

    def __handleOK(self,x,y):
        if "S" not in self.board[x][y] and "B" not in self.board[x][y]:
            if (self.x+1 < 7) and ("-" not in self.board[x+1][y]) and ("O" not in self.board[x+1][y]):
                self.board[x+1][y] = "K"
                self.__addEdge(10*x+y,(x+1)*10+y)
                self.__addEdge(10*(x+1)+y,(x*10)+y)
                if [x+1,y] not in self.avail:
                    self.avail.append([x+1,y])
                
            if (self.x-1 >= 0) and ("-" not in self.board[x-1][y]) and ("O" not in self.board[x-1][y]):
                self.board[x-1][y] = "K"
                self.__addEdge(10*x+y,(x-1)*10+y)
                self.__addEdge(10*(x-1)+y,(x*10)+y)
                if [x-1,y] not in self.avail:
                    self.avail.append([x-1,y])
             
            if (self.y+1 < 7) and ("-" not in self.board[x][y+1]) and ("O" not in self.board[x][y+1]):
                self.board[x][y+1] = "K"
                self.__addEdge(10*x+y,(x*10)+y+1)
                self.__addEdge(10*x+y+1,(x*10)+y)
                if [x,y+1] not in self.avail:
                    self.avail.append([x,y+1])
                
            if (self.y-1 >= 0) and ("-" not in self.board[x][y-1]) and ("O" not in self.board[x][y-1]):
                self.board[x][y-1] = "K"
                self.__addEdge(10*x+y,(x*10)+y-1)
                self.__addEdge(10*x+y-1,(x*10)+y)
                if [x,y-1] not in self.avail:
                    self.avail.append([x,y-1])
        
        
        

    def __destination(self):
        # mark shell walked
        if "O" not in self.board[self.x][self.y]:
            self.board[self.x][self.y] += "O"
            if [self.x,self.y] not in self.walked:
                self.walked.append([self.x,self.y])
            

        #remove K if the player is there
        self.board[self.x][self.y]=self.board[self.x][self.y].replace("K","")
        #self.avail.remove([self.x,self.y])
       
        if self.gold == False and self.shot == False:# and self.count < 60:
            #choose action
            if self.findW == False:
                #print("did not find w and move")
                self.__move()
            elif self.findW == True and self.killW == False:
                """
                self.__printBoard()        
                print ("x  " + str(self.x) + " " + "y  " + str(self.y))
                print ("info  " + self.board[self.x][self.y] )
                print ("diretion " + str(self.agentDir))
                print (self.killW)
                input(self.Action)
                """
                self.__killW()
            elif self.findW == True and self.killW == True:
                self.__move()

            
        elif self.gold == False and self.shot == True:
            self.move()

        elif self.gold == True and self.get == False:
            self.get = True
            for d in self.avail:
                self.board[d[0]][d[1]] = self.board[d[0]][d[1]].replace("K","")

                    
        else:  #gold = True  ##or self.count >=60
            if self.x == 6 and self.y == 0: # and locate (6,0)
                self.Action = Agent.Action.CLIMB
            else: #choose destination back to (6,0)   ..  not at (6,0)
                self.path = []
                self.__getPath(self.x*10+self.y,60)
                if len(self.path) != 0:
                    d = self.path.pop()
                    
                    self.board[d[0]][d[1]] += "K" 
                    self.__move()
        
        
            #check path cost to choose destination
            #if startpoint = destination, check next des
            #else continue go to the destination follow the path


    def __move(self):
        if self.y+1 < 7 and "O" in self.board[self.x][self.y] and "K" in self.board[self.x][self.y+1]:
            #print ("#go right")
            if self.agentDir == 0:
                self.Action   = Agent.Action.FORWARD
            if self.agentDir == 1:
                self.Action   = Agent.Action.TURN_RIGHT
            if self.agentDir == 2:
                self.Action   = Agent.Action.TURN_RIGHT
            if self.agentDir == 3:
                self.Action   = Agent.Action.TURN_LEFT
                
                
                    
        elif self.x-1 >= 0 and "O" in self.board[self.x][self.y] and "K" in self.board[self.x-1][self.y]:
            #print ("#go up")
            if self.agentDir == 0:
                self.Action   = Agent.Action.TURN_LEFT
            if self.agentDir == 1:
                self.Action   = Agent.Action.FORWARD
            if self.agentDir == 2:
                self.Action   = Agent.Action.TURN_RIGHT
            if self.agentDir == 3:
                self.Action   = Agent.Action.TURN_RIGHT
                
                    
        elif self.y-1 >= 0 and "O" in self.board[self.x][self.y] and "K" in self.board[self.x][self.y-1]:
            #print ("#go left")
            if self.agentDir == 0:
                self.Action   = Agent.Action.TURN_RIGHT
            if self.agentDir == 1:
                self.Action   = Agent.Action.TURN_LEFT
            if self.agentDir == 2:
                self.Action   = Agent.Action.FORWARD
            if self.agentDir == 3:
                self.Action   = Agent.Action.TURN_RIGHT
                
                    
        elif self.x+1 < 7 and "O" in self.board[self.x][self.y] and "K" in self.board[self.x+1][self.y]:
            #print ("#go down")
            if self.agentDir == 0:
                self.Action   = Agent.Action.TURN_RIGHT
            if self.agentDir == 1:
                self.Action   = Agent.Action.TURN_RIGHT
            if self.agentDir == 2:
                self.Action   = Agent.Action.TURN_LEFT
            if self.agentDir == 3:
                self.Action   = Agent.Action.FORWARD


        else:
            #print("no way go")
            if len(self.walked) >= 2:
                d = self.walked.pop()
                d = self.walked.pop()
                
                if ([d[0]-1,d[1]] in self.avail) or ([d[0]+1,d[1]] in self.avail) or ([d[0],d[1]+1] in self.avail) or ([d[0],d[1]-1] in self.avail):
                    self.walked.append(d)
                self.board[d[0]][d[1]] += "K"
                self.__move()
            elif self.x == 6 and self.y == 0:
                self.Action = Agent.Action.CLIMB
            else:
                pass
                
                    
        
    def __getLast(self):
        if self.Action == Agent.Action.FORWARD:  
            self.lastAction = "FORWARD"
        if self.Action == Agent.Action.TURN_LEFT:   
            self.lastAction = "TURN_LEFT"
        if self.Action == Agent.Action.TURN_RIGHT:   
            self.lastAction = "TURN_RIGHT"
        if self.Action == Agent.Action.GRAB:   
            self.lastAction = "GRAB"
        if self.Action == Agent.Action.CLIMB:   
            self.lastAction = "CLIMB"
        if self.Action == Agent.Action.SHOOT:   
            self.lastAction = "SHOOT"


    def __killW(self):
        #0:right 1:up 2:left 3:down
        #print("we are in the killing function")
        if self.x+1 <7 and "W" in self.board[self.x+1][self.y]:# wumpus at down
            #print("we are in the killing function down")
            if self.agentDir == 0:
                self.Action   = Agent.Action.TURN_RIGHT
            if self.agentDir == 1:
                self.Action   = Agent.Action.TURN_RIGHT
            if self.agentDir == 2:
                self.Action   = Agent.Action.TURN_LEFT
            if self.agentDir == 3:
                self.Action   = Agent.Action.SHOOT
                
        elif self.x-1 >= 0 and "W" in self.board[self.x-1][self.y]: # wumpus at up
            #print("we are in the killing function up")
            if self.agentDir == 0:
                self.Action   = Agent.Action.TURN_LEFT
            if self.agentDir == 1:
                self.Action   = Agent.Action.SHOOT
            if self.agentDir == 2:
                self.Action   = Agent.Action.TURN_RIGHT
            if self.agentDir == 3:
                self.Action   = Agent.Action.TURN_RIGHT
                
        elif self.y+1 < 7 and "W" in self.board[self.x][self.y+1]: # wumpus at right
            #print("we are in the killing function right")
            if self.agentDir == 0:
                self.Action   = Agent.Action.SHOOT
            if self.agentDir == 1:
                self.Action   = Agent.Action.TURN_RIGHT
            if self.agentDir == 2:
                self.Action   = Agent.Action.TURN_RIGHT
            if self.agentDir == 3:
                self.Action   = Agent.Action.TURN_LEFT
                
        elif self.y-1 >= 0 and "W" in self.board[self.x][self.y-1]:# wumpus at left
            #print("we are in the killing function left")
            if self.agentDir == 0:
                self.Action   = Agent.Action.TURN_RIGHT
            if self.agentDir == 1:
                self.Action   = Agent.Action.TURN_LEFT
            if self.agentDir == 2:
                self.Action   = Agent.Action.SHOOT
            if self.agentDir == 3:
                self.Action   = Agent.Action.TURN_RIGHT

        else:
            self.findW = False
            self.__move()
            
# BFS
    def __addEdge(self,node,nextNode):
        if node not in self.graph:
            self.graph.update({node : [nextNode]})
        else:
            if nextNode not in self.graph[node]:
                self.graph[node].append(nextNode)

    def __bfs(self, start, goal):
        ways = {}
        visited = set()
        queue = [start]

        while queue:
            node = queue.pop(0)
            if node not in visited:
                visited.add(node)
                if node == goal:
                    return ways
                if node in self.graph:
                    for neighbor in self.graph[node]:
                        if neighbor not in visited:
                            ways[neighbor] = node
                            queue.append(neighbor)

        return ways

    def __getPath(self,start,goal):
        ways =  self.__bfs(start,goal)
        now = goal
        while(now != start):
            if [now/10,now%10] not in self.path:
                self.path.append([int(now/10),now%10])
            if now in ways:
                now = ways[now]



