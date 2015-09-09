# multiAgents.py
# --------------
# Licensing Information:  You are free to use or extend these projects for 
# educational purposes provided that (1) you do not distribute or publish 
# solutions, (2) you retain this notice, and (3) you provide clear 
# attribution to UC Berkeley, including a link to 
# http://inst.eecs.berkeley.edu/~cs188/pacman/pacman.html
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero 
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and 
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent
from operator import or_

class ReflexAgent(Agent):
    """
      A reflex agent chooses an action at each choice point by examining
      its alternatives via a state evaluation function.

      The code below is provided as a guide.  You are welcome to change
      it in any way you see fit, so long as you don't touch our method
      headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {North, South, West, East, Stop}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"            
        #Initializing score to zero    
        myEvalScore = 0    
        #Obtaining the Food Positions
        foodPositionList = newFood.asList()
        foodDistanceList = []
        ghostDistanceList = [] 
        #Finding all manhattan distances from the pacman position to the available food positions and storing them in a list 
        for foodPos in foodPositionList :
            foodDistanceList.append(manhattanDistance(foodPos, newPos))
        # Finding all the manhattan distances from the pacman position to the ghosts locations and storing them in a list    
        for ghost in newGhostStates :
            ghostDistanceList.append(manhattanDistance(ghost.getPosition(), newPos))
        for ghostDistance in ghostDistanceList :
            if ((len(foodDistanceList) == 0) or (min(foodDistanceList) == 0)) :
                # For each manhattan distance from ghost that is available we are calculating score 
                # as multiplication of ghost distance and 0.5 times reciprocal of minimum food distance available 
                # but if food distance is zero then we simply return twice the ghost distance
                myEvalScore = myEvalScore + (ghostDistance*2)
            else :
                # For each manhattan distance from ghost that is available we are calculating score 
                # as multiplication of ghost distance and 0.5 times reciprocal of minimum food distance available
                myEvalScore = myEvalScore + (ghostDistance*(0.5/min(foodDistanceList)))         
        return (successorGameState.getScore() + myEvalScore )

def scoreEvaluationFunction(currentGameState):
    """
      This default evaluation function just returns the score of the state.
      The score is the same one displayed in the Pacman GUI.

      This evaluation function is meant for use with adversarial search agents
      (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
      This class provides some common elements to all of your
      multi-agent searchers.  Any methods defined here will be available
      to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

      You *do not* need to make any changes here, but you can if you want to
      add functionality to all your adversarial search agents.  Please do not
      remove anything, however.

      Note: this is an abstract class: one that should not be instantiated.  It's
      only partially specified, and designed to be extended.  Agent (game.py)
      is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
      Your minimax agent (question 2)
    """
    #This is the logic of the minimax algorithm which returns the best value and the best action for the max i.e Pac Man. 
    #It take's agent,gamestate,depth and number of agents that are present in game as arguments.
    
    def minimax(self,agent,gameState,depth,totalAgents):
        bestAction = []
        successorList=[]        
        count = 0
        #Checking whether the given node is a terminal node or not with the help of depth (if it is zero) or 
        # with the isWin() or isLose() functions which return true in either of the case when the node is the win state or lose state respectively
        #In the Terminal Node case we return evaluation number for that node using evaluationFunction() and return STOP as the action.
        if depth == 0 or gameState.isWin() or gameState.isLose():
            return self.evaluationFunction(gameState),Directions.STOP
        #If it is not a terminal Node then next thing which we check is whether it is Max move (in our case it is Pac man's with agent number zero)
        if agent == 0 :
            bestValue = float("-inf")
            #If it is Pac-man's move then we find out the legal actions for that state and generate's it's successor
            actions = gameState.getLegalActions(agent)
            for action in actions :
                successorList.append([action,gameState.generateSuccessor(agent,action)])            
            for successor in successorList :
                # For each successor that we generated we call the minimax but with incremented agent number
                # as now the move is for ghosts and the depth is decreased by one unit
                 val,retAct = self.minimax((agent+1)%totalAgents,successor[1],depth-1,totalAgents)
                 #As we get the evaluated values for each successor we compare it with the best value(-infinity) for max and take the maximum of both.
                 bestValue = max(bestValue,val)
                 if bestValue == val :
                     #when ever we are storing the best value i.e when ever it is getting updated we will store the action as well as we return both
                     bestAction = successor[0]
            return bestValue,bestAction
        else:
            bestValue = float("inf")
            #Since it is not max's move it is min's move which in our case is ghosts where the agent number is not zero
            successorList=[]
            actions = gameState.getLegalActions(agent)
            for action in actions :
                successorList.append([action,gameState.generateSuccessor(agent,action)])            
            for successor in successorList :
                #For each successor that we generated we call the minimax but with incremented agent number
                # as now the move is for next ghosts or a pac man(depending on agent number) and the depth is decreased by one unit
                val,retAct = self.minimax((agent+1)%totalAgents,successor[1],depth-1,totalAgents)
                #As we get the evaluated values for each successor we compare it with the best value(+infinity) for min and take the minimum of both.
                bestValue = min(bestValue,val)
                if bestValue == val :
                    #when ever we are storing the best value i.e when ever it is getting updated we will store the action as well as we return both
                    bestAction = successor[0]
            return bestValue,bestAction        
            
    def getAction(self, gameState):
        """
          Returns the minimax action from the current gameState using self.depth
          and self.evaluationFunction.

          Here are some method calls that might be useful when implementing minimax.

          gameState.getLegalActions(agentIndex):
            Returns a list of legal actions for an agent
            agentIndex=0 means Pacman, ghosts are >= 1

          gameState.generateSuccessor(agentIndex, action):
            Returns the successor game state after an agent takes an action

          gameState.getNumAgents():
            Returns the total number of agents in the game
        """
        "*** YOUR CODE HERE ***"
        #The agent number is zero for the PacMan
        agent = 0 
        # Taking depth as multiples of number of agents as we know that each depth in our Pac-man game is
        # one max move i.e (Pac man's) and the total number of ghosts move which is nothing but total number of agents that's 
        # why we are multiplying given depth with number of agents.
        depth = (self.depth)*(gameState.getNumAgents())  
        #Calling the minimax function with agent=0(Max move) as arguments.
        val1,retAct = self.minimax((agent)%(gameState.getNumAgents()),gameState, depth,gameState.getNumAgents())   
        return retAct

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """
    def minimaxwithAlphaBetaPruning(self,agent,gameState,depth,totalAgents,alpha,beta,action):
        bestAction = []
        #Checking whether the given node is a terminal node or not with the help of depth (if it is zero) or 
        # with the isWin() or isLose() functions which return true in either of the case when the node is the win state or lose state respectively
        #In the Terminal Node case we return evaluation number for that node using evaluationFunction() and return STOP as the action.  
        if depth == 0 or gameState.isWin() or gameState.isLose():
            return self.evaluationFunction(gameState),action
        #If it is not a terminal Node then next thing which we check is whether it is Max move (in our case it is Pac man's with agent number zero)
        if agent == 0 :
            bestValue = float("-inf")
            #If it is Pac-man's move then we find out the legal actions for that state and generate's it's successor
            actions = gameState.getLegalActions(agent)
            #For each successor that we generated we call the minimaxwithAlphaBetaPruning but with incremented agent number 
            # as now the move is for next ghosts or a pac man(depending on agent number) and the depth is decreased by one unit and updated alpha beta values
            for action in actions :         
                 val,retAct = self.minimaxwithAlphaBetaPruning((agent+1)%totalAgents,gameState.generateSuccessor(agent,action),depth-1,totalAgents,alpha,beta,action)
                 #As we get the evaluated values for each successor we compare it with the best value(-infinity) for max and take the maximum of both.
                 bestValue = max(bestValue,val)
                 if bestValue == val :
                     #when ever we are storing the best value i.e when ever it is getting updated we will store the action as well as we return both
                     bestAction = action
                 # We will update the alpha value at the max node with maximum of the value that is obtained from its successor and the current alpha value
                 alpha = max(alpha,bestValue)
                 # Whenever alpha cross the beta we will break out from there with out generating any new successors i.e we prune.
                 if beta < alpha :
                     break   
            return bestValue,bestAction
        else:
            bestValue = float("inf")
            #Since it is not max's move it is min's move which in our case is ghosts where the agent number is not zero
            actions = gameState.getLegalActions(agent)
            for action in actions :
                #For each successor that we generated we call the minimaxwithAlphaBetaPruning but with incremented agent number
                # as now the move is for next ghosts or a pac man(depending on agent number) and the depth is decreased by one unit and updated alpha beta values
                val,retAct = self.minimaxwithAlphaBetaPruning((agent+1)%totalAgents,gameState.generateSuccessor(agent,action),depth-1,totalAgents,alpha,beta,action)
                #As we get the evaluated values for each successor we compare it with the best value(+infinity) for min and take the minimum of both.
                bestValue = min(bestValue,val)
                if bestValue == val :
                    #when ever we are storing the best value i.e when ever it is getting updated we will store the action as well as we return both
                    bestAction = action
                # We will update the beta value at the min node with minimum of the value that is obtained from its successor and the current beta value
                beta = min(beta,bestValue)
                # Whenever alpha cross the beta we will break out from there with out generating any new successors i.e we prune.
                if beta < alpha :
                    break    
            return bestValue,bestAction
    

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        #The agent number is zero for the PacMan        
        agent = 0 
        #Taking alpha value as -infinity initially
        alpha = float("-inf")
        #Taking beta value as +infinity initially
        beta = float("inf")
        # Taking depth as multiples of number of agents as we know that each depth in our Pac-man game is
        # one max move i.e (Pac man's) and the total number of ghosts move which is nothing but total number of agents that's 
        # why we are multiplying given depth with number of agents.
        depth = (self.depth)*(gameState.getNumAgents())
        #Calling the minimaxwithAlphaBetaPruning function with agent=0(Max move) as arguments.
        val1,retAct = self.minimaxwithAlphaBetaPruning((agent)%(gameState.getNumAgents()),gameState, depth,gameState.getNumAgents(),alpha,beta,Directions.STOP)
        return retAct

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
          Returns the expectimax action using self.depth and self.evaluationFunction

          All ghosts should be modeled as choosing uniformly at random from their
          legal moves.
        """
        "*** YOUR CODE HERE ***"
        util.raiseNotDefined()

def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction

class ContestAgent(MultiAgentSearchAgent):
    """
      Your agent for the mini-contest
    """

    def getAction(self, gameState):
        """
          Returns an action.  You can use any method you want and search to any depth you want.
          Just remember that the mini-contest is timed, so you have to trade off speed and computation.

          Ghosts don't behave randomly anymore, but they aren't perfect either -- they'll usually
          just make a beeline straight towards Pacman (or away from him if they're scared!)
        """
        "*** YOUR CODE HERE ***"
        util.raiseNotDefined()

