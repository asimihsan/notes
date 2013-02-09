# Wes Weimer
# -- INSTRUCTOR PROVIDES this file
#
# This is an interpreter for a simple subset of HTML. The interpretation is
# that a graphics library is called on the text and tags of the HTML. This
# is basically just an AST tree walk.
#
# It is likely that this would be explained by the professor in class and
# provided to students. 
import ply.lex as lex
import ply.yacc as yacc
import jstokens
import jsgrammar
import graphics as graphics
import jsinterp 

# Recursively Interpret an HTML AST
def interpret(ast):     # AST 
        for node in ast:
          nodetype = node[0]
          if nodetype == "word-element":
                  graphics.word(node[1]) 
          elif nodetype == "tag-element":
                  tagname = node[1];
                  tagargs = node[2];
                  subast = node[3];
                  closetagname = node[4]; 
                  if (tagname <> closetagname):
                    graphics.warning("(mistmatched " + tagname + " " + closetagname + ")")
                  else: 
                    graphics.begintag(tagname,tagargs);
                    interpret(subast)
                    graphics.endtag(); 
          elif nodetype == "javascript-element": 
                jstext = node[1]; 
                jslexer = lex.lex(module=jstokens) 

                if False: # JavaScript lexer/parser debugging
                  print jstext
                  jslexer.input(jstext) 
                  while True:
                          tok = jslexer.token() 
                          if not tok: break
                          print tok 

                jsparser = yacc.yacc(module=jsgrammar,tabmodule="parsetabjs") 
                jsast = jsparser.parse(jstext,lexer=jslexer) 
                result = jsinterp.interpret(jsast)
                graphics.word(result) 
