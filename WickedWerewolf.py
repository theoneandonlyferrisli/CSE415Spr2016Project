'''
Wicked Werewolf
Frances Davies & Yuefeng Li
5/31/16
'''

import random
import itertools

class Player:
    
    def init_remark(s):
        if s.niceness > 0.5 and s.likability > 0.5:
            return "I love games!"
        if s.niceness > 0.5 or s.likability > 0.5:
            return "Let's play!"
        else:
            return "I play to win."
        
    def __init__(s, name, kind, niceness, likability, suspicion):
        # constants
        s.name = name # p1, p2, p3...
        s.kind = kind # werewolf, villager, seer...
        s.niceness = niceness # 0-1
        s.likability = likability # 0-1
        s.suspicion = suspicion # 0-1
        s.next_remark = s.init_remark()

#<METADATA>
QUIET_VERSION = "0.1"
PROBLEM_NAME = "Wicked Werewolf"
PROBLEM_VERSION = "0.1"
PROBLEM_AUTHORS = ['Frances Davies', 'Yuefeng Li']
PROBLEM_CREATION_DATE = "31-MAY-2016"
PROBLEM_DESC=\
'''This problem uses generic
Python 3 constructs and has been tested with Python 3.4.
It is designed to work according to the QUIET tools interface.
'''
#</METADATA>

#<COMMON_CODE>
def DESCRIBE_STATE(state):
      # Produces a textual description of a state.
      # Might not be needed in normal operation with GUIs.
      return str(state)

def HASHCODE(s):
    return str(s)

def copy_state(s):
    return copy.deepcopy(s)

def can_move(s, werewolf, quality, change):
    players = s['players']
    for p in players:
        if p.name == 'W' + werewolf:
            value = 0
            if p.quality == 'niceness':
                value = p.niceness + change
            if p.quality == 'likability':
                value = p.likability + change
            if p.quality == 'suspicion':
                value = p.suspicion + change
            return value >= 0 and value <= 1

def move(s, werewolf, quality, change):
    '''
    you get the whole state which includes all the players and their qualities
    figure out who is to be accused
    you pick a random order for them to speak
    the first person to speak makes the accusation
    as each player speaks their remark is saved (just for this round)
    players can talk about each other, suspicion of anyone can change, niceness/likability? can change
    after conversation ends, the vote happens
    players vote "kill" or "don't kill" based on niceness(a lot) vs likability(a little) vs suspicion(a lot)
    their identity is revealed
    if villager, players who voted 'kill' become more suspicious, if werewolf, players who voted to 'kill' become less suspicious
    return new state without dead player
    '''
    news = copy_state(s)
    players = news['players']
    for p in players:
        if p.name == 'W' + werewolf:
            if p.quality == 'niceness':
                p.niceness = p.niceness + change
            if p.quality == 'likability':
                p.likability = p.likability + change
            if p.quality == 'suspicion':
                p.suspicion = p.suspicion + change

    print("Would you like to make a change?")
    edit_input = input() # W5 niceness .4, V8 name Steve
    
    updated_state = generate_conversation(s)
    return news

def get_kind(s, kind):
    players = s['players']
    just_kind = []
    for p in players:
        if p.kind == kind:
            just_kind.append(p)
    return just_kind

def q(s):
    # smaller numbers are better
    werewolves = get_kind(s, 'werewolf')
    werewolves_len = len(werewolves)
    total = 0
    for w in werewolves:
        total = total + w.suspicion
    average_werewolf_suspicion = total/werewolf_len
    return (werewolf_len - len(get_kind(s, 'werewolf')))*average_werewolf_suspicion

def goal_test(s):
    return len(get_kind(s, 'werewolf')) > len(get_kind(s, 'villagers'))

def goal_message(s):
    return 'The werewolves are victorious!'

class Operator:
    def __init__(self, name, precond, state_transf):
        self.name = name
        self.precond = precond
        self.state_transf = state_transf

    def is_applicable(self, s):
        return self.precond(s)

    def apply(self, s):
        return self.state_transf(s)
#</COMMON_CODE>

#<INITIAL_STATE>
PLAYERS = []
from random import randrange
print('How many werewolves?')
w_input = int(input())
print('How many villagers?')
v_input = int(input())
for w in range(w_input):
    a = random.random()
    b = random.random()
    c = random.random()
    PLAYERS.append(Player('W' + str(w), 'werewolf', a, b, c))
for v in range(v_input):
    a = random.random()
    b = random.random()
    c = random.random()
    PLAYERS.append(Player('V' + str(v), 'villager', a, b, c))
INITIAL_STATE = {'players' : PLAYERS, 'round': 1}
CREATE_INITIAL_STATE = lambda: INITIAL_STATE
#</INITIAL_STATE>

#<OPERATORS>
# for each werewolf
# .1, .2, .5
# can add or subtract
COMBOS = []
werewolves = range(w_input)
qualities = ['niceness', 'likability']
changes = [0.0, 0.1, -0.1, 0.5, -0.5]
for p in itertools.product(werewolves, qualities, changes):
    COMBOS.append(p)
print(COMBOS)
    
OPERATORS = [Operator('Werewolf: '+ str(a) +' Quality: '+ str(b) +' Change: ' + str(c),
                      lambda s,a=a,b=b,c=c: can_move(s,a,b,c),
                      # The default value construct is needed
                      # here to capture the values of p&q separately
                      # in each iteration of the list comp. iteration.
                      lambda s,a=a,b=b,c=c: move(s,a,b,c))
             for (a,b,c) in COMBOS]
#</OPERATORS>

#<GOAL_TEST> (optional)
GOAL_TEST = lambda s: goal_test(s)
#</GOAL_TEST>

#<GOAL_MESSAGE_FUNCTION> (optional)
GOAL_MESSAGE_FUNCTION = lambda s: goal_message(s)
#</GOAL_MESSAGE_FUNCTION>
