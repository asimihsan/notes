# Do Not Repeat Repeated Work
#
# Focus: Units 5 and 6: Interpreting and Optimization
#
#
# In class we studied many approaches to optimizing away redundant
# computation. For example, "X * 0" can be replaced with "0", because we
# know in advance that the result will always be 0. However, even if we do
# not know the answer in advance, we can sometimes save work. Consider this
# program fragment:
#
#       x = a + b + c;
#       y = 2;
#       z = a + b + c;
#
# Even though we do not know what "a + b + c" will be, there is no reason
# for us to compute it twice! We can replace the program with:
#
#       x = a + b + c;
#       y = 2;
#       z = x;          # works since "x = a + b + c;" above
#                       # and neither a nor b nor c has been changed since
#
# ... and always compute the same answer. This family of optimizations is
# sometimes called "common expression elimination" -- the subexpression
# "a+b+c" was common to two places in the code, so we eliminated it in one.
#
# In this problem we will only consider a special case of this
# optimization. If we see the assignment statement:
#
#       var1 = right_hand_side ;
#
# Then all subsequent assignment statements:
#
#       var2 = right_hand_side ;
#
# can be replaced with "var2 = var1 ;" provided that the "right_hand_side"s
# match exactly and provided that none of the variables involved in
# "right_hand_Side" have changed. For example, this program cannot be
# optimized in this way:
#
#       x = a + b + c;
#       b = 2;
#       z = a + b + c;
#
# Even though the right-hand-sides are exact matches, the value of b has
# changed in the interim so, to be safe, we have to recompute "a + b + c" and
# cannot replace "z = a + b + c" with "z = x".
#
# For this problem we will use the abstract syntax tree format from our
# JavaScript interpreter. Your procedure will be given a list of statements
# and should return an optimized list of statements (using the optimization
# above). However, you will *only* be given statement of the form:
#
#       ("assign", variable_name, rhs_expression)
#
# No other types of statements (e.g., "if-then" statements) will be passed
# to your procedure. Similarly, the rhs_expression will *only* contain
# expressions of these three (nested) form:
#
#       ("binop", exp, operator, exp)
#       ("number", number)
#       ("identifier", variable_name)
#
# No other types of expressions (e.g., function calls) will appear.
#
# Write a procedure "optimize()" that takes a list of statements (again,
# only assignment statements) as input and returns a new list of optimized
# statements that compute the same value but avoid recomputing
# whole right-hand-side expressions. (If there are multiple equivalent
# optimizations, return whichever you like.)
#
# Hint: x = y + z makes anything involving y and z un-available, and
# then makes y + z available (and stored in variable x).

import pprint

def invalidate(variable_name, available):
    print "invalidate entry. variable_name: %s, available: %s" % (variable_name, pprint.pformat(available))
    new_available = available.copy()
    for exp in available:
        if exp[0] == "binop":
            (_, (_, var1), _, (_, var2)) = exp
            variables = [var1, var2]
        elif exp[0] == "identifier":
            (_, var1) = exp
            variables = [var1]
        else:
            variables = []
        if variable_name in variables:
            import ipdb; ipdb.set_trace()
            del new_available[exp]
    print "invalidate returning: %s" % pprint.pformat(new_available)
    return new_available

def update(variable_name, rhs_expression, available):
    # The RHS as a whole is now available *recursively*, i.e. if
    #
    # a = b + c
    # x = a
    #
    # Then clearly:
    # - (b+c) is available in a, (a) in x
    # - But recursively, (b+c) is available in x.
    new_available = available.copy()
    if rhs_expression not in new_available:
        new_available[rhs_expression] = []
    new_available[rhs_expression].append(("identifier", variable_name))

    reverse_lookup = {}
    for (key, values) in available.items():
        for value in values:
            if value not in reverse_lookup:
                reverse_lookup[value] = []
            reverse_lookup[value].append(key)
    if rhs_expression in reverse_lookup:
        elem = reverse_lookup[rhs_expression]
        new_available[elem].append(("identifier", variable_name))

    return new_available

def optimize(ast):
    available = {}
    new_ast = []
    for (ast_operation, variable_name, rhs_expression) in ast:
        # Invalidate the LHS variable name.
        available = invalidate(variable_name, available)

#       ("binop", exp, operator, exp)
#       ("number", number)
#       ("identifier", variable_name)
        assert(rhs_expression[0] in ["binop", "number", "identifier"])
        if rhs_expression[0] == "binop":
            # Maybe the RHS is available?
            if rhs_expression in available:
                new_rhs_expression = available[rhs_expression]
                new_ast.append((ast_operation, variable_name, new_rhs_expression))
            else:
                new_ast.append((ast_operation, variable_name, rhs_expression))

            # invalidate all variables on RHS
            #print rhs_expression
            (_, rhs_exp1, rhs_operator, rhs_exp2) = rhs_expression
            for exp in [rhs_exp1, rhs_exp2]:
                if exp[0] == "identifier":
                    available = invalidate(exp[1], available)

            # Refresh "available" recursively (see update() for more info)
            available = update(variable_name, rhs_expression, available)
        else:
            new_ast.append((ast_operation, variable_name, rhs_expression))

    return new_ast

# We have included some testing code to help you check your work. Since
# this is the final exam, you will definitely want to add your own tests.

example1 = [ \
("assign", "x", ("binop", ("identifier","a"), "+", ("identifier","b"))) ,
("assign", "y", ("number", 2)) ,
("assign", "z", ("binop", ("identifier","a"), "+", ("identifier","b"))) ,
]
answer1 = [ \
("assign", "x", ("binop", ("identifier","a"), "+", ("identifier","b"))) ,
("assign", "y", ("number", 2)) ,
("assign", "z", ("identifier", "x")) ,
]

print "test 1"
#print (optimize(example1)) == answer1

example2 = [ \
("assign", "x", ("binop", ("identifier","a"), "+", ("identifier","b"))) ,
("assign", "a", ("number", 2)) ,
("assign", "z", ("binop", ("identifier","a"), "+", ("identifier","b"))) ,
]

print "test 2"
#import pprint; pprint.pprint(optimize(example2))
#print (optimize(example2)) == example2

example3 = [ \
("assign", "x", ("binop", ("identifier","a"), "+", ("identifier","b"))) ,
("assign", "y", ("binop", ("identifier","a"), "+", ("identifier","b"))) ,
("assign", "x", ("number", 2)) ,
("assign", "z", ("binop", ("identifier","a"), "+", ("identifier","b"))) ,
]
answer3 = [ \
("assign", "x", ("binop", ("identifier","a"), "+", ("identifier","b"))) ,
("assign", "y", ("identifier", "x")) ,
("assign", "x", ("number", 2)) ,
("assign", "z", ("identifier", "y")) , # cannot be "= x"
]

print "test 3"
#print (optimize(example3)) == answer3

example4 = [ \
("assign", "x", ("binop", ("identifier","a"), "+", ("identifier","b"))) ,
("assign", "y", ("binop", ("identifier","b"), "+", ("identifier","c"))) ,
("assign", "z", ("binop", ("identifier","c"), "+", ("identifier","d"))) ,
("assign", "b", ("binop", ("identifier","c"), "+", ("identifier","d"))) ,
("assign", "z", ("number", 5)) ,
("assign", "p", ("binop", ("identifier","a"), "+", ("identifier","b"))) ,
("assign", "q", ("binop", ("identifier","b"), "+", ("identifier","c"))) ,
("assign", "r", ("binop", ("identifier","c"), "+", ("identifier","d"))) ,
]

answer4 = [ \
("assign", "x", ("binop", ("identifier","a"), "+", ("identifier","b"))) ,
("assign", "y", ("binop", ("identifier","b"), "+", ("identifier","c"))) ,
("assign", "z", ("binop", ("identifier","c"), "+", ("identifier","d"))) ,
("assign", "b", ("identifier", "z")) ,
("assign", "z", ("number", 5)) ,
("assign", "p", ("binop", ("identifier","a"), "+", ("identifier","b"))) ,
("assign", "q", ("binop", ("identifier","b"), "+", ("identifier","c"))) ,
("assign", "r", ("identifier", "b")) ,
]

print "test 4"
#print optimize(example4) == answer4
import pprint; pprint.pprint(optimize(example4))

