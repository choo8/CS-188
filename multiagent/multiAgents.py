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

import sys
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
        distGhost = 0
        for state in newGhostStates:
            distGhost = distGhost + manhattanDistance(state.getPosition(), newPos)

        distFood = 0
        nearestFood = sys.maxint
        for x, listFood in enumerate(newFood):
            for y, val in enumerate(listFood):
                if val:
                    temp = manhattanDistance((x,y), newPos)
                    distFood = distFood + temp
                    if temp < nearestFood:
                        nearestFood = temp

        if distGhost <= 1 and sum(newScaredTimes) == 0 and distGhost != 0:
            return -10000 

        elif distGhost <= 1 and sum(newScaredTimes) > 0 and distGhost != 0:
            return 1. / (distGhost + 1.)

        if nearestFood != sys.maxint:
            return successorGameState.getScore() + 11*(1./ nearestFood)
        else:
            return successorGameState.getScore()

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
        (score, action) = self.actionHelper(gameState, "max", 0, self.depth)
        return action

    def actionHelper(self, gameState, type, numGhosts, depth):
        if depth == 1:
            if type == "min":
                score = sys.maxint
                finalAction = ""
                if numGhosts == (gameState.getNumAgents() - 1):
                    for action in gameState.getLegalActions(numGhosts):
                        temp = gameState.generateSuccessor(numGhosts, action)
                        tempScore = self.evaluationFunction(temp)
                        if tempScore < score:
                            score = tempScore
                            finalAction = action
                    if score == sys.maxint:
                        score = self.evaluationFunction(gameState)
                else:
                    for action in gameState.getLegalActions(numGhosts):
                        temp = gameState.generateSuccessor(numGhosts, action)
                        (tempScore,_) = self.actionHelper(temp, "min", numGhosts + 1, depth)
                        if tempScore < score:
                            score = tempScore
                            finalAction = action
                    if score == sys.maxint:
                        score = self.evaluationFunction(gameState)
                return (score, finalAction)
            else:
                score = -sys.maxint
                finalAction = ""
                for action in gameState.getLegalActions(0):
                    temp = gameState.generateSuccessor(0, action)
                    (tempScore,_) = self.actionHelper(temp, "min", 1, depth)
                    if tempScore > score:
                        score = tempScore
                        finalAction = action
                if score == -sys.maxint:
                        score = self.evaluationFunction(gameState)
                return (score, finalAction)
        else:
            if type == "min":
                score = sys.maxint
                finalAction = ""
                if numGhosts == (gameState.getNumAgents() - 1):
                    for action in gameState.getLegalActions(numGhosts):
                        temp = gameState.generateSuccessor(numGhosts, action)
                        (tempScore,_) = self.actionHelper(temp, "max", 0, depth - 1)
                        if tempScore < score:
                            score = tempScore
                            finalAction = action
                    if score == sys.maxint:
                        score = self.evaluationFunction(gameState)
                else:
                    for action in gameState.getLegalActions(numGhosts):
                        temp = gameState.generateSuccessor(numGhosts, action)
                        (tempScore,_) = self.actionHelper(temp, "min", numGhosts + 1, depth)
                        if tempScore < score:
                            score = tempScore
                            finalAction = action
                    if score == sys.maxint:
                        score = self.evaluationFunction(gameState)
                return (score, finalAction)
            else:
                score = -sys.maxint
                finalAction = ""
                for action in gameState.getLegalActions(0):
                    temp = gameState.generateSuccessor(0, action)
                    (tempScore,_) = self.actionHelper(temp, "min", 1, depth)
                    if tempScore > score:
                        score = tempScore
                        finalAction = action
                if score == -sys.maxint:
                        score = self.evaluationFunction(gameState)    
                return (score, finalAction)

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        (score, action) = self.actionHelper(gameState, "max", 0, self.depth, -sys.maxint, sys.maxint)
        return action

    def actionHelper(self, gameState, type, numGhosts, depth, alpha, beta):
        curAlpha = alpha
        curBeta = beta
        if depth == 1:
            if type == "min":
                score = sys.maxint
                finalAction = ""
                if numGhosts == (gameState.getNumAgents() - 1):
                    for action in gameState.getLegalActions(numGhosts):
                        # Don't have to consider other children
                        if score < curAlpha:
                            return (score, finalAction)
                        temp = gameState.generateSuccessor(numGhosts, action)
                        tempScore = self.evaluationFunction(temp)
                        if tempScore < score:
                            score = tempScore
                            finalAction = action
                            curBeta = min(tempScore, curBeta)
                    if score == sys.maxint:
                        score = self.evaluationFunction(gameState)
                else:
                    for action in gameState.getLegalActions(numGhosts):
                        # Don't have to consider other children
                        if score < curAlpha:
                            return (score, finalAction)
                        temp = gameState.generateSuccessor(numGhosts, action)
                        (tempScore,_) = self.actionHelper(temp, "min", numGhosts + 1, depth, curAlpha, curBeta)
                        if tempScore < score:
                            score = tempScore
                            finalAction = action
                            curBeta = min(tempScore, curBeta)
                    if score == sys.maxint:
                        score = self.evaluationFunction(gameState)
                return (score, finalAction)
            else:
                score = -sys.maxint
                finalAction = ""
                for action in gameState.getLegalActions(0):
                    # Don't have to consider other children
                    if score > curBeta:
                        return (score, finalAction)
                    temp = gameState.generateSuccessor(0, action)
                    (tempScore,_) = self.actionHelper(temp, "min", 1, depth, curAlpha, curBeta)
                    if tempScore > score:
                        score = tempScore
                        finalAction = action
                        curAlpha = max(tempScore, curAlpha)
                if score == -sys.maxint:
                        score = self.evaluationFunction(gameState)
                return (score, finalAction)
        else:
            if type == "min":
                score = sys.maxint
                finalAction = ""
                if numGhosts == (gameState.getNumAgents() - 1):
                    for action in gameState.getLegalActions(numGhosts):
                        # Don't have to consider other children
                        if score < curAlpha:
                            return (score, finalAction)
                        temp = gameState.generateSuccessor(numGhosts, action)
                        (tempScore,_) = self.actionHelper(temp, "max", 0, depth - 1, curAlpha, curBeta)
                        if tempScore < score:
                            score = tempScore
                            finalAction = action
                            curBeta = min(tempScore, curBeta)
                    if score == sys.maxint:
                        score = self.evaluationFunction(gameState)
                else:
                    for action in gameState.getLegalActions(numGhosts):
                        # Don't have to consider other children
                        if score < curAlpha:
                            return (score, finalAction)
                        temp = gameState.generateSuccessor(numGhosts, action)
                        (tempScore,_) = self.actionHelper(temp, "min", numGhosts + 1, depth, curAlpha, curBeta)
                        if tempScore < score:
                            score = tempScore
                            finalAction = action
                            curBeta = min(tempScore, curBeta)
                    if score == sys.maxint:
                        score = self.evaluationFunction(gameState)
                return (score, finalAction)
            else:
                score = -sys.maxint
                finalAction = ""
                for action in gameState.getLegalActions(0):
                    # Don't have to consider other children
                    if score > curBeta:
                        return (score, finalAction)
                    temp = gameState.generateSuccessor(0, action)
                    (tempScore,_) = self.actionHelper(temp, "min", 1, depth, curAlpha, curBeta)
                    if tempScore > score:
                        score = tempScore
                        finalAction = action
                        curAlpha = max(tempScore, curAlpha)
                if score == -sys.maxint:
                        score = self.evaluationFunction(gameState)    
                return (score, finalAction)

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
        (score, action) = self.actionHelper(gameState, "max", 0, self.depth)
        return action

    def actionHelper(self, gameState, type, numGhosts, depth):
        if depth == 1:
            if type == "min":
                score = 0
                finalAction = ""
                numActions = len(gameState.getLegalActions(numGhosts))
                if numGhosts == (gameState.getNumAgents() - 1):
                    for action in gameState.getLegalActions(numGhosts):
                        temp = gameState.generateSuccessor(numGhosts, action)
                        score = score + (1./numActions)*self.evaluationFunction(temp)
                    if numActions == 0:
                        score = self.evaluationFunction(gameState)
                else:
                    for action in gameState.getLegalActions(numGhosts):
                        temp = gameState.generateSuccessor(numGhosts, action)
                        (tempScore,_) = self.actionHelper(temp, "min", numGhosts + 1, depth)
                        score = score + (1./numActions)*tempScore
                    if numActions == 0:
                        score = self.evaluationFunction(gameState)
                return (score, finalAction)
            else:
                score = -sys.maxint
                finalAction = ""
                for action in gameState.getLegalActions(0):
                    temp = gameState.generateSuccessor(0, action)
                    (tempScore,_) = self.actionHelper(temp, "min", 1, depth)
                    if tempScore > score:
                        score = tempScore
                        finalAction = action
                if score == -sys.maxint:
                        score = self.evaluationFunction(gameState)
                return (score, finalAction)
        else:
            if type == "min":
                score = 0
                finalAction = ""
                numActions = len(gameState.getLegalActions(numGhosts))
                if numGhosts == (gameState.getNumAgents() - 1):
                    for action in gameState.getLegalActions(numGhosts):
                        temp = gameState.generateSuccessor(numGhosts, action)
                        (tempScore,_) = self.actionHelper(temp, "max", 0, depth - 1)
                        score = score + (1./numActions)*tempScore
                    if numActions == 0:
                        score = self.evaluationFunction(gameState)
                else:
                    for action in gameState.getLegalActions(numGhosts):
                        temp = gameState.generateSuccessor(numGhosts, action)
                        (tempScore,_) = self.actionHelper(temp, "min", numGhosts + 1, depth)
                        score = score + (1./numActions)*tempScore
                    if numActions == 0:
                        score = self.evaluationFunction(gameState)
                return (score, finalAction)
            else:
                score = -sys.maxint
                finalAction = ""
                for action in gameState.getLegalActions(0):
                    temp = gameState.generateSuccessor(0, action)
                    (tempScore,_) = self.actionHelper(temp, "min", 1, depth)
                    if tempScore > score:
                        score = tempScore
                        finalAction = action
                if score == -sys.maxint:
                        score = self.evaluationFunction(gameState)    
                return (score, finalAction)

def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    # Useful information you can extract from a GameState (pacman.py)
    newPos = currentGameState.getPacmanPosition()
    newFood = currentGameState.getFood()
    newGhostStates = currentGameState.getGhostStates()
    newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

    "*** YOUR CODE HERE ***"
    distGhost = 0
    for state in newGhostStates:
        distGhost = min(distGhost, manhattanDistance(state.getPosition(), newPos))

    distFood = 0
    nearestFood = sys.maxint
    for x, listFood in enumerate(newFood):
        for y, val in enumerate(listFood):
            if val:
                temp = manhattanDistance((x,y), newPos)
                distFood = distFood + temp
                if temp < nearestFood:
                    nearestFood = temp

    if distGhost <= 1 and sum(newScaredTimes) == 0 and distGhost != 0:
        return -10000 
    elif distGhost <= 3 and sum(newScaredTimes) > 0 and distGhost != 0:
        return 5. / (distGhost + 1.)
    if nearestFood != sys.maxint:
        return currentGameState.getScore() + 6*(1./ nearestFood)
    else:
        return currentGameState.getScore()

# Abbreviation
better = betterEvaluationFunction

