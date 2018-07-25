# multiAgents.py
# --------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
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
        # print(legalMoves)

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        # print(gameState)
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        # chosenIndex = random.choice(bestIndices) # Pick randomly among the best
        chosenIndex = bestIndices[0]
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

        oldfood = currentGameState.getFood()
        #The Pacman should not remain in stop state
        if action == "Stop":
            return -1000

        #If the pacman position and new ghost position are same, check if the ghost is scared then eat it otherwise run away.
        factor = 0
        for i in range(len(newGhostStates)):
            if newGhostStates[i].getPosition() == newPos and newScaredTimes[i] > 0:
                factor =  0
            elif newGhostStates[i].getPosition() == newPos and newScaredTimes[i] <= 0:
                factor =  -10000

        d = 1000
        #d = distance of closest food particle from the pacman in the new position
        # More the closest distance more the penalty
        for food in oldfood.asList():
            d = min(d,manhattanDistance(food, newPos))

        d1 = 1000
    	caps = currentGameState.getCapsules()
    	for cap in caps:
        	d1 = min(d1,manhattanDistance(cap,newPos))
        if len(caps) == 0:
        	d1=0
        return -d1-2*d + factor


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
        cur_depth = 0
        result = self.helper(cur_depth,gameState,0)
        return result[1]
        util.raiseNotDefined()

    def helper(self, cur_depth, gameState,agentIndex):
        if agentIndex == gameState.getNumAgents():
            agentIndex = 0
            if cur_depth == self.depth:
                return [self.evaluationFunction(gameState)]

        if agentIndex == 0:
            result = self.MaxValue(cur_depth+1,gameState,agentIndex)
        else:
            result = self.MinValue(cur_depth,gameState,agentIndex)

        return result

    def MaxValue(self,cur_depth,gameState,agentIndex):

        actions = gameState.getLegalActions(agentIndex)
        if len(actions) == 0:
            return [self.evaluationFunction(gameState)]
        scores = []
        for a in actions:
            newGameState = gameState.generateSuccessor(agentIndex,a)
            temp = self.helper(cur_depth,newGameState,agentIndex+1)
            scores.append(temp[0])

        maxs = max(scores)
        i = scores.index(maxs)
        return [maxs,actions[i]]

    def MinValue(self,cur_depth,gameState,agentIndex):
        actions = gameState.getLegalActions(agentIndex)
        if len(actions) == 0:
            return [self.evaluationFunction(gameState)]
        
        scores = []
        for a in actions:
            newGameState = gameState.generateSuccessor(agentIndex,a)
            temp = self.helper(cur_depth,newGameState,agentIndex+1)
            scores.append(temp[0])

        mins = min(scores)
        i = scores.index(mins)
        return [mins,actions[i]]


class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        alpha = -10000
        beta = 10000
        cur_depth = 0
        result = self.helper(cur_depth,gameState,0,alpha,beta)
        return result[1]
        util.raiseNotDefined()

    def helper(self, cur_depth, gameState,agentIndex,alpha,beta):
        if agentIndex == gameState.getNumAgents():
            agentIndex = 0
            if cur_depth == self.depth:
                return [self.evaluationFunction(gameState)]

        if agentIndex == 0:
            result = self.MaxValue(cur_depth+1,gameState,agentIndex,alpha,beta)
        else:
            result = self.MinValue(cur_depth,gameState,agentIndex,alpha,beta)

        return result

    def MaxValue(self,cur_depth,gameState,agentIndex,alpha,beta):

        actions = gameState.getLegalActions(agentIndex)
        if len(actions) == 0:
            return [self.evaluationFunction(gameState)]
        scores = []
        for a in actions:
            newGameState = gameState.generateSuccessor(agentIndex,a)
            temp = self.helper(cur_depth,newGameState,agentIndex+1,alpha,beta)
            if temp[0] > beta:
                return [temp[0]]
            alpha = max(alpha, temp[0])
            scores.append(temp[0])

        maxs = max(scores)
        i = scores.index(maxs)
        return [maxs,actions[i]]

    def MinValue(self,cur_depth,gameState,agentIndex,alpha,beta):
        actions = gameState.getLegalActions(agentIndex)
        if len(actions) == 0:
            return [self.evaluationFunction(gameState)]
        
        scores = []
        for a in actions:
            newGameState = gameState.generateSuccessor(agentIndex,a)
            temp = self.helper(cur_depth,newGameState,agentIndex+1,alpha,beta)
            if temp[0] < alpha:
                return [temp[0]]
            beta = min(beta,temp[0])
            scores.append(temp[0])

        mins = min(scores)
        i = scores.index(mins)
        return [mins,actions[i]]

def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: Get the closest distance from the capsules, closest distance from the food. The lower they are the better it is for the pacman
      More food remaining means it is a bad state.
    """
    "*** YOUR CODE HERE ***"
    # successorGameState = currentGameState.generatePacmanSuccessor(action)
    newPos = currentGameState.getPacmanPosition()
    ghost_factor = 0
    min_distance_from_caps = 0
    min_distance_from_food = 0
    food_remaining = 0

    d = 1000
    caps = currentGameState.getCapsules()
    for cap in caps:
        d = min(d,manhattanDistance(cap,newPos))
    min_distance_from_caps = d
    # newFood = successorGameState.getFood()
    newGhostStates = currentGameState.getGhostStates()
    newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

    # "*** YOUR CODE HERE ***"

    oldfood = currentGameState.getFood()
    scare_factor = 0
    for i in range(len(newGhostStates)):
        if newScaredTimes[i] > 0:
            scare_factor += 80-3*manhattanDistance(newGhostStates[i].getPosition(),newPos)
        elif newScaredTimes[i] <= 0:
            ghost_factor = min(ghost_factor,manhattanDistance(newGhostStates[i].getPosition(),newPos))
    ghost_factor = max(ghost_factor,4)
    if(scare_factor > 0):
        ghost_factor = 0
    d = 1000
    for food in oldfood.asList():
        d = min(d,manhattanDistance(food, newPos))

    min_distance_from_food = d

    food_remaining = len(oldfood.asList())
    isWin = 0
    if currentGameState.isWin():
       isWin = 10000
    return isWin + scoreEvaluationFunction(currentGameState)-1*min_distance_from_food -0*min_distance_from_caps + 2*ghost_factor+scare_factor-4*food_remaining
    util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction

