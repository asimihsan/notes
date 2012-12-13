# Reading Machine Minds 2
#
# We say that a finite state machine is "empty" if it accepts no strings.
# Similarly, we say that a context-free grammar is "empty" if it accepts no
# strings. In this problem, you will write a Python procedure to determine
# if a context-free grammar is empty.
#
# A context-free grammar is "empty" starting from a non-terminal symbol S
# if there is no _finite_ sequence of rewrites starting from S that
# yield a sequence of terminals.
#
# For example, the following grammar is empty:
#
# grammar1 = [
#       ("S", [ "P", "a" ] ),           # S -> P a
#       ("P", [ "S" ]) ,                # P -> S
#       ]
#
# Because although you can write S -> P a -> S a -> P a a -> ... that
# process never stops: there are no finite strings in the language of that
# grammar.
#
# By contrast, this grammar is not empty:
#
# grammar2 = [
#       ("S", ["P", "a" ]),             # S -> P a
#       ("S", ["Q", "b" ]),             # S -> Q b
#       ("P", ["P"]),                   # P -> P
#       ("Q", ["c", "d"]),              # Q -> c d
#
# And ["c","d","b"] is a witness that demonstrates that it accepts a
# string.
#
# Write a procedure cfgempty(grammar,symbol,visited) that takes as input a
# grammar (encoded in Python) and a start symbol (a string). If the grammar
# is empty, it must return None (not the string "None", the value None). If
# the grammar is not empty, it must return a list of terminals
# corresponding to a string in the language of the grammar. (There may be
# many such strings: you can return any one you like.)
#
# To avoid infinite loops, you should use the argument 'visited' (a list)
# to keep track of non-terminals you have already explored.
#
# Hint 1: Conceptually, in grammar2 above, starting at S is not-empty with
# witness [X,"a"] if P is non-empty with witness X and is non-empty with
# witness [Y,"b"] if Q is non-empty with witness Y.
#
# Hint 2: Recursion! A reasonable base case is that if your current
# symbol is a terminal (i.e., has no rewrite rules in the grammar), then
# it is non-empty with itself as a witness.
#
# Hint 3: all([True,False,True]) = False
#         any([True,True,False]) = True

import pprint

def get_nonterminals_and_terminals(grammar):
    allsymbols = set()
    nonterminals = set()
    for (production_lhs, production_rhs) in grammar:
        nonterminals.add(production_lhs)
        allsymbols.add(production_lhs)
        allsymbols.update(production_rhs)
    terminals = allsymbols - nonterminals
    return (nonterminals, terminals)

def cfgempty(grammar, symbol, visited, nonterminals = None, terminals = None):
    #print "cfgempty() entry. symbol: '%s', visited: '%s'" % (symbol, pprint.pformat(visited))

    # -------------------------------------------------------------------------
    #   Prepare to track nonterminals and terminals without needing to
    #   re-parse grammar repeatedly.
    # -------------------------------------------------------------------------
    if nonterminals is None or nonterminals is None:
        (nonterminals, terminals) = get_nonterminals_and_terminals(grammar)
    # -------------------------------------------------------------------------

    # -------------------------------------------------------------------------
    #   Base case - if symbol is a terminal then it is necessarily non-empty,
    #   with itself as a witness.
    # -------------------------------------------------------------------------
    if symbol in terminals:
        return [symbol]
    # -------------------------------------------------------------------------

    # -------------------------------------------------------------------------
    #   We are looking at a nonterminal. There may be one or more rewrite
    #   rules for this symbol. We are looking for any rewrite rule that
    #   results in a nonempty result.
    # -------------------------------------------------------------------------
    for (production_lhs, production_rhs) in grammar:
        if production_lhs == symbol:
            # If we've already visited this production skip it.
            if (production_lhs, production_rhs) in visited:
                #print "symbol: '%s'. already visited '%s' -> '%s'." % (symbol, production_lhs, production_rhs)
                continue

            # We're about this visit this production, so mark it so.
            visited.append((production_lhs, production_rhs))

            # If there is nothing in the RHS this is an epsilon
            # production i.e. R -> \epsilon. Hence the empty string
            # is a witness.
            if len(production_rhs) == 0:
                #print "symbol: %s -> %s goes to epsion." % (symbol, production_rhs)
                return []

            witnesses = [cfgempty(grammar,
                                  rewritten_symbol,
                                  visited,
                                  nonterminals,
                                  terminals)
                         for rewritten_symbol in production_rhs]

            # If there are no nonempty CFGs under this symbol then this
            # symbol is itself empty.
            if all(witness is None for witness in witnesses):
                #print "symbol: '%s'. no witnesses found." % symbol
                return None

            # If all rewritten symbols are terminals we have a witness.
            if all(witness is not None for witness in witnesses):
                #print "symbol: '%s'. all witnesses are terminals." % symbol
                return_value = []
                for witness in witnesses:
                    return_value.extend(witness)
                return return_value
    # -------------------------------------------------------------------------

    # At this point we couldn't find any witness strings, so this symbol
    # is empty.
    #print "symbol: '%s'. searched all rewritten symbols, couldn't find a witness." % symbol
    return None

# We have provided a few test cases for you. You will likely want to add
# more of your own.

grammar1 = [
      ("S", [ "P", "a" ] ),
      ("P", [ "S" ]) ,
      ]

print "1"
print cfgempty(grammar1,"S",[]) == None

grammar2 = [
      ("S", ["P", "a" ]),
      ("S", ["Q", "b" ]),
      ("P", ["P"]),
      ("Q", ["c", "d"]),
      ]

print "2"
print cfgempty(grammar2,"S",[]) == ['c', 'd', 'b']

grammar3 = [  # some Spanish provinces
        ("S", [ "Barcelona", "P", "Huelva"]),
        ("S", [ "Q" ]),
        ("Q", [ "S" ]),
        ("P", [ "Las Palmas", "R", "Madrid"]),
        ("P", [ "T" ]),
        ("T", [ "T", "Toledo" ]),
        ("R", [ ]) ,
        ("R", [ "R"]),
        ]

print "3"
print cfgempty(grammar3,"S",[]) == ['Barcelona', 'Las Palmas', 'Madrid', 'Huelva']

