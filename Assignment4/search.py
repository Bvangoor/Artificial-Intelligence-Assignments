# search.py
# ---------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# For more info, see http://inst.eecs.berkeley.edu/~cs188/sp09/pacman.html
"""
In search.py, you will implement generic search algorithms which are called 
by Pacman agents (in searchAgents.py).
"""

from libxml2mod import last
from spade import pyxf
import sys

import util


class SearchProblem:
  """
  This class outlines the structure of a search problem, but doesn't implement
  any of the methods (in object-oriented terminology: an abstract class).
  
  You do not need to change anything in this class, ever.
  """
  
  def getStartState(self):
     """
     Returns the start state for the search problem 
     """
     util.raiseNotDefined()
    
  def isGoalState(self, state):
     """
       state: Search state
    
     Returns True if and only if the state is a valid goal state
     """
     util.raiseNotDefined()

  def getSuccessors(self, state):
     """
       state: Search state
     
     For a given state, this should return a list of triples, 
     (successor, action, stepCost), where 'successor' is a 
     successor to the current state, 'action' is the action
     required to get there, and 'stepCost' is the incremental 
     cost of expanding to that successor
     """
     util.raiseNotDefined()

  def getCostOfActions(self, actions):
     """
      actions: A list of actions to take
 
     This method returns the total cost of a particular sequence of actions.  The sequence must
     be composed of legal moves
     """
     util.raiseNotDefined()
           

def tinyMazeSearch(problem):
  """
  Returns a sequence of moves that solves tinyMaze.  For any other
  maze, the sequence of moves will be incorrect, so only use this for tinyMaze
  """
  from game import Directions
  s = Directions.SOUTH
  w = Directions.WEST
  return  [s,s,w,s,w,w,s,w]

def depthFirstSearch(problem):
  """
  Search the deepest nodes in the search tree first [p 85].
  
  Your search algorithm needs to return a list of actions that reaches
  the goal.  Make sure to implement a graph search algorithm [Fig. 3.7].
  
  To get started, you might want to try some of these simple commands to
  understand the search problem that is being passed in:
  
  print "Start:", problem.getStartState()
  print "Is the start a goal?", problem.isGoalState(problem.getStartState())
  print "Start's successors:", problem.getSuccessors(problem.getStartState())
  """
  "*** YOUR CODE HERE ***"
  f = open('maze.P','r')
  for line in f:
      if "goal" in line:
          g = line
  last = line
  print "lastline",last
  print "goal",g
  f.close()
  refine = last.split("(")
  refine2 = refine[1].split(")")
  startPac = refine2[0]
  myXSB = pyxf.xsb("/home/nikhil/Downloads/XSB/bin/xsb")
  myXSB.load("maze.P")
  myXSB.load("dfs.P")
  
  result = myXSB.query("depthFirstSearch("+startPac+", Path,Direction).")
  print result
  x = result[0]['Path']
  f1 = x.split("[")
  neededDir = f1[1].split(",")
  gg = g.split("(")
  g2 = gg[1].split(")")
  ls = []
  f2 = open('maze.P','r')
  for i in xrange(len(neededDir)):
      f2 = open('maze.P','r')
      for line1 in f2:
          if i+1<len(neededDir):
              stri = neededDir[i] + "," + neededDir[i+1]
              if i+1<len(neededDir) and stri in line1:
                  j = line1.split(",")
                  k = j[2].split(").")
                  print line1,neededDir[i],neededDir[i+1],k[0]
                  if g2[0]==neededDir[i+1]:
                      exit
                      
                  ls.append(str(k[0]))
                  continue
      f2.close()
      
  return ls

  
  

  
      
  """for x in xrange(len(array)):
      #print dict[array[x]]
      print array[x]"""
  


def breadthFirstSearch(problem):
  "Search the shallowest nodes in the search tree first. [p 81]"
  "*** YOUR CODE HERE ***"
  f = open('maze.P','r')
  for line in f:
    pass
  last = line
  refine = last.split("(")
  refine2 = refine[1].split(")")
  startPac = refine2[0]
  myXSB = pyxf.xsb("/home/nikhil/Downloads/XSB/bin/xsb")
  myXSB.load("maze.P")
  myXSB.load("bfs.P")
  if sys.argv=="CornersProblem":
      myXSB = pyxf.xsb("/home/nikhil/Downloads/XSB/bin/xsb")
      myXSB.load("maze.P")
      myXSB.load("CornersProblem.P")
      result = myXSB.query("breadthFirstSearch("+startPac+",Path,Direction).")
      print result
  else:
      result = myXSB.query("breadthFirstSearch("+startPac+",Path,Direction).")
      print result
      
def uniformCostSearch(problem):
  "Search the node of least total cost first. "
  "*** YOUR CODE HERE ***"
  #util.raiseNotDefined()
  
def nullHeuristic(state, problem=None):
  """
  A heuristic function estimates the cost from the current state to the nearest
  goal in the provided SearchProblem.  This heuristic is trivial.
  """
  return 0

def aStarSearch(problem, heuristic=nullHeuristic):
  "Search the node that has the lowest combined cost and heuristic first."
  "*** YOUR CODE HERE ***"
  f = open('maze.P','r')
  for line in f:
    pass
  last = line
  refine = last.split("(")
  refine2 = refine[1].split(")")
  startPac = refine2[0]
  myXSB = pyxf.xsb("/home/nikhil/Downloads/XSB/bin/xsb")
  myXSB.load("maze.P")
  myXSB.load("AStar.P")
  
  result = myXSB.query("AStarAlgorithm("+startPac+",Path,Direction).")
  print result
    
  
# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch