from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

class ReflexAgent(Agent):
    """
      A reflex agent chooses an action at each choice point by examining
      its alternatives via a state evaluation function.

      The code below is provided as a guide. You are welcome to change
      it in any way you see fit, so long as you don't touch the method
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

        if successorGameState.isWin():
            return float("inf")
        elif successorGameState.isLose():
            return -float("inf")

        ghostPosition = currentGameState.getGhostPosition(1)
        distFromGhost = util.manhattanDistance(ghostPosition, newPos)

        score = max(distFromGhost, 1) + successorGameState.getScore()

        allDots = newFood.asList()
        for dotPos in allDots:
            closestDot = min(util.manhattanDistance(dotPos, newPos), allDots)

        if (currentGameState.getNumFood() > successorGameState.getNumFood()):
            score += 100

        if action == Directions.STOP:
            score -= 1.5
        score -= 1.5 * closestDot

        powerPellets = currentGameState.getCapsules()
        if successorGameState.getPacmanPosition() in powerPellets:
            score += 100

        return score

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
      add functionality to all your adversarial search agents. Please do not
      remove anything, however.

      Note: this is an abstract class: one that should not be instantiated.  It's
      only partially specified, and designed to be extended. Agent (game.py)
      is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):

    def gameOver(self, gameState, depth):
        return gameState.isWin() or gameState.isLose(), depth == 0

    def maxValue(self, gameState, depth, numOfGhosts):

        if self.gameOver(gameState, depth):
           return self.evaluationFunction(gameState)

        v = -float("inf")
        pacman = 0
        v = map(lambda x: max(v, self.minValue(gameState.generateSuccessor(pacman, x), depth - 1, 1, numOfGhosts)))
        return v

    def minValue(self, gameState, depth, agentindex, numOfGhosts):

        if self.gameOver(gameState, depth):
            return self.evaluationFunction(gameState)

        v = +float("inf")

        if agentindex == numOfGhosts:
            v = map(lambda x: min(v, self.maxValue(gameState.generateSuccessor(agentindex, x), depth - 1, numOfGhosts)))
        else:
            v = map(lambda x:min(v, self.minValue(gameState.generateSuccessor(agentindex, x), depth, agentindex + 1, numOfGhosts)))
            return v

    def getAction(self, gameState):

        legalActions = gameState.getLegalActions()
        numOfGhosts = gameState.getNumAgents() - 1
        bestAction = Directions.STOP
        score = -float("inf")

        for action in legalActions:
            nextState = gameState.generateSuccessor(0, action)
            prevScore = score
            score = max(score, self.minValue(nextState, self.depth, 1, numOfGhosts))

            if score > prevScore:
                bestAction = action

            return bestAction

class AlphaBetaAgent(MultiAgentSearchAgent):

    def gameOver(self, gameState, depth):
        return gameState.isWin() or gameState.isLose(), depth == 0

    def maxValue(self, gameState, alpha, beta, depth):

        pacman = 0

        if self.gameOver(gameState, depth):
            return self.evaluationFunction(gameState)

        v = -float("inf")
        legalActions = gameState.getLegalActions(pacman)

        nextState = map(lambda action: gameState.generateSuccessor(pacman, action), legalActions)
        v = max(v, self.minValue(nextState, alpha, beta, gameState.getNumAgents() - 1, depth))

        if v >= beta:
            return v
            alpha = max(alpha, v)
        return v

    def minValue(self, gameState, alpha, beta, agentindex, depth):

        numOfGhosts = gameState.getNumAgents() - 1

        #if self.gameOver(gameState, depth): return self.evaluationFunction(gameState)
        """
            IF WE REPLACE THE ABOVE IF-STATEMENT FOR THE ONE BELOW, PACMAN WINS ALMOST
            EVERYTIME... WIERD 'CAUSE IS THE SAME CODE... ANYHOW, PACMAN IS NOT SUPPOSE TO WIN,
            WE SHOULD, ON THE OTHER HAND, GET THE SAME RESULT AS IN MINIMAXAGENT, THAT'S TO
            SAY, -492 OR SO.

            PACMAN.PY
            -p AlphaBetaAgent  -l minimaxClassic  -a depth=1
        """
        if gameState.isWin() or gameState.isLose() or depth == 0: return self.evaluationFunction(gameState)

        v = +float("inf")
        legalActions = gameState.getLegalActions(agentindex)

        #nextState = map(lambda action: gameState.generateSuccessor(agentindex, action), legalActions)
        #Too much red-tape to make this work...

        for action in legalActions:

            nextState = gameState.generateSuccessor(agentindex, action)

            if agentindex == numOfGhosts:
                v = min(v, self.maxValue(nextState, alpha, beta, depth - 1))

                if v <= alpha:
                    return v
                beta = min(beta, v)
            else:
                v = min(v, self.minValue(nextState, alpha, beta, agentindex + 1, depth))
                if v <= alpha:
                    return v
                beta = min(beta, v)

        return v

    def getAction(self, gameState):

        pacman = 0
        legalActions = gameState.getLegalActions(pacman)
        bestAction = Directions.STOP
        score = -(float("inf"))
        alpha = -(float("inf"))
        beta = float("inf")

        for action in legalActions:

            nextState = gameState.generateSuccessor(pacman, action)
            prevScore = score
            score = max(score, self.minValue(nextState, alpha, beta, 1, self.depth))

            if score > prevScore:
                bestAction = action
            if score >= beta:
                return bestAction
            alpha = max(alpha, score)

        return bestAction

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent
    """
    def getAction(self, gameState):
        """
          Returns the expectimax action using self.depth and self.evaluationFunction

          All ghosts should be modeled as choosing uniformly at random from their
          legal moves.
        """
        "*** YOUR CODE HERE ***"

        def expValue(gameState, agentindex, depth):
            if gameState.isWin() or gameState.isLose() or depth == 0:
                return self.evaluationFunction(gameState)
            numberOfGhosts = gameState.getNumAgents() - 1
            legalActions = gameState.getLegalActions(agentindex)
            n = len(legalActions)
            v = 0
            for action in legalActions:
                nextState = gameState.generateSuccessor(agentindex, action)
                if (agentindex == numberOfGhosts):
                    v += maxValue(nextState, depth - 1)
                else:
                    v += expValue(nextState, agentindex + 1, depth)
            return v / n

        def maxValue(gameState, depth):
            if gameState.isWin() or gameState.isLose() or depth == 0:
                return self.evaluationFunction(gameState)
            legalActions = gameState.getLegalActions(0)
            v = -(float("inf"))
            for action in legalActions:
                nextState = gameState.generateSuccessor(0, action)
                v = max(v, expValue(nextState, 1, depth))
            return v

        if gameState.isWin() or gameState.isLose() or self.depth == 0:
            return self.evaluationFunction(gameState)
        legalActions = gameState.getLegalActions(0)
        bestAction = Directions.STOP
        v = -(float("inf"))
        for action in legalActions:
            nextState = gameState.generateSuccessor(0, action)
            prev = v
            v = max(v, expValue(nextState, 1, self.depth))
            if v > prev:
                bestAction = action
        return bestAction

def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function.

      DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction