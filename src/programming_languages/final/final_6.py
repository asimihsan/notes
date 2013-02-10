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

class AvailableExpressions(object):
    def __init__(self):
        # ---------------------------------------------------------------------
        #    Track availability of expressions with respect to variable names.
        # ---------------------------------------------------------------------
        self.available = []

    def print_available(self):
        print "available:\n%s" % self.available

    def invalidate(self, variable_name):
        print "invalidate entry. variable_name: %s" % variable_name
        self.print_available()

        new_available = []
        for (available_variable_name, available_expressions) in self.available:
            should_be_preserved = True
            if variable_name == available_variable_name:
                should_be_preserved = False
            else:
                for expression in available_expressions:
                    if expression[0] == "identifier" and expression[1] == variable_name:
                        should_be_preserved = False
            if should_be_preserved:
                new_available.append((available_variable_name, available_expressions))

        print "invalidate exit. variable_name: %s" % variable_name
        self.print_available()

    def update(self, variable_name, expression):
        print "update entry. variable_name: %s, expression: %s" % (variable_name, expression)
        self.print_available()

        if not any(available_variable_name == variable_name
                   for (available_variable_name, _) in self.available):
            self.available.append((variable_name, []))
        for i, (available_variable_name, available_expressions) in enumerate(self.available):
            if available_variable_name == variable_name:
                self.available[i] = (available_variable_name, available_expressions + [expression])

        print "update exit. variable_name: %s, expression: %s" % (variable_name, expression)
        self.print_available()

    def is_available(self, expression):
        return any(expression in expressions for (_, expressions) in self.available)

    def get_variable_name_for_expression(self, expression):
        if not self.is_available(expression):
            return None
        for (variable_name, expressions) in self.available:
            if expression in expressions:
                return variable_name
        return None

def optimize(ast):
    available = AvailableExpressions()

    new_ast = []
    for (ast_operation, variable_name, rhs_expression) in ast:
        print "optimize. ast_operation: %s, variable_name: %s, rhs_expression: %s" % (ast_operation, variable_name, rhs_expression)

        # Invalidate the LHS variable name.
        available.invalidate(variable_name)

#       ("binop", exp, operator, exp)
#       ("number", number)
#       ("identifier", variable_name)
        assert(rhs_expression[0] in ["binop", "number", "identifier"])
        if rhs_expression[0] == "binop":
            # Maybe the RHS is available?
            if available.is_available(rhs_expression):
                new_rhs_expression = available.get_variable_name_for_expression(rhs_expression)
                new_ast.append((ast_operation, variable_name, new_rhs_expression))
            else:
                new_ast.append((ast_operation, variable_name, rhs_expression))

            # invalidate all variables on RHS
            #print rhs_expression
            (_, rhs_exp1, rhs_operator, rhs_exp2) = rhs_expression
            for exp in [rhs_exp1, rhs_exp2]:
                if exp[0] == "identifier":
                    available.invalidate(exp[1])

            # Refresh "available" recursively (see update() for more info)
            available.update(variable_name, rhs_expression)
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
#import pprint; pprint.pprint(optimize(example1))

example2 = [ \
("assign", "x", ("binop", ("identifier","a"), "+", ("identifier","b"))) ,
("assign", "a", ("number", 2)) ,
("assign", "z", ("binop", ("identifier","a"), "+", ("identifier","b"))) ,
]

print "test 2"
import pprint; pprint.pprint(optimize(example2))
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
#import pprint; pprint.pprint(optimize(example4))

