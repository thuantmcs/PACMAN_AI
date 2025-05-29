# pacmanAgents.py
# ---------------
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


from pacman import Directions
from game import Agent
import random
import game
import util
from game import Agent, Directions
from util import manhattanDistance
import random

class ReflexAgent(Agent):
    def getAction(self, gameState):

        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices)  # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood().asList()
        ghostStates = successorGameState.getGhostStates()
        ghostPositions = [ghost.getPosition() for ghost in ghostStates]

        # LẤY THỜI GIAN POWER PELLET
        power_time = successorGameState.getPacmanState().powerTimer

        # Không chọn hành động STOP
        if action == Directions.STOP:
            return -float('inf')

        # Nếu Pacman đụng ma khi không có power => chết
        if newPos in ghostPositions and power_time == 0:
            return -1000

        score = successorGameState.getScore()

        # Ăn gần food
        if newFood:
            minFoodDist = min(util.manhattanDistance(newPos, foodPos) for foodPos in newFood)
            score += 10.0 / minFoodDist

        # Tính khoảng cách tới ghost
        if ghostPositions:
            minGhostDist = min(util.manhattanDistance(newPos, g) for g in ghostPositions)
            if power_time > 0:
                # Còn power => đến gần ghost
                score += 20.0 / (minGhostDist + 1)
            else:
                # Không có power => tránh xa ghost
                score -= 10.0 / (minGhostDist + 1)

        return score


class LeftTurnAgent(game.Agent):
    "An agent that turns left at every opportunity"

    def getAction(self, state):
        legal = state.getLegalPacmanActions()
        current = state.getPacmanState().configuration.direction
        if current == Directions.STOP: current = Directions.NORTH
        left = Directions.LEFT[current]
        if left in legal: return left
        if current in legal: return current
        if Directions.RIGHT[current] in legal: return Directions.RIGHT[current]
        if Directions.LEFT[left] in legal: return Directions.LEFT[left]
        return Directions.STOP

class GreedyAgent(Agent):

    def __init__(self, evalFn="scoreEvaluation"):
        self.evaluationFunction = util.lookup(evalFn, globals())
        assert self.evaluationFunction != None

    def getAction(self, state):
        # Generate candidate actions
        legal = state.getLegalPacmanActions()
        if Directions.STOP in legal: legal.remove(Directions.STOP)

        successors = [(state.generateSuccessor(0, action), action) for action in legal]
        scored = [(self.evaluationFunction(state), action) for state, action in successors]
        bestScore = max(scored)[0]
        bestActions = [pair[1] for pair in scored if pair[0] == bestScore]
        return random.choice(bestActions)

def scoreEvaluation(state):
    return state.getScore()