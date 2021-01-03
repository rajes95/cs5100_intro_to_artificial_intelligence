'''
21p1.py

Implementation of Reinforcement Learning modules based on:
https://github.com/aimacode/aima-python/blob/master/reinforcement_learning.ipynb

DUE, TD, ADP algorithms are used to evaluate the viability of a possibility

@author: Rajesh Sakhamuru
@version: 12/3/2019
'''

from imports.reinforcement_learning4e import PassiveDUEAgent
from imports.reinforcement_learning4e import PassiveADPAgent
from imports.reinforcement_learning4e import PassiveTDAgent
from imports.reinforcement_learning4e import run_single_trial

from imports.mdp4e import GridMDP

# import 4x3 grid environment
from imports.mdp4e import sequential_decision_environment
"""
sequential_decision_environment = GridMDP([[-0.04, -0.04, -0.04, +1],
                                           [-0.04, None, -0.04, -1],
                                           [-0.04, -0.04, -0.04, -0.04]],
                                          terminals=[(3, 2), (3, 1)])
"""


def utilityPolicy(policy, decision_environment):
    """
    Evaluates the policy in the given decision environment using DUE, TD and ADP
    algorithms.
    
    The utility estimates for each algorithm used are then printed out.
    
    """
    print("Direct Utility Estimation (DUE):")

    DUEagent = PassiveDUEAgent(policy, decision_environment)
    for _ in range(200):
        run_single_trial(DUEagent, decision_environment)
        DUEagent.estimate_U()

    print('\n'.join([str(k) + ':' + str(v) for k, v in DUEagent.U.items()]))

    print("\nTemporal-difference learning (TD)")

    TDagent = PassiveTDAgent(policy, decision_environment, alpha=lambda n: 60. / (59 + n))
    for _ in range(200):
        run_single_trial(TDagent, decision_environment)

    print('\n'.join([str(k) + ':' + str(v) for k, v in TDagent.U.items()]))

    print("\nAdaptive Dynamic Programming (ADP):")

    ADPagent = PassiveADPAgent(policy, decision_environment)

    for _ in range(200):
        run_single_trial(ADPagent, decision_environment)

    print('\n'.join([str(k) + ':' + str(v) for k, v in ADPagent.U.items()]))


def main():

    # Action Directions
    north = (0, 1)
    south = (0, -1)
    west = (-1, 0)
    east = (1, 0)

    policy1 = {
        (0, 2): east, (1, 2): east, (2, 2): east, (3, 2): None,
        (0, 1): north, (2, 1): north, (3, 1): None,
        (0, 0): north, (1, 0): east, (2, 0): north, (3, 0): west, }

    policy2 = {
        (0, 2): east, (1, 2): south, (2, 2): east, (3, 2): None,
        (0, 1): north, (2, 1): north, (3, 1): None,
        (0, 0): east, (1, 0): north, (2, 0): north, (3, 0): west, }

    biggerGrid = GridMDP([[-0.04, -0.04, -0.04, +1],
                          [-0.04, None, -0.04, -1],
                          [-0.04, -0.04, -0.04, -0.04],
                          [-0.04, None, -0.04, -0.04],
                          [-0.04, None, -0.04, -0.04]],
                          terminals=[(3, 4), (3, 3)])

    policy3 = {
        (0, 4): east, (1, 4): east, (2, 4): east, (3, 4): None,
        (0, 3): north, (2, 3): north, (3, 3): None,
        (0, 2): east, (1, 2): east, (2, 2): north, (3, 2): west,
        (0, 1): north, (2, 1): north, (3, 1): west,
        (0, 0): north, (2, 0): north, (3, 0): west, }

    biggerGridNoObstacles = GridMDP([[-0.04, -0.04, -0.04, +1],
                                      [-0.04, -0.04, -0.04, -1],
                                      [-0.04, -0.04, -0.04, -0.04],
                                      [-0.04, -0.04, -0.04, -0.04],
                                      [-0.04, -0.04, -0.04, -0.04]],
                                      terminals=[(3, 4), (3, 3)])

    policy4 = {
        (0, 4): east, (1, 4): east, (2, 4): east,  (3, 4): None,
        (0, 3): east, (1, 3): east, (2, 3): north, (3, 3): None,
        (0, 2): east, (1, 2): east, (2, 2): north, (3, 2): west,
        (0, 1): east, (1, 1): east, (2, 1): north, (3, 1): west,
        (0, 0): east, (1, 0): east, (2, 0): north, (3, 0): west, }

    print("4x3 grid and POLICY 1 (optimal):\n")
    utilityPolicy(policy1, sequential_decision_environment)

    print("\n---------------\n4x3 grid and POLICY 2 (not optimal):\n")
    utilityPolicy(policy2, sequential_decision_environment)

    print("\n---------------\nBigger grid (Obstacles) and POLICY 3:\n")
    utilityPolicy(policy3, biggerGrid)

    print("\n---------------\nBigger grid (NO OBSTACLES) and POLICY 4:\n")
    utilityPolicy(policy4, biggerGridNoObstacles)

    return


main()

