# CHALLENGE: Complexity of Parsing
#
# Because every HTML webpage and bit of embedded JavaScript must be parsed
# before it can be rendered, the efficiency of parsing is of critical
# importance.
#
# In the past, computer scientists and linguists developed special
# restricted classes of grammars that could be parsed rapidly. The
# memoization approach to parsing that we used in this class is named
# Earley's Algorithm after its inventor. It can handle any context-free
# grammar, but it is not always very efficient. In fact, if the size of the
# webpage is X tokens, it can sometimes take as many as X*X*X (i.e., X
# cubed) operations to determine if the string is in the language of the
# grammar or not. That would be really bad, because it means that if the
# size of your webpage doubles, it would take 8 times longer to load!
# That's not how you build a scalable business.
#
# (Later courses on computer science theory and the analysis and complexity
# of algorithms will provide you with the tools to determine why it could
# perform X*X*X but not X*X*X*X operations in the worst case. For now,
# simply assume it is true.)
#
# Since the exact time it takes to execute a program depends on your
# particular hardware, we will measure operations. In particular, every
# time our parser has to look over our grammar rules to compute the
# closure, if there are X grammar rules we charge it for X units of work.
# Similarly, whenever our parser has to look back at chart[j] to to
# reductions, if there are Y states in chart[j] we charge it for Y units of
# work.
#
# For this problem you should define a grammar and a list of tokens
# so that parsing the tokens requires at least 2*X*X*X "work operations"
# (as defined above), where X is the number of input tokens, the number
# of grammar rules, or the size of the largest grammar rule. In addition,
# you must find a answer where X > 10 (we want to see real poor
# performance, not a small corner case on tiny input) and also where X < 50
# (to avoid overloading our grading servers).
#
# Hint 1: You can make parsing take more time by increasing the size of the
# input string, but since that also increases X, you can't solve this
# problem with that alone. We're interested in seeing worst-case
# performance in proportion to the size of the input.
#
# Hint 2: This problem is intentionally open-ended. Computer science
# involves creativity. Make up some grammars and try them out.
#
# Hint 3: It doesn't even matter if your token string is in the language of
# the grammar or not. But if it's not, our parser often finds that out
# very early, so that probably won't be the example of poor performance
# you're looking for.
#
# Hint 4: Think about the concept from class that gave us the most
# difficulty when parsing and interpreting natural languages and computer
# languages alike. If you can think of such a thing, try to put a lot of it
# in your counter-example!

# Aside from "work_count", this is just a reprint of the parsing algorithm
# from class. You can't change the parsing algorithm for this problem, so
# just skip down to the end.

work_count = 0      # track one notion of "time taken"

def addtoset(theset,index,elt):
  if not (elt in theset[index]):
    theset[index] = [elt] + theset[index]
    return True
  return False

def parse(tokens,grammar):
  global work_count
  work_count = 0
  tokens = tokens + [ "end_of_input_marker" ]
  chart = {}
  start_rule = grammar[0]
  for i in range(len(tokens)+1):
    chart[i] = [ ]
  start_state = (start_rule[0], [], start_rule[1], 0)
  chart[0] = [ start_state ]
  for i in range(len(tokens)):
    while True:
      changes = False
      for state in chart[i]:
        # State ===   x -> a b . c d , j
        x = state[0]
        ab = state[1]
        cd = state[2]
        j = state[3]

        # Current State ==   x -> a b . c d , j
        # Option 1: For each grammar rule c -> p q r
        # (where the c's match)
        # make a next state               c -> . p q r , i
        # English: We're about to start parsing a "c", but
        #  "c" may be something like "exp" with its own
        #  production rules. We'll bring those production rules in.
        next_states = [ (rule[0],[],rule[1],i)
          for rule in grammar if cd <> [] and cd[0] == rule[0] ]
        work_count = work_count + len(grammar)
        for next_state in next_states:
          changes = addtoset(chart,i,next_state) or changes

        # Current State ==   x -> a b . c d , j
        # Option 2: If tokens[i] == c,
        # make a next state               x -> a b c . d , j
        # in chart[i+1]
        # English: We're looking for to parse token c next
        #  and the current token is exactly c! Aren't we lucky!
        #  So we can parse over it and move to j+1.
        if cd <> [] and tokens[i] == cd[0]:
          next_state = (x, ab + [cd[0]], cd[1:], j)
          changes = addtoset(chart,i+1,next_state) or changes

        # Current State ==   x -> a b . c d , j
        # Option 3: If cd is [], the state is just x -> a b . , j
        # for each p -> q . x r , l in chart[j]
        # make a new state                p -> q x . r , l
        # in chart[i]
        # English: We just finished parsing an "x" with this token,
        #  but that may have been a sub-step (like matching "exp -> 2"
        #  in "2+3"). We should update the higher-level rules as well.
        next_states = [ (jstate[0], jstate[1] + [x], (jstate[2])[1:],
                         jstate[3] )
          for jstate in chart[j]
          if cd == [] and jstate[2] <> [] and (jstate[2])[0] == x ]
        work_count = work_count + len(chart[j])
        for next_state in next_states:
          changes = addtoset(chart,i,next_state) or changes

      # We're done if nothing changed!
      if not changes:
        break

# Comment this block back in if you'd like to see the chart printed.
#
  for i in range(len(tokens)):
    print "== chart " + str(i)
    for state in chart[i]:
      x, ab, cd, j = state
      print "    " + x + " ->",
      for sym in ab:
        print " " + sym,
      print " .",
      for sym in cd:
        print " " + sym,
      print "  from " + str(j)

  accepting_state = (start_rule[0], start_rule[1], [], 0)
  return accepting_state in chart[len(tokens)-1]

#####################################################################
# We've rigged up a simple testing framework for you.

def test_it(grammar, tokens):
        X = max( len(grammar) , len(tokens), \
                max([len(rule[1]) for rule in grammar]))
        result = parse(tokens,grammar)
        print "X =", X, " work =", work_count, " 2*X^3 =", 2*X*X*X
        if work_count > 2 * X * X * X and X > 10 and X < 50:
                print "Success! Copy these down and submit them."
                print "grammar = ", grammar
                print "tokens = ", tokens


# You should start changing code around here.

#grammar = [
#  ("S", ["P" ]) ,
#  ("P", ["(" , "P", ")" ]),
#  ("P", [ ]) ,
#]
#
#for i in [5,10,15,20,25]:
#        # Make i nested balanced parentheses.
#        tokens = [ "(" for j in range(i) ] + [ ")" for j in range(i) ]
#        test_it(grammar,tokens)

# If you run this and look closely, you'll see that as X doubles
# from 5 to 10, the work_count roughly doubles as well, and so on.
# So the work done when we parse strings in this balanced
# parentheses grammar behaves like X^1, not X^3. So this isn't the
# answer. Use your creativity to find something that is.

# !!AI Wikipedia says Earley is O(n^3) for ambiguous input. But what
# does that mean, and why is this so?
#
# Hand-waving: ambiguity relates to more than one parse tree for
# a given CFG and input. We already know that binary arithmetic operators
# without precedence are ambiguous.
#
# But really, what happens with our Early parser, which is memoized,
# during ambiguity? The chart variable explodes. It's tracking every possible
# binding of all operators!

grammar = [
    ("A", ["A", "+", "A"]),
    ("A", ["A", "-", "A"]),
    ("A", ["A", "*", "A"]),
    ("A", ["A", "/", "A"]),
    ("A", ["A", "<", "A"]),
    ("A", ["A", ">", "A"]),
    ("A", ["1"]),
    ("A", ["2"]),
    ("A", ["3"]),
    ("A", ["4"]),
    ("A", ["5"]),
    ("A", ["6"]),
    ("A", ["7"]),
    ("A", ["8"]),
    ("A", ["9"]),
    ("A", ["0"]),
]

import random
operators = ["+", "-", "*", "/", "<", ">"]
for i in [2]:
    tokens = []
    for j in xrange(i):
        tokens.append(str(random.randrange(0, 10)))
        tokens.append(random.choice(operators))
    tokens.append(str(random.randrange(0, 10)))
    print tokens
    test_it(grammar,tokens)

grammar = [ ] # put your final answer here
tokens = [ ] # put your final answer here

