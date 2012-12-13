# Infinite Mind Reading
#
# Just as a context-free grammar may be 'empty', it may also have an
# infinite language. We say that the language for a grammar is infinite if
# the grammar accepts an infinite number of different strings (each of
# which is of finite length). Most interesting (and creative!) languages
# are infinite.
#
# For example, the language of this grammar is infinite:
#
# grammar1 = [
#       ("S", [ "S", "a" ] ),        # S -> S a
#       ("S", [ "b", ]) ,            # S -> b
#       ]
#
# Because it accepts the strings b, ba, baa, baaa, baaaa, etc.
#
# However, this similar grammar does _not_ have an infinite language:
#
# grammar2 = [
#       ("S", [ "S", ]),             # S -> S
#       ("S", [ "b", ]) ,            # S -> b
#       ]
#
# Because it only accepts one string: b.
#
# For this problem you will write a procedure cfginfinite(grammar)
# that returns True (the value True, not the string "True") if the grammar
# accepts an infinite number of strings (starting from any symbol). Your
# procedure should return False otherwise.
#
# Consider this example:
#
# grammar3 = [
#       ("S", [ "Q", ] ),        # S -> Q
#       ("Q", [ "b", ]) ,        # Q -> b
#       ("Q", [ "R", "a" ]),     # Q -> R a
#       ("R", [ "Q"]),           # R -> Q
#       ]
#
# The language of this grammar is infinite (b, ba, baa, etc.) because it is
# possible to "loop" or "travel" from Q back to Q, picking up an "a" each
# time. Since we can travel around the loop as often as we like, we can
# generate infinite strings. By contrast, in grammar2 it is possible to
# travel from S to S, but we do not pick up any symbols by doing so.
#
# Important Assumption: For this problem, you may assume that for every
# non-terminal in the grammar, that non-terminal derives at least one
# non-empty finite string.  (You could just call cfgempty() from before to
# determine this, so we'll assume it.)
#
# Hint 1: Determine if "Q" can be re-written to "x Q y", where either x
# or y is non-empty.
#
# Hint 2: The "Important Assumption" above is more important than it looks:
# it means that any rewrite rule "bigger" than ("P", ["Q"]) adds at least
# one token.
#
# Hint 3: While cfginfinite(grammar) is not recursive, you may want to
# write a helper procedure (that determines if Q can be re-written to "x Q
# y" with |x+y| > 0 ) that _is_ recursive. Watch out for infinite loops:
# keep track of what you have already visited.

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

def cfginfinite(grammar):
    (nonterminals, terminals) = get_nonterminals_and_terminals(grammar)
    if any(is_infinite_loop(grammar,
                            rule,
                            nonterminals,
                            terminals) == True
           for rule in grammar):
        return True
    else:
        return False

def is_infinite_loop(grammar,
                     start_rule,
                     nonterminals,
                     terminals,
                     current_rule = None,
                     visited = None):
    print "is_infinite_loop() entry. start_rule: '%s', current_rule: '%s', visited:\n'%s'" % (start_rule, current_rule, pprint.pformat(visited))

    # ------------------------------------------------------------------------
    #   Initialize variables.
    # ------------------------------------------------------------------------
    if visited is None:
        visited = []
    if current_rule is None:
        current_rule = start_rule
    # ------------------------------------------------------------------------

    # ------------------------------------------------------------------------
    #   Base-case: if the start rule's LHS symbol is in the current rule's
    #   RHS and the current rule _or_ the starting rule has any terminals
    #   we're infinite.
    # ------------------------------------------------------------------------
    if (start_rule[0] in current_rule[1]) and \
       (any(elem in terminals for elem in start_rule[1] + current_rule[1])):
           print "start_rule: '%s'. base-case infinite loop found." % (start_rule, )
           return True
    # ------------------------------------------------------------------------

    unvisited_rules = [rule for rule in grammar
                       if rule not in visited and
                          any(elem in rule[1] for elem in current_rule[1])]
    for rule in unvisited_rules:
        print "unvisited rule: '%s'" % (rule, )
        visited.append(rule)
        (rule_lhs, rule_rhs) = rule
        any_terminals = any(elem in terminals for elem in rule_rhs)
        rewrites_to_ourself = any(elem == start_rule[0] for elem in rule_rhs)

        if rewrites_to_ourself and any_terminals:
            print "start_rule: '%s'. rewrites_to_ourself and any_terminals True." % (start_rule, )
            return True

        for rhs_nonterminal in [elem for elem in rule_rhs if elem in nonterminals]:
            print "start_rule: '%s'. rhs_nonterminal: '%s'" % (start_rule, rhs_nonterminal)
            matching_rules = [rule for rule in grammar if rule[0] == rhs_nonterminal]
            any_rhs_is_infinite =  any(is_infinite_loop(grammar,
                                                        start_rule,
                                                        nonterminals,
                                                        terminals,
                                                        matching_rule,
                                                        visited)
                                       for matching_rule in matching_rules)
            print "start_rule: '%s'. returning any_rhs_is_infinite: %s" % (start_rule, any_rhs_is_infinite)
            return any_rhs_is_infinite

    print "end of function, return False."
    return False


# We have provided a few test cases. You will likely want to write your own
# as well.

grammar1 = [
      ("S", [ "S", "a" ]), # S -> S a
      ("S", [ "b", ]) , # S -> b
      ]
print '-' * 20 + ' 1 ' + '-' * 20
print cfginfinite(grammar1) == True

grammar2 = [
      ("S", [ "S", ]), # S -> S
      ("S", [ "b", ]) , # S -> b
      ]

print '-' * 20 + ' 2 ' + '-' * 20
print cfginfinite(grammar2) == False

grammar3 = [
      ("S", [ "Q", ]), # S -> Q
      ("Q", [ "b", ]) , # Q -> b
      ("Q", [ "R", "a" ]), # Q -> R a
      ("R", [ "Q"]), # R -> Q
      ]

print '-' * 20 + ' 3 ' + '-' * 20
print cfginfinite(grammar3) == True

grammar4 = [  # Nobel Peace Prizes, 1990-1993
      ("S", [ "Q", ]),
      ("Q", [ "Mikhail Gorbachev", ]) ,
      ("Q", [ "P", "Aung San Suu Kyi" ]),
      ("R", [ "Q"]),
      ("R", [ "Rigoberta Tum"]),
      ("P", [ "Mandela and de Klerk"]),
      ]

print '-' * 20 + ' 4 ' + '-' * 20
print cfginfinite(grammar4) == False

