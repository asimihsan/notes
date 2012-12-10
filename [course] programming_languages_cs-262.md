# Programming Languages (Udacity, CS-262)

## Unit 1

### 1.4: Breaking Up Strings

-    Input

        <b>Hello 1
        
-    Can use `string.find()`, look for space.

### 1.5: Selecting Substrings

        "hello"[1:3] = "el"
        "hello"[1:] = "ello"
        
### 1.6: Split

        "Jane Eyre".split() = ["Jane", "Eyre"]
        
### 1.7: Regular Expressions

-    Regular = "simple strings"
-    Expression = "concise notation"
-    Efficiently describe ranges of simple strings.

### 1.9: Import Re

        import re
        re.findall(r"[0-9]", "1+2==3") = ["1", "2", "3"]

### 1.12: Concatenation

        r"[a-c][1-2]"
        
        "a1", "a2", "b1", …
        
### 1.14: One or more

-    **Maximal munch**: REs should consume the longest possible strings. Default.

### 1.15: Finite State Machines

-    Visual representation of REs.
-    States.
    -    Start state.
    -    Accept state(s).
-    Transitions based on input.
-    **Self-loop**: transition from and to the same state.

### 1.18: Disjunction

-    Two accepting states!
-    Pipe / or operator.

        impore re
        r = r"[a-z]+|[0-9]+"
        re.findall(r, "Goethe 1749") = ["oethe", "1749"]
        
        # note that:
        [0-2] = "0|1|2"   

### 1.21: Options

-    i.e. optional parts.
-    e.g. postive and negative integers. minus sign is optional.
-    Naive FSM is wasteful, too many states.
-    Can we have an edge that consumes no input?
-    Yes: $\epsilon$. aka "the empty string". aka "consume no input".
-    For regular expressions, can use a question mark, `?`
    -    "optional"
    -    "the previous thing 0 or 1 times".
    
            import re
            r = r"-?[0-9]+"
            re.findall(r, "1861-1941 R. Tagore") = ["1861", "-1941"]

### 1.22: Escape Sequences

-    Star, `*`, zero or more copies.

        a+ === aa*
        
-    But how to match actual stars, question marks, brackets?
-    Escape using `\`.

### 1.23: Hyphenation

-    Write a regexp to accept lower-cased words, or singly-hyphenated lowercase words.

        r = r"[a-z]+-?[a-z]+"
  
-    This is OK, accept can only accept words of length 2 or more.
-    Tempted to make either one a Kleene star. But then accept bad inputs like "-a" or "a-".
-    Would like to group the ? operator!

### 1.26: Quoted Strings

-    `.`: any character except new-line.
-    Note regexps are **non-overlapping**: will not return extra characters!
-    `[^ab]`: any characters that aren't a or b.
          
### 1.27: Structure

        `(?:xyz)+
        
-    Above is grouped, so matches:

        xyz
        xyzxyz
        …
        
-    e.g. want to match any number of any permutation of `do re mi`.

        r = r"do+|re+|mi+"
        
-    Above doesn't work because the operator binds to the last letter.

        r = r"(?:do|re|mi)+"
        
-    Above works, operator binds to the groups of letters.

### 1.28: Escaping the escape

-    Find a regexp that matches double-quotes string literals and allows for escaped double quotes.

        regexp = r'"(?:(?:\\.)*|[^\\])*"'
        
-    Regular expressions can "sing" "ABC 123" and "BINGO", but _not_ "99 bottles of beer on the wall".
    -    Can't count!
    
### 1.29: Representing a FSM

-    "Tracing with a finger" is basically what computers do to evaluate FSMs!
    -    Where you are in the input.
    -    What state you are in.
-    Python dictionaries to represent edges.

        edges[(1, 'a')] = 2
        
-    edges[(state, input)] = next_state
-    also need to know accepting states

        accepting = [3]
        
-    don't need a list of states! already encoded in `edges`.

### 1.30: FSM simulator

        edges = {(1, 'a') : 2,
                 (2, 'a') : 2,
                 (2, '1') : 3,
                 (3, '1') : 3}
        
        accepting = [3]
        
        def fsmsim(string, current, edges, accepting):
            if len(string) == 0:
                return current in accepting
            letter = string[0]
            next_state = edges.get((current, letter), None)
            if next_state is None:
                return False
            return fsmsim(string[1:], next_state, edges, accepting)

### 1.31: FSM Interpretation

-    What are `edges` and `accepting` for `q*`?
-    Start state is `1`.

        edges = {(1, 'q'): 1}        
        accepting = [1]
        
### 1:32: More FSM Encoding

-    What are `edges` and `accepting` for RE:

        r"[a-b][c-d]?"

        edges = {(1, 'a'): 2,
                 (1, 'b'): 2,
                 (2, 'c'): 3,
                 (2, 'd'): 3}
        
        accepting = [2, 3]

### 1.34: Epsilon and Ambiguity

-    An FSM is **ambiguous** if it has epsilon transitions or has multiple outgoing edges leaving the same state with the same label.
-    FSM accepts a string s if *there exists even one path* from the start state to *any accepting state*.
    -    FSMs are generous.
    -    But this doesn't help us.

### 1.35: Phone It In.

-    Recognize phone numbers with or without hyphens.

        regexp = r'[0-9]+(?:[0-9]|-[0-9])*'

### 1.37: Non-deterministic FSM

-    "Easy-to-write" FSMs with *epsilon* transitions or *ambiguity* are known as **non-deterministic finite state machines** (NFAs).
    -    Don't know exactly where to put your finger!
-     A "lock-step" FSM with no epsilon edges or no ambiguity is a **deterministic finite state machine** (DFA).
    -    Our `fsmsim` function can handle DFAs.
    
-    But the non-determinism, just like the real world, is just an illusion of free will.    
-    Every non-deterministic FSM has a corresponding deterministic FSM that *accepts exactly the same strings*.
    -    NFAs are *not more powerful* than DFAs, they're just more convenient.

-    Idea: build a deterministic machine D where every state in D corresponds to a set of states in the non-deterministic machine.
    -    The set of states in the DFA is the **epsilon-closure** of the transitionary states in the NFA (recall the Coursera course).
    -    On states with two edges with same label take both simultaneously.
    -    If any state in NFA is accepting then the superset state in DFA is also accepting.

### 1.38: Save the world

-    **Strings** are sqeuences of characters.
-    **Regular expressions**: concise notation for specifying sets of strings.
    -    More flexible than fixed string matching. 
    -    Phone numbers, words, numbers, quotes, strings.
    -    Search for and match them.
-    **Finite state machines**: pictorial equivalent of regular expressions.
-    Every FSM can be converted to a **deterministic** FSM.
-    **FSM simulation**: It is very easy, ~10 lines of recursive code, to see if a deterministic FSM accepts a string.

### Problem Set 1

-    Given `re.findall()`, there are equivalent problems that do not use `re.findall()`.
    -    Recall that regular expressions may be expressed as finite state machines, and vice versa.
    -    Hence write an FSM and use `fsmsim()`. This gives you `re.match()`, only one search.
    -    Algorithm for matching `re.findall()`:
    
            s1 = "12+34"
            fsmsim() for '[0-9]+'.
            
            call fsmsim("1"), it matches.
            call fsmsim("2"), it matches.
            call fsmsim("12+"), it doesn't match. Hence one 'token' is '12', and advance input to '3'.
            
            call fsmsim("3"), it matches.
            call fsmsim("4"), it matches.
            end of string.
            
            result is ["12", "34"].


## Unit 2

### 2.1: Introduction

-    Going to make a lexical analyzer.

### 2.3: Specification

-    Recall outline of course.
    -    Start with webpage. *outline*.
    -    Break it down to important *words*.
    -    Put words in a *tree*.
    -    Get a result.

### 2.8: Taking HTML Apart

-    In both Latin and ancient Japanese, spaces weren't used as delimeters.
-    Need domain knowledge to lexically analyze them!
-    Given this fragment

        Wollstonecraft</a>

-    Want the following output

        word                 Wollstonecraft
        start of closing tag </
        word                 a
        end of closing tag   >
        word                 wrote

### 2.9: HTML Structure

-    **Token**: smallest unit of output of lexical analysis.
    -    words, strings, numbers, punctuation.
    -    *not* whitespace.

-    e.g.

         LANGLE        <
         LANGLESLASH   </
         RANGLE        >
         EQUAL         =
         STRING        "google.com"
         WORD          Welcome!

-    Left is name, right is example.         
-    Names of tokens are arbitrary, but would like them to be uppercase.

### 2.10: Specifying tokens

-    Use *regular expressions to specify tokens*. In Python:

        def t_RANGLE(token):
            r'>' # I am a regexp!
            return token # return text unchanged, but can transform it.
             
        def t_LANGLESLASH(token):
            r'/>'
            return token
            
### 2.11: Token values

-    By default the value is the string it matches. But we can transform text!

        def t_NUMBER(token):
            r'[0-9]+'
            token.value = int(token.value)
            return token

-    This is returned as an integer, not a string.
-    Remember that **maximal munch** is being used.

### 2.12: Quoted Strings

        def t_STRING(token):
            r'"[^"]*"'
            return token

### 2.13: Whitespace

        def t_WHITESPACE(token):
            r' '
            pass
            
-    By passing we skip it.

And if we define a word as any number of characters except <, >, or space, leaving the value unchanges:

        def t_WORD(token):
            r'[^<> ]+'
            return token

### 2.14: Lexical Analyzer

-    **Lexical Analyzer**, or **lexer**, is just a collection of token definitions.

### 2.15: Ambiguity

-    What if token definitions overlap?
-    "We don't just serve hamburgers, we serve people!"
-    **First one wins**, according to where it is in the file.

### 2.17: String snipping

-    For quoted strings really just want the contents of the quotes portion:

         def t_STRING(token):
             r'"[^"]*"'
             token.value = token.value[1:-1]
             return token

Making a lexer

    import ply.lex as lex
    
    tokens = (
        'LANGLE',        # <
        'LANGLESLASH',   # </
        'RANGLE',        # >
        'EQUAL',         # =
        'STRING',        # ".."
        'WORD'           # dada
    )   
    
    t_ignore = ' ' # shortcut for whitespace
   
    # note this is before t_LANGLE, want it to win
    def t_LANGLESLASH(token):
        r'</'
        return token
        
    def t_LANGLE(token):
        r'<'
        return token
        
    def t_RANGLE(token):
        r'>'
        return token
        
    def t_EQUAL(token):
        r'='
        return token
       
    def t_STRING(token):
        r'"[^"]*"'
        token.value = token.value[1:-1]
        return token
        
    def t_WORD(token):
        r'[^ <>]+'
        return token
        
    webpage = "This is <b>my</b> webpage!"
    htmllexer = lex.lex()
    htmllexer.input(webpage)
    while True:
        tok = htmllexer.token()
        if not tok: break
        print tok

-    Output is a list of LexToken objects.
-    They indicate `LexToken(TYPE, line, character)`. Indicate line and character on that line.

### 2.19: Tracking line numbers

-    Lexer keeps track of column number, but not line number.
    -    Column number is character since the beginning of the file.
-    We need to add a rule to help us, right at the top.

         def t_newline(token):
             r'\n'
             token.lexer.lineno += 1
             pass
   
-    But then we'd have to remove `\n` from `t_WORD`, just like we're currently ignoring spaces.

### 2.21: Commented HTML

-    Start with `<!--`, end with `-->`

How to add to lexer.

    states = (
        ('htmlcomment', 'exclusive'),
    )

If we are in the state `htmlcomment` we cannot be doing anything else at the same time, like looking for strings or words.

    def t_htmlcomment(token):
        r'<!--'
        token.lexer.being('htmlcomment')
        
    def t_htmlcomment_end(token):
        r'-->'
        token.lexer.lineno += token.value.count('\n')
        token.lexer.begin('INITIAL')
        
    def t_htmlcomment_error(token):
        token.lexer.skip(1)
        
-    `INITIAL` just means whatever you were going before coming into this state, i.e. `htmlcomment`.        
-    Note we even exclude our helpful little line number counter! Hence we need to count line breaks in the entire comment when it finishes.
-    Finally, we don't match anything in the comments. They all result in errors! Hence let's skip all the errors.
    -    But instead of `pass` we're actually gathering up all the characters that resulted in the error, so that we can subsequently count for newlines.
    
-    Just because a comment returns no tokens, it isn't ignored. It still splits up other tokens.

### 2.26: Identifier

-    **Identifier**: variable name or function name. Identify a value or storage locations.
    -    factorial, x, tmp, Super, WonderWoman, my_count.
    -    Not: _blah, 123.
    
            def t_identifier(token):
                r'[A-Za-z][A-Za-z0-9_]+'
                return token

### 2.27: Number

    def t_NUMBER(token):
        r'-?[0-9]+(?:\.[0-9]*)?'
        token.value = float(token.value)
        return token

### 2.28: The End Of The Line

Comments to the end of the line in JavaScript.

    def t_eolcomment(token):
        r'//[^\n]*'
        pass

### 2.30: Wrap Up

-    **Tokens**!
    -    Number, word, string.
    -    Specified by **regular expressions**.
-    HTML, Javascript.

### Office Hours 2

-    `ply` library
    -    First line of token definition is in the docstring! So `ply` can use reflection to get them.
    -    Each token has a regular expression.
    -    Then generate an NFA that has a special new start state, with an epsilon transition to each start state for each token. Massive union!
    -    Then convert to DFA!
    -    Lexer doesn't just accept strings. It accepts strings and knows what the token is.
    
-    Use of ply lexer states
    -    Convenience. One FSM per state.
    -    But not going to use one state for HTML, one state for Javascript.
    -    Instead we'll use two different lexer files entirely.
    -    Both running in the same program!

-    Internationalization
    -    ASCII is OK for English, 256 characters.
    -    Need more numbers for other langauges!
    -    How about 65,535?
    -    Unicode!
    -    Want to use special regular expression shortcuts, rather than character ranges.
    
-    Long Token Definition Rules
    -    Man, lots of rules! Is it really this long?
    -    There's no free lunch; yes, languages are complicated.
    -    But one can take a structured approach and make it manageable.
    -    Is it difficult to pave a road, build a sewer, paint a beautiful painting?
    -    Yes, but only need to do it once, then reuse forever.
    
-    Ill formed input
    -    Going to get to his in unit 3.
    -    But in this class we're going to recognize malformed input and then reject.
    -    In reality browsers put a huge amount of effort into being forgiving. Most webpages are malformed.
    -    **Error recovery**, **Error tolerance**, **Fault tolerance**.
    -    In practice you write duplicate rules, and then print out warnings and keep going.
    -    Applies to lexical analysis and semantic analysis.
    
-    Speak Javascript
    -    Yes, by the end of the class will have written simple but actual Javascript programs.
    -    But not going to do flashy DOM manipulation or UI.

-    Use of Lexing Elsewhere
    -    Yes! Large number of uses for lexing outside of languages.
    -    *Electronic commerce*; phone numbers, credit numbers use regular expressions.
    -    *Virus detection*. Based on regular expressions and lexing.
        -    Virus definition file is a giant list of tokens.
        -    Each virus gets a corresponding regular expression to find its payload etc.
    -    *Computational biology*.
        -    Strings, made up of four characters.
        -    Longest common substring matching.
        -    How do we make new drugs?
        -    Want to make mathematical models, governed by protein folding.
        -    *BLAST*. Common software project for doing this work.
    -    *Readability metrics* for both software programs and human languages.
        -    Grade level of bool by measuring number of words in sentences and number of letters per word.
    -    *Natural language processing*: real world languages can be lexed, but parsing is much more difficult.
        -    *Document summarisation*. This is very difficult!
        -    Joke is that natural language processing is "AI-complete" (analogous to NP-complete).

## References

## Unit 1

-    [Regular Expressions in Python](http://code.google.com/edu/languages/google-python-class/regular-expressions.html) (Google Code University)

-    Bernoulli numbers
    -    Sequence of rational numbers.
    -    Appear in Taylor series expansions of `tan()` and `tanh()`.
-    Barbara Jane Liskov
    -    Invented CLU.
    -    Won Turing Award.
-    Mir Taqi Mir and Khwaja Mir Dard.
    -    18th century Urdu poets
    -    Two of the four pillars of Urdu poetry.
-    Rabindranath Tagore
    -    Bengali poet, Nobel Prize laureate.
    -    Where the mind is without fear.