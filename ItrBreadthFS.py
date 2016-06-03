# Frances Davies, fdavies
# CSE 415, Assignement 3, Part II, Problem 1
# 4/21/16

# ItrBFS.py
# Iterative Breadth-First Search of a problem space.
# The Problem should be given in a separate Python
# file using the "QUIET" file format.

import sys

if sys.argv==[''] or len(sys.argv)<2:
  import WickedWerewolf as Problem
else:
  import importlib
  Problem = importlib.import_module(sys.argv[1])


print("\nWelcome to ItrBFS")
COUNT = None
BACKLINKS = {}

# runBFS sets up structures to be used by the iterative breadth first search.
def runBFS():
  initial_state = Problem.CREATE_INITIAL_STATE()
  print("Initial State:")
  print(Problem.DESCRIBE_STATE(initial_state))
  global COUNT, BACKLINKS
  COUNT = 0
  BACKLINKS = {}
  IterativeBFS(initial_state)
  print(str(COUNT)+" states examined.")

# IterativeBFS takes an initial state and finds the shortest path to the goal state.
def IterativeBFS(initial_state):
  global COUNT, BACKLINKS
  OPEN = [initial_state]
  CLOSED = [initial_state]
  BACKLINKS[Problem.HASHCODE(initial_state)] = -1
  while OPEN != []: # While a state exists that hasn't been explored
    S = OPEN.pop(0)
    COUNT += 1
    if Problem.GOAL_TEST(S): # If that state is the goal state, stop
      print(Problem.GOAL_MESSAGE_FUNCTION(S))
      backtrace(S)
      return
    else: # Else explore that state
      for op in Problem.OPERATORS:
        print(op.name)
        if op.precond(S):
          new_state = op.state_transf(S)
          if new_state not in CLOSED:
            CLOSED.append(new_state)
            OPEN.append(new_state)
            BACKLINKS[Problem.HASHCODE(new_state)] = S

def backtrace(S):
  global BACKLINKS

  path = []
  while not S == -1:
    path.append(S)
    S = BACKLINKS[Problem.HASHCODE(S)]
  path.reverse()
  print("Solution path: ")
  for s in path:
    print(Problem.DESCRIBE_STATE(s))
  return path    
  

def occurs_in(s1, lst):
  for s2 in lst:
    if Problem.DEEP_EQUALS(s1, s2): return True
  return False

if __name__=='__main__':
  runBFS()
