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
    def __init__(self):
        self.lastPos = None
        self.history = []

    def getAction(self, gameState):
        legalMoves = gameState.getLegalActions()
        if Directions.STOP in legalMoves:
            legalMoves.remove(Directions.STOP)

        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)

        # Lọc những action có điểm cao nhất
        bestIndices = [i for i, score in enumerate(scores) if score == bestScore]

        # Nếu có nhiều action điểm bằng nhau, ưu tiên action không quay lại vị trí trước
        filteredBest = []
        for i in bestIndices:
            successor = gameState.generatePacmanSuccessor(legalMoves[i])
            pos = successor.getPacmanPosition()
            if pos != self.lastPos:
                filteredBest.append(i)

        if len(filteredBest) == 0:
            filteredBest = bestIndices

        chosenIndex = random.choice(filteredBest)
        chosenAction = legalMoves[chosenIndex]

        # Cập nhật vị trí hiện tại để tránh đi lại
        successor = gameState.generatePacmanSuccessor(chosenAction)
        self.lastPos = successor.getPacmanPosition()

        # Lưu lịch sử để tránh lặp nhiều bước
        self.history.append(self.lastPos)
        if len(self.history) > 5:
            self.history.pop(0)

        return chosenAction

    def evaluationFunction(self, currentGameState, action):
        successor = currentGameState.generatePacmanSuccessor(action)
        newPos = successor.getPacmanPosition()
        newFood = successor.getFood()
        newGhostStates = successor.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        # Khoảng cách tới ghost
        ghostDistances = [manhattanDistance(newPos, ghostState.getPosition()) for ghostState in newGhostStates]

        # Phạt ghost gần (khi không scared)
        penalty = 0
        for dist, scaredTime in zip(ghostDistances, newScaredTimes):
            if scaredTime == 0 and dist <= 2:
                penalty += 1000 / (dist + 0.1)  # càng gần càng phạt nhiều

        # Tính khoảng cách thức ăn gần nhất
        foodList = newFood.asList()
        if foodList:
            minFoodDist = min(manhattanDistance(newPos, food) for food in foodList)
        else:
            minFoodDist = 0

        # Tổng điểm: ưu tiên tránh ghost, rồi tới thức ăn
        score = -minFoodDist - penalty

        # Phạt hành động đứng yên
        if action == Directions.STOP:
            score -= 100

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
