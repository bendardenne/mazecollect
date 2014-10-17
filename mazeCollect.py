##                                                                ##
##  mazeCollect.py                                                ##
##  The Koutack Problem : Assigment 1                             ##
##                                                                ##
##  INGI2261                                                      ##
##                                                                ##
##  Created by Nicolas Van Wallendael && Benoit Dardenne          ##
##                                                                ##

from search import *
import operator


######################  State class  ###############################

#
#
#
#
#
class State :

    def __init__(self, newDollars=[], scroogePos=(-1,-1)):
        self.scrooge = scroogePos
        self.dollars = newDollars

    def addScrooge(self, pos):
        self.scrooge = pos

    def addDollar(self, pos):
        self.dollars.append(pos)

    def __str__(self):
        string = ['\n'] * (mazeWidth+1) * mazeHeigth

        for i in range(mazeHeigth) :
            for j in range(mazeWidth) :
                if (i,j) in maze:
                    string[i*(mazeWidth+1) + j] = '#'
                else:
                    string[i*(mazeWidth+1) + j] = ' '
    

        for dollar in self.dollars:
            string[dollar[0]*(mazeWidth+1) + dollar[1]] = '$'

        string[safe[0]*(mazeWidth+1) + safe[1]] = '+'

        string[self.scrooge[0]*(mazeWidth+1) + self.scrooge[1]] = '@'

        return "".join(string)
    
    def __hash__(self):
        return (self.scrooge, tuple(self.dollars)).__hash__()
    
    def __eq__(self, other):
        return self.dollars == other.dollars and self.scrooge == self.scrooge

    def minScroogeDistance(self, list):
        dist = 0
        for item in list:
            dx = abs(self.scrooge[0] - item[0])
            dy = abs(self.scrooge[1] - item[1])
            tmp = dx+dy
            if dist < tmp:
                dist = tmp

        return dist







######################  Implement the maze #######################

maze = {}
safe = (-1,-1)
mazeWidth  = 0
mazeHeigth = 0

moves = [(-1,0),(1,0),(0,-1),(0,1)]





######################  Implement the search #######################

class MazeCollect(Problem):
    
    def __init__(self,init):
        
        global safe    # Needed to modify global copy of globvar
        global mazeWidth    # Needed to modify global copy of globvar
        global mazeHeigth   # Needed to modify global copy of globvar
        
        self.initial = State()

        f = open(init, 'r')
        line = []
        
        # for each tile, add it to the State
        i = 0
        j = 0
        
        for line in f:
            j = 0
            for tile in line:
                if (tile == "#"):
                    self.addWall((i,j))
                elif (tile == "$"):
                    self.initial.addDollar((i,j))
                elif (tile == "+"):
                    safe = (i,j)
                elif (tile == "@"):
                    self.initial.addScrooge((i,j))
                
                j += 1
                #print(tile)
                    
            i += 1

        mazeWidth  = j - 1      #for '\n'
        mazeHeigth = i          #no EOF
        

    
    def goal_test(self, state):
    
        return state.dollars == [] and state.scrooge == safe
    
    def successor(self, state):
        for move in moves:
            newPos = tuple(map(operator.add, state.scrooge, move))
            
            #print(move)
            #print(newPos)

            if newPos in maze or not self.validPos(newPos):
                #print('newPos not Valid -> ' +str(newPos) + str(state.scrooge))
                continue
            
            #update dollars if we found a $
            newDollars = state.dollars[:]
            if newPos in newDollars: newDollars.remove(newPos)
            
            newState = State(newDollars, newPos)
            #print('newPos is  Valid -> ' +str(newPos) + str(state.scrooge))
            #print(newState)
            #print('\n\n'+'-------------------------------------------------'+'\n\n')
            
            yield( (move, newState) )

    
    def heuristic(self, node):
        
        #print('Distance = '+ str(node.state.minScroogeDistance([safe])))
        return node.state.minScroogeDistance(node.state.dollars) + node.state.minScroogeDistance([safe])
    
    def validPos(self,pos):
        return (pos[0] < mazeHeigth and pos[0] >= 0 and pos[1] < mazeWidth and pos[1] >= 0)
        
    def isWall(self, pos):
    
        return maze[pos]

    def addWall(self, pos):
        global maze    # Needed to modify global copy of globvar

        maze[pos] = True
    



###################### Launch the search #########################
problem=MazeCollect(sys.argv[1])

node = astar_graph_search(problem, problem.heuristic)


#example of print
path = node.path()
path.reverse()
for n in path:
    print(n.state)
    for z in range(37-mazeHeigth):
        print('\n')

