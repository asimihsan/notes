# Market Exchange
#
# Focus: Units 5 and 6, Interpreting and Environments
#
#
# In this problem you will use your knowledge of interpretation and
# environments to simulate a simple market. Here the "program" is not a
# list of JavaScript commands that describe webpage computation, but
# instead a list of economic commands that describe business transactions.
#
# Our parse tree (or abstract syntax tree) is a list of elements. Elements
# have three forms: has, buy and sell. "has" elements indicate that the
# given person begins with the given amount of money:
#
#       [ "klaus teuber", "has", 100 ]
#
# "buy" elements indicate that the given person wants to purchase some
# item for the listed amount of money. For example:
#
#       [ "klaus teuber", "buy", "sheep", 50 ]
#
# ... means that "klaus teuber" is interesting in buying the item
# "sheep" for 50 monetary units. For this assignment, that transaction will
# only happen if there is a seller also selling "sheep" for 50 (and if
# klaus actually has 50 or more monetary units). That is, both the item and
# the price must match exactly. The final type of element is "sell":
#
#       [ "andreas seyfarth", "sell", "sheep" , 50 ]
#
# This indicates that "andreas seyfarth" is willing to sell the item
# "sheep" for 50 monetary units. (Again, that transaction will only take
# place if there is a buyer wishing to purchase that item for exactly the
# same amount of money -- and if the buyer actually has at least that much
# money!)
#
# All of the "has" commands will come first in the program.
#
# "buy" and "sell" elements only operate once per time they are listed. In
# this example:
#
#       [ "klaus teuber", "has", 100 ]
#       [ "andreas seyfarth", "has", 50 ]
#       [ "klaus teuber", "buy", "sheep", 50 ]
#       [ "andreas seyfarth", "sell", "sheep" , 50 ]
#
# klaus will buy "sheep" from andreas once, at which poin klaus will have
# 50 money and andreas will have 100. However, in this example:
#
#       [ "klaus teuber", "has", 100 ]
#       [ "andreas seyfarth", "has", 50 ]
#       [ "klaus teuber", "buy", "sheep", 50 ]
#       [ "klaus teuber", "buy", "sheep", 50 ]          # listed twice
#       [ "andreas seyfarth", "sell", "sheep" , 50 ]
#       [ "andreas seyfarth", "sell", "sheep" , 50 ]    # listed twice
#
# klaus will buy "sheep" from andreas and then buy "sheep" from andreas
# again, at which point klaus will have 0 money and andreas will have 150.
#
# Write a procedure evaluate() that takes a list of elements as an input.
# It should perform all possible transactions, in any order, until no more
# transactions are possible (e.g., because all "buy" and "sell" elements
# have been used and/or potential buyers do not have enough money left for
# their desired "buy"s). Your procedure should return an environment
# (a Python dictionary) mapping names to final money amounts (after all
# transactions have happened).
#
# Hint: To avoid processing a "buy" or "sell" twice, you might either call
# yourself recursively with a smaller AST (i.e., with those two elements
# removed) or you can use Python's list.remove() to remove elements "in
# place". Example:
#
# lst = [("a",1) , ("b",2) ]
# print lst
# [('a', 1), ('b', 2)]
#
# lst.remove( ("a",1) )
# print lst
# [('b', 2)]

import pprint
import itertools

def resolve_transactions(transactions, environment):
    #print "resolve_transactions entry. transactions: %s, environment: %s" % (pprint.pformat(transactions), pprint.pformat(environment))

    old_transactions = transactions[:]
    if len(transactions) == 0:
        return (transactions, environment)
    pairs = itertools.combinations(transactions, 2)
    def predicate(pair):
        ((name1, action1, entity1, amount1),
         (name2, action2, entity2, amount2)) = pair
        if ((action1 == "buy" and action2 == "sell") or
            (action1 == "sell" and action2 == "buy")) and \
           (entity1 == entity2) and \
           (amount1 == amount2):
               return True
        return False
    valid_trades = itertools.ifilter(predicate, pairs)
    for (elem1, elem2) in valid_trades:
        trade_worked = False

        (name1, action1, entity1, amount1) = elem1
        (name2, action2, entity2, amount2) = elem2
        if action1 == "buy" and action2 == "sell":
            if environment[name1] >= amount1:
                environment[name1] -= amount1
                environment[name2] += amount2
                trade_worked = True
        else:
            if environment[name2] >= amount2:
                environment[name1] += amount1
                environment[name2] -= amount2
                trade_worked = True
        if trade_worked:
            transactions.remove(elem1)
            transactions.remove(elem2)


    if len(old_transactions) == len(transactions):
        # Despite going through all trades we've failed to
        # identify any good ones, so bail out.
        return (transactions, environment)

    return resolve_transactions(transactions, environment)

def evaluate(ast, environment=None, transactions=None):
    #print "evalute entry. ast: %s, environment: %s, transactions: %s" % (pprint.pformat(ast), pprint.pformat(environment), pprint.pformat(transactions))

    # Base case for recursive calls
    if len(ast) == 0:
        #print "returning: %s" % pprint.pformat(environment)
        (transactions, environment) = resolve_transactions(transactions, environment)
        return environment

    # Tracking outstanding transactions
    if transactions is None:
        transactions = []

    # Tracking the environment
    if environment is None:
        environment = {}

    (elem, ast_remaining) = ast[0], ast[1:]
    assert(elem[1] in ["has", "buy", "sell"])
    if elem[1] == "has":
        (name, action, amount) = elem
    else:
        (name, action, entity, amount) = elem
    if action == "has":
        environment[name] = amount
    else:
        transactions.append((name, action, entity, amount))

    # Recurse.
    return evaluate(ast_remaining, environment, transactions)

# In test1, exactly one sell happens. Even though klaus still has 25 money
# left over, a "buy"/"sell" only happens once per time it is listed.
test1 = [ ["klaus","has",50] ,
          ["wrede","has",80] ,
          ["klaus","buy","sheep", 25] ,
          ["wrede","sell","sheep", 25] , ]

print "test 1"
print evaluate(test1) == {'klaus': 25, 'wrede': 105}

# In test2, klaus does not have enough money, so no transactions take place.
test2 = [ ["klaus","has",5] ,
          ["wrede","has",80] ,
          ["klaus","buy","sheep", 25] ,
          ["wrede","sell","sheep", 25] , ]

print "test 2"
print evaluate(test2) == {'klaus': 5, 'wrede': 80}

# Wishful thinking, klaus! Although you want to buy sheep for 5 money and
# you even have 5 money, no one is selling sheep for 5 money. So no
# transactions happen.
test2b = [ ["klaus","has",5] ,
           ["wrede","has",80] ,
           ["klaus","buy","sheep", 5] ,
           ["wrede","sell","sheep", 25] , ]

print "test 2b"
print evaluate(test2b) == {'klaus': 5, 'wrede': 80}

# In test3, wrede does not have the 75 required to buy the wheat from
# andreas until after wrede sells the sheep to klaus.
test3 = [ ["klaus","has",50] ,
          ["wrede","has",50] ,
          ["andreas","has",50] ,
          ["wrede","buy","wheat", 75] ,
          ["andreas","sell","wheat", 75] ,
          ["klaus","buy","sheep", 25] ,
          ["wrede","sell","sheep", 25] ,
          ]

print "test 3"
print evaluate(test3) == {'andreas': 125, 'klaus': 25, 'wrede': 0}

