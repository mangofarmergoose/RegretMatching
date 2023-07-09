import numpy as np
import random

''' 
Setting of mixed extension of Nash Equilibrium
1.  Set N = {1, 2, · · · , n} of players 
2.  For each player i, a set P_i of all mixed strategies of player i
3.  For each player, a payoff function Hi : ∏i∈N P_i → R, where each Hi
is a linear combination of his with coefficients equal to product of the
corresponding probabilities

'''

# Declare Variables
ROCK, PAPER, SCISSORS, NUM_ACTIONS = 0, 1, 2, 3 
strategy = np.zeros(NUM_ACTIONS)
strategySum = np.zeros(NUM_ACTIONS)
regretSum = np.zeros(NUM_ACTIONS)
# Opponent uses the mixed strat (R, S, P) = (0.4, 0.3, 0.3)
oppStrategy = np.array([0.4, 0.3, 0.3])

def getValue(p1, p2):
    if p1 == p2:
        return 0 
    if p1 == ROCK and p2 == SCISSORS:
        return 1
    if p1 == SCISSORS and p2 == PAPER:
        return 1
    if p1 == PAPER and p2 == ROCK:
        return 1
    else:
        return -1

# accmulate in stratSum
def getStrategy():
    global regretSum, strategySum
    strategy = np.maximum(regretSum, 0)
    normalizingSum = np.sum(strategy)
    if normalizingSum > 0:
        strategy /= normalizingSum
    else:
        strategy = np.ones(NUM_ACTIONS)/NUM_ACTIONS
    strategySum += strategy
    return strategy

def getAction(strategy):
    # Returns a random number in (0,1)
    rr = random.random()
    # Returns 0, 1, 2 based on the mixed strategy
    return np.searchsorted(np.cumsum(strategy/np.sum(strategy)), rr)


def getStrategyPayoff(myStrat, oppStrat, iter1, iter2):
    vvv = []
    for i in range(iter1):
        vv = 0 
        for j in range(iter2):
            myAction = getAction(myStrat)
            oppAction = getAction(oppStrat)
            vv += getValue(myAction, oppAction)
        vvv.append(vv)

    return np.mean(vvv)

def updateRegretSum(myStrat, oppStrat, iter):
    # To train the algorithm and modify the regretSum array
    global regretSum
    actionPayoff = np.zeros(NUM_ACTIONS)
    for i in range(iter):
        
        oppAction = getAction(oppStrat)       

       # Compute Action Payoffs: ROCK 0; PAPER 1; SCISSORS 2
        actionPayoff[oppAction] = 0 
        actionPayoff[(oppAction+1)%NUM_ACTIONS] = 1
        actionPayoff[(oppAction+2)%NUM_ACTIONS] = -1 

        regretSum += actionPayoff

def getAverageStrategy():
    global strategySum
    normalizingSum = np.sum(strategySum)

    if normalizingSum > 0:
        avgStrategy = strategySum / normalizingSum
    else:
        avgStrategy = np.ones(NUM_ACTIONS)/NUM_ACTIONS

    return avgStrategy
        

def main():

    myStrat = getStrategy() # Use default mixed strat (1/3, 1/3, 1/3)
    print("Using default mixed strategy (1/3, 1/3, 1/3)")
    print(getStrategyPayoff(myStrat, oppStrategy, 100, 100))

    updateRegretSum(myStrat, oppStrategy, 100000) # Modify global variable regretSum
    
    myNewStrat = getStrategy()
    print("Using regret matched mixed strategy after training: ", myNewStrat)
    print(getStrategyPayoff(myNewStrat, oppStrategy, 100, 100))

main()