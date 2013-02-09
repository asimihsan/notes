# Debugging Environments
#
# Debugging is critical to making high-quality software. In this problem I
# have inserted a bug into our JavaScript interpreter and you will have to
# fix it. In particular, we will focus on function call expressions.
#
# Suppose our code for eval_exp(), evaluating JavaScript expressions, looks
# like this :

# def eval_exp(exp,env):
#         etype = exp[0]
#         if etype == "identifier":
#                 vname = exp[1]
#                 value = env_lookup(vname,env)
#                 if value == None:
#                         print "ERROR: unbound variable " + vname
#                 else:
#                         return value
#         elif etype == "number":
#                 return float(exp[1])
#         elif etype == "string":
#                 return exp[1]
#         elif etype == "true":
#                 return True
#         # ...
#         elif etype == "call":
#                 return eval_call(exp,env)
#
# Then the function eval_call() is responsible for handling function call
# expressions. I have written a buggy version of it below. You must find
# and fix the bug.
#
# To test your eval_call() and localize the bug, you may define the
# variable webpage to hold any webpage text (presumably including
# JavaScript) that you like.
#
# Hint: Pay careful attention to environments. Remember that a function is
# defined in one environment but called in another.

import ply.lex as lex
import ply.yacc as yacc
import graphics as graphics
import jstokens
import jsgrammar
import jsinterp
import htmltokens
import htmlgrammar
import htmlinterp

htmllexer  = lex.lex(module=htmltokens)
htmlparser = yacc.yacc(module=htmlgrammar,tabmodule="parsetabhtml")
jslexer    = lex.lex(module=jstokens)
jsparser   = yacc.yacc(module=jsgrammar,tabmodule="parsetabjs")
env_lookup = jsinterp.env_lookup
eval_exp = jsinterp.eval_exp
JSReturn = jsinterp.JSReturn
eval_stmts = jsinterp.eval_stmts
env_update = jsinterp.env_update

def eval_call(exp,env):
    # Recall: exp = (fname, args, body, fenv)
    fname = exp[1]
    args = exp[2]
    fvalue = env_lookup(fname,env)
    if fname == "write":
        argval = eval_exp(args[0],env)
        output_sofar = env_lookup("javascript output",env)
        env_update("javascript output",output_sofar + str(argval),env)
    elif fvalue[0] == "function":
        fparams = fvalue[1]
        fbody = fvalue[2]
        fenv = fvalue[3]
        if len(fparams) <> len(args):
            print "ERROR: wrong number arguments to " + fname
        else:
            # make a new environment frame
            # !!AI the error was here. Yes, we need to make a new
            # environment frame for this function call, but the parent
            # must be the **environment frame when the function was
            # initialized**, not the current calling environment frame
            newenv = (fenv,{ })

            for i in range(len(args)):
                argval = eval_exp(args[i],env)
                (newenv[1])[fparams[i]] = argval
            # evaluate the body in the new frame
            try:
                eval_stmts(fbody,newenv)
                return None
            except JSReturn as r:
                return r.retval
    else:
        print "ERROR: call to non-function " + fname

jsinterp.eval_call = eval_call

# This example webpage already demonstrates the error, but you may want
# to change or refine it to localize the bug.

# Another webpage, trying to localize.
webpage2 = """<html>
<p>
<script type="text/javascript">
function f(a) {
    var g = function(b) {
        write(a);
        write(" ");
        write(b);
    } ;
    return g;
}

var foo = f(3);
var b = 7;
foo(4);
</script>
</p>
</html>
"""

# Original webpage
webpage = """<html>
<p>
The correct answer is 3.0 4.0:
<script type="text/javascript">
function tvtropes(tgwtg) {
    var theonion = "reddit" + "pennyarcade";
    var loadingreadyrun = function(extracredits) {
        write(tgwtg);
        write(" ");
        write(extracredits);
    } ;
    return loadingreadyrun;
}
var yudkowsky = tvtropes(3);
var tgwtg = 888;
var extracredits = 999;
yudkowsky(4);
/* Shoutouts to a random sampling of Western Web Comedy,
 * Analysis and Literature circa 2012. Bonus points if you
 * can get any of them to return the favor. Udacity needs
 * a tvtropes page. :-) */
</script>
</p>
<hr> </hr>
<img src="cs262.png"> </img>
</html>
"""


htmlast = htmlparser.parse(webpage,lexer=htmllexer)
graphics.initialize() # let's start rendering a webpage
htmlinterp.interpret(htmlast)
graphics.finalize() # we're done rendering this webpage



