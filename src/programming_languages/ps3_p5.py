# Detecting Ambiguity
#
# A grammar is ambiguous if there exists a string in the language of that
# grammar that has two (or more) parse trees. Equivalently, a grammar is
# ambiguous if there are two (or more) different sequences of rewrite rules
# that arrive at the same final string.
#
# Ambiguity is a critical concept in natural languages and in programming
# languages. If we are not careful, our formal grammars for languages like
# JavaScript will have ambiguity.
#
# In this problem you will write a procedure isambig(grammar,start,tokens)
# that takes as input a grammar with a finite number of possible
# derivations and a string and returns True (the value True, not the string
# "True") if those tokens demonstrate that the grammar is ambiguous
# starting from that start symbol (i.e., because two different sequences of
# rewrite rules can arrive at those tokens).
#
# For example:
#
# grammar1 = [                  # Rule Number
#       ("S", [ "P", ] ),       # 0
#       ("S", [ "a", "Q", ]) ,  # 1
#       ("P", [ "a", "T"]),     # 2
#       ("P", [ "c" ]),         # 3
#       ("Q", [ "b" ]),         # 4
#       ("T", [ "b" ]),         # 5
#       ]
#
# In this grammar, the tokens ["a", "b"] do demonstrate that the
# grammar is ambiguous because there are two difference sequences of
# rewrite rules to obtain them:
#
#       S  --0->  P  --2->  a T  --5->  a b
#
#       S  --1->  a Q  --4->  a b
#
# (I have written the number of the rule used inside the arrow for
# clarity.) The two sequences are [0,2,5] and [1,4].
#
# However, the tokens ["c"] do _not_ demonstrate that the grammar is
# ambiguous, because there is only one derivation for it:
#
#       S  --0->  P  --3->  c
#
# So even though the grammar is ambiguous, the tokens ["c"] do not
# demonstrate that: there is only one sequence [0,3].
#
# Important Assumption: In this problem the grammar given to you will
# always have a finite number of possible derivations. So only a
# finite set of strings will be in the language of the grammar. (You could
# test this with something like cfginfinite, so we'll just assume it.)
#
# Hint 1: Consider something like "expand" from the end of the Unit, but
# instead of just enumerating utterances, enumerate (utterance,derivation)
# pairs. For a derivation, you might use a list of the rule indexes as we
# did in the example above.
#
# Hint 2: Because the grammar has only a finite number of derivations, you
# can just keep enumerating new (utterance,derivation) pairs until you
# cannot find any that are not already enumerated.

import pprint
import itertools
import types

def flatten_list(input_list):
    output_list = []
    for elem in input_list:
        if type(elem) == types.ListType:
            output_list.extend(elem)
        elif type(elem) == types.TupleType:
            output_list.extend(list(elem))
        else:
            output_list.append(elem)
    return output_list

def get_nonterminals_and_terminals(grammar):
    allsymbols = set()
    nonterminals = set()
    for (production_lhs, production_rhs) in grammar:
        nonterminals.add(production_lhs)
        allsymbols.add(production_lhs)
        allsymbols.update(production_rhs)
    terminals = allsymbols - nonterminals
    return (nonterminals, terminals)

def isambig(grammar, start, utterance):
    all_strings = [string for string in enumerate_all_strings(grammar, start)]
    #print "all_strings:"
    #for string in all_strings:
    #    print string
    return all_strings.count(utterance) > 1

# -----------------------------------------------------------------------------
#   Note that we know that all input CFGs are finite, so we don't need to
#   prevent infinite loops.
# -----------------------------------------------------------------------------
def enumerate_all_strings(grammar, start, nonterminals = None, terminals = None):
    #print "enumerate_all_strings() entry. start: '%s'" % (start, )
    if nonterminals is None or terminals is None:
        (nonterminals, terminals) = get_nonterminals_and_terminals(grammar)
    matching_rules = [rule for rule in grammar if rule[0] == start]
    for (_, rule) in matching_rules:
        #print "start: '%s'. rule: '%s'" % (start, rule)
        if all(elem in terminals for elem in rule):
            #print "start: '%s', all elems are terminals." % (start, )
            yield rule
        else:
            all_strings = []
            for i, symbol in enumerate(rule):
                if symbol in nonterminals:
                    strings = enumerate_all_strings(grammar,
                                                    symbol,
                                                    nonterminals,
                                                    terminals)
                    strings_expanded = [string for string in strings]
                    #print "start: '%s', i: '%s', symbol: '%s', strings: '%s'" % (start, i, symbol, strings_expanded)
                    all_strings.append([(i, elem) for elem in strings_expanded])
            strings_product = [elem for elem in itertools.product(*all_strings)]
            for combination in strings_product:
                #print "start: '%s', combination: '%s'" % (start, combination)
                rule_copy = rule[:]
                for (index, element) in combination:
                    rule_copy[index] = element
                #print "rule_copy before: '%s'" % (rule_copy, )
                rule_copy = flatten_list(rule_copy)
                #print "rule_copy: '%s'" % (rule_copy, )
                yield rule_copy

# We have provided a few test cases. You will likely want to add your own.

grammar1 = [
       ("S", [ "P", ]),
       ("S", [ "a", "Q", ]) ,
       ("P", [ "a", "T"]),
       ("P", [ "c" ]),
       ("Q", [ "b" ]),
       ("T", [ "b" ]),
       ]
print '-' * 20 + ' 1 ' + '-' * 20
print isambig(grammar1, "S", ["a", "b"]) == True
print isambig(grammar1, "S", ["c"]) == False

grammar2 = [
       ("A", [ "B", ]),
       ("B", [ "C", ]),
       ("C", [ "D", ]),
       ("D", [ "E", ]),
       ("E", [ "F", ]),
       ("E", [ "G", ]),
       ("E", [ "x", "H", ]),
       ("F", [ "x", "H"]),
       ("G", [ "x", "H"]),
       ("H", [ "y", ]),
       ]
print '-' * 20 + ' 2 ' + '-' * 20
print isambig(grammar2, "A", ["x", "y"]) == True
print isambig(grammar2, "E", ["y"]) == False

grammar3 = [ # Rivers in Kenya
       ("A", [ "B", "C"]),
       ("A", [ "D", ]),
       ("B", [ "Dawa", ]),
       ("C", [ "Gucha", ]),
       ("D", [ "B", "Gucha"]),
       ("A", [ "E", "Mbagathi"]),
       ("A", [ "F", "Nairobi"]),
       ("E", [ "Tsavo" ]),
       ("F", [ "Dawa", "Gucha" ])
       ]
print '-' * 20 + ' 3 ' + '-' * 20
print isambig(grammar3, "A", ["Dawa", "Gucha"]) == True
print isambig(grammar3, "A", ["Dawa", "Gucha", "Nairobi"]) == False
print isambig(grammar3, "A", ["Tsavo"]) == False

grammar4 = [
        ("A", ["B", "C"]),
        ("B", ["bravo"]),
        ("B", ["bravo"]),
        ("C", ["charlie"]),
        ("C", ["charlie"]),
        ]
print "-" * 20 + ' 4 ' + '-' * 20
#print isambig(grammar4, "A", ["bravo", "charlie", "delta"]) == False

