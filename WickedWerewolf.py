'''
Wicked Werewolf
Frances Davies & Yuefeng Li
5/31/16
'''

import random
import itertools
import copy

ALL_COMMENTS = {} # "name --> comment"

# To be replenished
POSITIVE_ADJ = ["nice", "reliable", "trustworthy", "not"]
NEGATIVE_ADJ = ["dishonest", "mean", "reckless"]
NEGATIVE_VERBS = ["lying", "bluffing", "not-telling-the-truth"]
POSITIVE_VERBS = ["telling-the-truth", "speaking-from-his/her-heart"]

GENERIC_VERBS = ['go', 'be', 'try', 'eat', 'take', 'help',
         'make', 'get', 'jump', 'write', 'type', 'fill',
         'put', 'turn', 'compute', 'think', 'drink',
         'blink', 'crash', 'crunch', 'add', 'dance', 'kill',
         'read', 'hear', 'heard', 'tell', 'talk']

NOUNS = ['food', 'grass', 'marbles', 'my-professor']


OPENING_SUPER_NICE = ["I hope everyone is going to have a good time!", "Werewolves is a fun game! Forget all your unhappiness!"]
OPENING_NICE = ["Let's play!", "Look! It's a psychological game! Yay!", "I'll drink and play"]
OPENING_NONCHALANT = ["It's a game. Okay. I get it.", "Let's get this over with so I can go home and watch FamilyGuys.", "I play to win!"]
GREETINGS = ['greetings', 'hello', 'hey','hi','what\'s up', 'wassup', 'bonjour', 'yo', 'good day']

class Player:
    # A map of comments made by other players about current player.
        
    def __init__(s, name, kind, niceness, likability, suspicion):
        # constants
        s.COMMENTS_ABOUT_ME = {} # "name --> comment"
        s.name = name # p1, p2, p3...
        s.kind = kind # werewolf, villager
        s.niceness = niceness # 0-1
        s.likability = likability # 0-1
        s.suspicion = suspicion # 0-1
        
        global POSITIVE_ADJ
        global NEGATIVE_ADJ
        global NEGATATIVE_VERBS
        global POSITIVE_VERBS
        global GENERIC_VERBS
        global NOUNS
        global OPENING_SUPER_NICE
        global OPENING_NICE
        global OPENING_NONCHALANT
        global GREETINGS
        
        if s.niceness > 0.5 and s.likability > 0.5:
            print(GREETINGS[random.randrange(0, len(GREETINGS))].capitalize() + "! " + OPENING_SUPER_NICE[random.randrange(0, len(OPENING_SUPER_NICE))])
        if s.niceness > 0.5 or s.likability > 0.5:
            print(GREETINGS[random.randrange(0, len(GREETINGS))].capitalize() + "! " + OPENING_NICE[random.randrange(0, len(OPENING_NICE))])
        else:
            print(GREETINGS[random.randrange(0, len(GREETINGS))].capitalize() + "! " + OPENING_NONCHALANT[random.randrange(0, len(OPENING_NONCHALANT))])
        
    def make_accusation(self, s):
        option = get_top_3(s, 'suspicion')
        return option[0]

    def vote(self, s, accusation):
        return random.randrange(0,1)

    def comment_is_about_me(self, comment):
        "Add comments about current player to COMMENTS_ABOUT_ME."
        words = comment.split(' ')
        for word in words:
            if word == self.name:
                return True
        return False

    def remember_conversations(self): 
        
        for name in ALL_COMMENTS.keys():
            val = ALL_COMMENTS[name]
            if self.comment_is_about_me(val):
                self.COMMENTS_ABOUT_ME[name] = ALL_COMMENTS[name]

    def make_comment(self, s):
        comment = ''
        
        # Randomly chooses between making comments about other players
        # vs. comments that are not player-specific

        # 0 is generic comments and 1 is player.specific
        specific_or_not = random.randrange(0, 2)

        # First, randomly chooses a quality to choose the top 3 players from.
        
        # Second, chooses a random player out of the 3 top players based on a random quality generated
        # in first step.
        
        # Third, make comment about that player.
        # If niceness is chosen and niceness is > 0.5, then make positive comments about that player, negative otherwise.
        # If likability is chosen and is > 0.5, make positive comments. Negative otherwise.
        # If suspicion is chosen and is > 0.5, negative comments are made. Positive otherwise.

        # Comments are in the following format: I think he/she is + verb or adj, positive/negative based on quality.

        int_to_quality = {0 : "niceness", 1 : "likability", 2 : "suspicion"}   # For randomly choose a quality.
        quality = int_to_quality[random.randrange(0, 3)]    # Randomly chooses a quality to get the top 3 players with that quality.
        comment = ""

        if specific_or_not == 1:
            if quality == "niceness":    # If making comments based on niceness
                pos_or_neg = random.randrange(0, 2)
                verb = None
                names = get_top_3(s, "niceness")
                comment = "I think " + names[random.randrange(0, len(names))] + " is " + POSITIVE_VERBS[random.randrange(0, len(POSITIVE_VERBS))] + "!"
            if quality == "likability":
                names = get_top_3(s, "likability")
                comment = "I think " + names[random.randrange(0, len(names))] + " is " + POSITIVE_VERBS[random.randrange(0, len(POSITIVE_VERBS))] + "!"
            if quality == "suspicion":
                names = get_top_3(s, "suspicion")
                comment = "I think " + names[random.randrange(0, len(names))] + " is " + NEGATIVE_VERBS[random.randrange(0, len(NEGATIVE_VERBS))] + "!"
        elif specific_or_not == 0:
            comment = "I " + GENERIC_VERBS[random.randrange(0, len(GENERIC_VERBS))] + " " + NOUNS[random.randrange(0, len(NOUNS))] + "."
        ALL_COMMENTS[self.name] = comment
        if comment != '':
            print(comment)
        
    def respond(self):
        #print(self.COMMENTS_ABOUT_ME)
        #print(ALL_COMMENTS)
        if len(self.COMMENTS_ABOUT_ME) != 0:
            names = self.COMMENTS_ABOUT_ME.keys()
            name = names[random.randrange(0, len(names))]
            comment = self.COMMENTS_ABOUT_ME[name]
            words = comment.split(' ')
            words = words[4]           
            response = "Why do you think that I'm " + word + "?!"
            print(response)
            
            
        # If there are comments about current player, respond to one of those comments
        # chosen at random. Otherwise randomly respond to a comment. 
        # Most of the pattern-matching happens here.

    # need a make_accusation function??? (takes s, returns random player from 3 with highest suspicion)
    # need a vote function??? (takes accusation, returns 0 or 1)
    # need get_top_3???

                

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
def DESCRIBE_STATE(s):
    # Produces a textual description of a state.
    # Might not be needed in normal operation with GUIs.
    result = "ROUND: " + str(s['round']) + " PLAYERS: "
    players = s['players']
    for p in players:
        result = result + p.name + " "
    return result

def HASHCODE(s):
    return str(s)

def copy_state(s):
    return copy.deepcopy(s)

def generate_conversation(s):
    players = s['players']
    random.shuffle(players)
    p0 = players[0]
    accusation = p0.make_accusation(s)
    for p in players:
        p.make_comment(s)
    for p in players:
        p.remember_conversations()
    for p in players:
        p.respond()
    result = 0
    for p in players:
        result = result + p.vote(s, accusation)
    if result > len(players)/2:
        for p in players:
            if p.name == accusation:
                players.remove(p)
                break
    news = copy_state(s)
    news['players'] = players
    return news

def can_move(s, werewolf, quality, change):
    players = s['players']
    for p in players:
        if p.name == 'W' + str(werewolf):
            value = 0
            if quality == 'niceness':
                value = p.niceness + change
            if quality == 'likability':
                value = p.likability + change
            if quality == 'suspicion':
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
    ALL_COMMENTS.clear()
    
    news = copy_state(s)
    players = news['players']
    for p in players:
        if p.name == 'W' + str(werewolf):
            if quality == 'niceness':
                p.niceness = p.niceness + change
            if quality == 'likability':
                p.likability = p.likability + change
            if quality == 'suspicion':
                p.suspicion = p.suspicion + change

    print("Would you like to make a change? Type 'name quality value' or 'no'.")
    edit_input = input() # W5 niceness .4, V8 name Steve
    if edit_input != 'no':
        values = edit_input.split()
        name = values[0]
        quality = values[1]
        x = float(values[2])
        for p in players:
            if p.name == name:
                if quality == 'niceness':
                    p.niceness = x
                if quality == 'likability':
                    p.likability = x
                if quality == 'suspicion':
                    p.suspicion = x
        
    # Loop over all players and:
    # 1. Make opening comments
    # 2. First player to make accusation
    # 3. Rest of players to make comments
    # 4. Players mentioned have an opportunity to respond to comments about them.
    
    updated_state = generate_conversation(s)
    updated_state['round'] = updated_state['round'] + 1
    return updated_state

def get_kind(s, kind):
    players = s['players']
    just_kind = []
    for p in players:
        if p.kind == kind:
            just_kind.append(p)
    return just_kind

def get_player_character(s):
    players = s['players']
    character = {}
    for p in players:
        character[p.name] = [p.niceness, p.likability, p.suspicion]
    return character
                                           
def get_top_3(s, kind):
    'Returns the top three players ranked in the given quality.'
    quality_to_int = {"niceness": 0, "likability": 1, "suspicion": 2}
    character = get_player_character(s)
    candidates = sorted(character.keys(), key = lambda k: -character[k][quality_to_int[kind]])    # Sort names according to suspicion, descending (hence the negative).
    candidates = candidates[0:3]
    return candidates[random.randrange(0, len(candidates))]

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
    # add logic for failed if wolves == 0...?
    return len(get_kind(s, 'werewolf')) > len(get_kind(s, 'villager'))

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
