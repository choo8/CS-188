# search.py
# ---------
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


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util
from sets import Set
import copy

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:
    """
    "*** YOUR CODE HERE ***"
    visited_states = Set()
    dfs_fringe = util.Stack()
    action_fringe = util.Stack()
    
    dfs_fringe.push([problem.getStartState()])
    action_fringe.push([])

    while True:
        if dfs_fringe.isEmpty():
            return []

        cur_fringe = dfs_fringe.pop() # The current list of states
        cur_action = action_fringe.pop() # The current list of actions to take to get to current state

        # Checks if latest node in fringe is goal state
        if problem.isGoalState(cur_fringe[-1]):
            return cur_action
        
        if cur_fringe[-1] not in visited_states:
            visited_states.add(cur_fringe[-1])
            for child in problem.getSuccessors(cur_fringe[-1]):
                # Update the state fringe
                temp = copy.copy(cur_fringe)
                temp.append(child[0])  
                dfs_fringe.push(copy.copy(temp))
                # Update the list of action
                temp = copy.copy(cur_action)
                temp.append(child[1])
                action_fringe.push(copy.copy(temp))

def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    visited_states = Set()
    bfs_fringe = util.Queue()
    action_fringe = util.Queue()
    
    bfs_fringe.push([problem.getStartState()])
    action_fringe.push([])

    while True:
        if bfs_fringe.isEmpty():
            return []

        cur_fringe = bfs_fringe.pop() # The current list of states
        cur_action = action_fringe.pop() # The current list of actions to take to get to current state

        # Checks if latest node in fringe is goal state
        if problem.isGoalState(cur_fringe[-1]):
            return cur_action
        
        if cur_fringe[-1] not in visited_states:
            visited_states.add(cur_fringe[-1])
            for child in problem.getSuccessors(cur_fringe[-1]):
                # Update the state fringe
                temp = copy.copy(cur_fringe)
                temp.append(child[0])  
                bfs_fringe.push(copy.copy(temp))
                # Update the list of action
                temp = copy.copy(cur_action)
                temp.append(child[1])
                action_fringe.push(copy.copy(temp))

def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    visited_states = Set()
    ucs_fringe = util.PriorityQueue()
    action_fringe = util.PriorityQueue()
    
    ucs_fringe.push([[problem.getStartState()], 0], 0)
    action_fringe.push([[], 0], 0)

    while True:
        if ucs_fringe.isEmpty():
            return []

        cur_fringe = ucs_fringe.pop() # The current list of states and its priority
        cur_action = action_fringe.pop() # The current list of actions to take to get to current state

        # Checks if latest node in fringe is goal state
        if problem.isGoalState(cur_fringe[0][-1]):
            return cur_action[0]
        
        if cur_fringe[0][-1] not in visited_states:
            visited_states.add(cur_fringe[0][-1])
            for child in problem.getSuccessors(cur_fringe[0][-1]):
                # Update the state fringe
                temp = copy.deepcopy(cur_fringe)
                temp[0].append(child[0])
                temp[1] = temp[1] + child[2]  
                ucs_fringe.push(copy.deepcopy(temp), temp[1])
                # Update the list of action
                temp = copy.deepcopy(cur_action)
                temp[0].append(child[1])
                temp[1] = temp[1] + child[2]
                action_fringe.push(copy.deepcopy(temp), temp[1])

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    visited_states = Set()
    astar_fringe = util.PriorityQueue()
    action_fringe = util.PriorityQueue()
    
    astar_fringe.push([[problem.getStartState()], 0], 0)
    action_fringe.push([[], 0], 0)

    while True:
        if astar_fringe.isEmpty():
            return []

        cur_fringe = astar_fringe.pop() # The current list of states and its priority
        cur_action = action_fringe.pop() # The current list of actions to take to get to current state

        # Checks if latest node in fringe is goal state
        if problem.isGoalState(cur_fringe[0][-1]):
            return cur_action[0]
        
        if cur_fringe[0][-1] not in visited_states:
            visited_states.add(cur_fringe[0][-1])
            for child in problem.getSuccessors(cur_fringe[0][-1]):
                # Update the state fringe
                temp = copy.deepcopy(cur_fringe)
                temp[0].append(child[0])
                temp[1] = temp[1] + child[2]
                astar_fringe.push(copy.deepcopy(temp), temp[1] + heuristic(child[0], problem))
                # Update the list of action
                temp = copy.deepcopy(cur_action)
                temp[0].append(child[1])
                temp[1] = temp[1] + child[2]
                action_fringe.push(copy.deepcopy(temp), temp[1] + heuristic(child[0], problem))


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
