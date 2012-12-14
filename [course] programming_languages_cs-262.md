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
        token.lexer.begin('htmlcomment')
        
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
        -    Grade level of text by measuring number of words in sentences and number of letters per word.
    -    *Natural language processing*: real world languages can be lexed, but parsing is much more difficult.
        -    *Document summarisation*. This is very difficult!
        -    Joke is that natural language processing is "AI-complete" (analogous to NP-complete).

## Unit 3: Syntactic Analysis

### 3.2: Bags of Words

-    Recall we've done String -> Lexing -> List of Tokens.
-    Lexing uses regular expressions.
-    But having a list of words isn't enough!
-    A natural language admits an infinite number of utters, but *not* all utterances. There are rules! All **grammars** rule something out.

### 3.3: Syntactic Structure

-    Noam Chomsky, 1955. *Syntactic Structures*
    -    Utterances have rules, **formal grammars**.
-    Grammatical sentence: follows the rules.
-    Can write down formal grammars using a set of **rewrite rules**.
    -    *Sentence* -> *Subject* *Verb*
    -    *Subject* -> Teachers
    -    *Subject* -> Students
    -    *Verb* -> write
    -    *Verb* -> think
    -    (italics => **non-terminals**, non-italcs => **terminals**).
    -    Non-terminals  can be re-written into terms on right, sometimes terminals,
    -    You can always replace non-terminals.
    -    Once you get a terminal it can't be changed.
-    e.g.

        sentence
        -> subject verb
        -> students verb
        -> students think

-    This is a **derivation**. Use re-write rules.
-    Can perform multiple derivations, e.g.

        sentence
        -> subject verb
        -> subject write
        -> teachers write    

### 3.5: Infinity and Beyond

-    Add just one rule, gives phenomenal power!

        Sentence -> Subject Verb
        Subject -> students
        Subject -> teachers
        Subject -> Subject and Subject
        Verb -> think
        Verb -> write
        
-    **Recursion** in a context-free grammar can allow for an infinite number of utterances (but not all utterances).
-    **Recursive rewrite rules** allow for **recursive grammars**.
-    Infinite utterances, *all of finite length*.
-    Formally, the number of strings is **countably infinite**.

### 3.7: An Arithmetic Grammar

-    Finite grammar -> countably infinite utterances.
-    Chomsky argues this is how a "finite brain" -> infinite creative ideas.
-    Arithmetic grammar example:

        Exp -> Exp + Exp
        Exp -> Exp - Exp
        Exp -> number

-    e.g. `number number` is not valid, `number + number - number` is valid.

### 3.8: Syntactical analysis

-    Recall:
    -    Lexical Analysis ("lexing"): String -> Token List.
    -    Syntactical Analysis ("parsing"): Token List -> Valid in Grammar?
-    Valid in grammar == is in the language of the grammar.

-    Lexing + Parsing = Expressive Power
-    Word rules + sentence rules = creativity!

        Exp -> Exp + Exp
        Exp -> Exp - Exp
        Exp -> Number
        
        and
        
        def t_NUMBER(token):
            r'[0-9]+'
            token.value = int(token.value)
            return token
            
-    Can now check for valid sequence of tokens.

        1 + 2, good
        7 + 2 - 2, good
        - - 2, bad.
        
### 3.9: Statements

        Stmt -> identifier = Exp
        Exp -> Exp + Exp
        Exp -> Exp - Exp
        Exp -> number

        lata = 1, good
        lata = lata + 1, bad

### 3.10: Optional Parts

-    "I think" vs. "I think corectly".
-    Optional adverbs!
-    Can specify two rewrite rules for the same non-terminal, where one of them goes to epsilon, i.e. the empty string.

        Sentence -> OptionalAdjective Subject Verb
        Subject -> william
        Subject -> tell
        OptionalAdjective -> accurate
        OptionalAdjective -> \epsilon
        Verb -> shoots
        Verb -> bows
        
        8 possible utterances!
        
### 3.11: More Digits

-    Grammars can encode **regular languages**.

        number - r'[0-9]+'
        
        Number -> Digit MoreDigits
        MoreDigits -> Digit MoreDigits
        MoreDigits -> \epsilon
        Digit -> 0
        Digit -> 1
        …
        Digit -> 9
        
        Number
        -> Digit MoreDigits
        -> Digit Digit MoreDigits
        -> Digit Digit \epsilon
        -> Digit 2
        -> 42

### 3.12: Grammars and Regexps

-    Grammar >= Regexp

        regexp = r'p+i?' # e.g. p, pp, pi, ppi
        
        Regexp -> Pplus Iopt
        Pplus -> p Pplus
        Pplus -> p
        Iopt -> i
        Iopt -> \epsilon
        
### 3.13: Context-Free Languages

-    *Regular expressions* describe *regular languages*.
-    *Context-free grammars* describe *context-free languages*.

        A -> B
        xyzAxyz -> xyzBxyz
        
-    Above, can always go from A -> B regardless of context around A, assuming we keep context the same.
-    Here are three different regular expression forms, and equivalent context-free grammars.

        r'ab'   => G -> ab
        
        r'a*'   => G -> \epsilon
                   G -> aG
                   
        r'a|b'  => G -> a
                => G -> b

-    But regular languages != context-free languages.

### 3.14: Parentheses

-    Consider:

        P -> ( P )
        P -> \epsilon  

-    **Balanced parentheses**.
-    Balanced parenthesis are **not regular**.
    -    The proof for this follows directly from the [**"pumping lemma" for regular languages**](http://en.wikipedia.org/wiki/Pumping_lemma_for_regular_languages).
-    Let's try:

        r'\(*\)*'
        
-    But it doesn't match parentheses :(.

### 3.16: Intuition

-    *Impossible* for a regular language to balance parentheses.
-    Here is some intuition.
-    We want:

        (^N )^N
        
-    i.e. both N times.
-    But all we can write is:

        (* )*
        
-    And these stars need not be the same.
-    Think about finite state machines. We only need to know where we are, not where we came from.
    -    Regular expressions just don't have that memory.

### 3.18: Extracting Information

-    HTML JavaScript -> formal grammars.
-    **Parse trees** are inverted trees / pictorial representations of the structure of an utterance.
-    Start with a non-terminal, then expand downwards. Tree growing upside down.
-    Interior nodes are non-terminals, leaves are terminals.

### 3.20: Ambiguity

-    Both natural languages and programming language elements can be ambiguous. Two or more interpretations.
-    e.g. "I saw Jane Austen using binoculars".

        1 - 2 + 3
        
        could be 2 or -4!
        
-    A grammar is **ambiguous** if there is *at least one* string in the grammar that has *more than one* different parse tree.
        
### 3.21: To The Rescue

-    Parentheses can come to the ( Rescue ).

        exp - exp + exp
        exp -> exp - exp
        exp -> number
        exp -> ( exp )
        
### 3.23: Grammar for HTML

        <b>Welcome to <i>my</i> webpage!</b>
        
        Html -> Element Html
        Html -> \epsilon
        Element -> word
        Element -> TagOpen Html TagClose
        TagOpen -> < word >
        TagClose -> </ word >

-    The parse tree for a web page allows us to determine the extent of tags, e.g. how much of a web page should be bolded.

### 3.25: Revenge of JavaScript

-    JavaScript is similar to Python.
-    In Python:

        def absval(x):
            if x < 0:
                return 0 - x
            else:
                return x

-    In JavaScript:

        function absval(x) {
            if x < 0 { 
                return 0 - x;
            } else {
                return x;
            }
        }

-    JavaScript uses braces to signify lexical scope. Python uses indentation.

-    In Python

        print "hello" + "!"
        
-    In JavaScript:

        document.write("hello" + "!"
        
        or
        
        write("hello" + "!")

-    All JavaScript function calls require brackets.

### 3.27: Universal Meaning

-    We can translate between Python and JavaScript. Theory of **universal grammar**.
-    They're both **Turing-Complete**.

Partial grammar for JavaScript:

        Exp -> identifier
        Exp -> TRUE
        Exp -> FALSE
        Exp -> number
        Exp -> string
        Exp -> Exp + Exp
        Exp -> Exp - Exp
        Exp -> Exp * Exp
        Exp -> Exp / Exp
        Exp -> Exp < Exp
        Exp -> Exp == Exp
        Exp -> Exp && Exp
        Exp -> Exp || Exp
        
-    !!AI surely missing parentheses, operator precedence?
-    !!AI not missing quoted strings with escaped characters because this is a lexical definition, not a syntactic one.

### 3.29: JavaScript Grammar

-    Expressions ~= Noun Phrases
-    Operators ~= Verbs
-    Statements ~= Sentences

-    Jay becomes three.
-    -> j = 3;

        Statement -> identifier = Exp
        Statement -> return Exp
        Statement -> if Exp CompoundStatement
        Statement -> if Exp CompoundStatement else CompoundStatement
        CompoundStatement -> { Statements }
        Statements -> Statement; Statements
        Statements -> \epsilon

-    So in addition to expressions we know have statements that build upon expressions.
-    !!AI surely `CompoundStatement` could also be `Statement` without braces?
    -    !!AI Actually no. Better to allow `CompoundStatement` or `Statement` in `Statement`?
-    !!AI Note the limitations of the above:
    -    Only one statement allowed; need a similar trick as HTML to make this infinite.

### 3.31: JavaScript Functions

-    We've seen expressions and statemetns.
-    We need functions!
    -    Declaration.
    -    Calling.
-    Python program = List of statements and function definitions.
-    JavaScript program the same!

           Js -> Element Js
           Js -> \epsilon
           
           Element -> function identifier ( OptParams ) CompoundStatement // function definition
           Element -> Statement;

           OptParams -> Params
           OptParams -> \epsilon
           
           Params -> identifier, Params
           Params -> identifier
           
-    Note that Element forces Statements to be *terminated* with semi-colons.
-    Note that Params forces identifiers to be *delimited* by colons.
-    This is a cute property of Context-Free Grammars.

           Exp -> … // as before
           Exp -> identifier( OptArgs ) // function call
           
           OptArgs -> Args
           OptArgs -> \epsilon
           Args -> Exp, Args
           Args -> Exp

-    Notice that a string that is in a grammar doesn't prevent certain errors.
    -    Could define `sin(x)`, but then call it as `sin(50, 60)`.

### 3.33: Lambda

-    Creating grammars vs. checking utterances.
-    Accept: `(1 + (2 + 3))`
-    Reject: `1 + + + ) 3`.
-    But how to check a given string is in the language of a given grammar?
    -    *Super slow*. Enumerate all valid strings, then see if your string is in there.
        -    Countably infinite number of strings!

-    **Lambda** (make me a function, **anonymous function**)

           def addtwo(x): return x+2
           addtwo(2) # = 4
           
           mystery = lambda(x): x+2
           mystery(3) # = 5
           
           pele = mystery
           pele(4) # = 6

### 3.34: List Power

        def mysquare(x): return x*x
        map(mysquare, [1,2,3,4,5]) # = [1,4,9,16,25]
        
        map(lambda(x): x*x, [1,2,3,4,5]) # same!

        [x*x for x in [1,2,3,4,5] # same!

### 3.37: Generators

-    List comprehensions are declarative, awesome.
-    Downside: need to write down the starting lists.

        def odds_only(numbers):
            for n in numbers:
                if n % 2 == 1:
                    yield n

-    `yield`: not return! A **generator**.
-    Convenient way to filter.
-    Even easier:

        [x for x in [1,2,3,4,5] if x % 2 == 1]
        
-    **Guard**, aka **predicate**.
   
### 3.39: Checking Valid Strings

-    Python program to check a string is in a grammar.

        Exp -> Exp + Exp
        Exp -> Exp - Exp
        Exp -> ( Exp )
        Exp -> num
        
        grammar = [
            ("Exp", ["Exp", "+", "Exp"]),
            ("Exp", ["Exp", "-", "Exp"]),
            ("Exp", ["(", "Exp", ")"],
            ("Exp", ["num"]),
        ]

-    Given e.g. `print exp;`

        utterance = ["print", "exp", ";"]
        into:
        ["print", "exp", "-", "exp", ";"]
        
        
        pos = 1
        result = utterance[0:pos] + rule[1] + utterance[pos+1:]
        
-    We want to enumerate all valid strings in the grammar, the super-slow method.
-    e.g.

            start with "a exp"
            with depth 1, get:
            "a exp + exp"
            "a exp - exp"
            "a (exp)"
            "a num"

-    Let's code it up:

        grammar = … (as above)
        
        def expand(tokens, grammar):
            for i, token in enumerate(tokens):
                for (rule_lhs, rule_rhs) in grammar:
                    if token == rule_lhs:
                        result = tokens[0:i] + rule_rhs + tokens[i+1:]
                        yield result
  
        depth = 2
        utterances = [["exp"]]
        for x in xrange(depth):
            for sentence in utterances:
                utterances = utterances + [ i for i in expand(sentence, grammar)]
        
        for sentence in utterances:
            print sentence

-    We saw: a slow way to encode grammars and enumerate strings.
-    But will learn a more efficient way to encode grammar rules and check for validity.

### Office Hours 3

-    Lex and Yacc used in the real world?
    -    Yes!
    -    The idea of making a lexer and/or a parser is so common there are many tools for many languages.
    -    Flex and Bison are free (GNU) versions of Lex and Yacc.
    -    Nowadays can find Flex and Bison for many languages.
    -    Java has Cup.
    -    Ruby has Rubylex and Rubyyacc.
    -    Python has ply.
    -    Ocaml has Ocamllex and Ocamlyacc.

-    Beyond Context Free
    -    Anything besides context-free grammars and regular languages?
    -    Context-free grammars are not the end-all and be-all.
    -    The opposite of CFG is **context-sensitive grammar**.
    -    Local state, memory.
    -    We will need to keep track of context when we interpret JavaScript and HTML later in the class - we'll need context sensitivity in unit 5.
    
-   Testing
    -    How to write good test cases?
    -    Formally, *checking that software implementation matches its specification*.
    -    Software testing gives us *confidence, not certainty*.
    -    There an infinite number of inputs.
    -    Hope that test cases are indicative of problems, or highlight errors.
    -    Goal of a good test suite is that once its run we'll have confidence is that there are no bugs.
    -    Think of corners, edge cases.
    -    *Be creative* and think that people are *cheating you or deceiving you* - the human brain is very good at adopting this stance.
    -    For *numbers*: try 0, try negatives, try positives, prime numbers, compostivies.
    -    For *lists*: try ascending order, descending order, random, empty, very big.
    -    For *grammars and strings*: short and long strings, recursive and non-recursive grammars.
    -    A lot of research in *automated test input generation*, to force programs down different branches.
    -    Whenever there is an infinite number of possibilities, room for creativity.
    
-    Beyond parsing
    -    Can context-free grammars be used to do anything besides parse languages?
    -    Yes!
    -    *Security*
        -    Regular expressions can be used in virus checking.
        -    Virus checkers are giant lexers.
        -    e.g. cross-site scripting and SQL injection.
        -    Can use CFGs if user input is normal or if it's trying to take advantage of XSS or SQL injection.
        -    Pretend to parse the string, and if the changes that results from the string or the parse tree is too large then we know that something bad is going on.
    -    *Optimization*
        -    Production compilers and intepreters.
        -    Faster, less memory, less power.
        -    We will cover basic optimization in unit 6.
        -    *Data flow analysis*: e.g. if x = 0 then y = x + x is always 0.
        -    Best known methods for doing data flow analysis use context-free grammars, in particular context-free language         reachability.
        -    Problem is equivalent to "can we generate a string in this context-free grammar".
    -    *Computational Linguistics*
        -    CFGs came out of computational linguistics.
    -    *Specification mining*
        -    Determining what a program should be doing by reading its source code.
        -    Output takes the form of a formal grammar or a state machine.
        -    e.g. "should always use braces" or "close a file after you've opened it".
    -    *Encryption*
        -    Cell phones try to encrypt voice content.
        -    But if I've used a lot of computational linguistics then we know there are different patterns of speech and pauses.
        -    Phones try to use silence detection.
        -    Whoops! We know where the pauses are likely to be, and then work backwards to what language you're speaking and your regional accent.
        -    But if you sacrifice power then you can workaround by encrypting everything.
        
## Unit 4

### 4.1: Introduction

-    Microsoft *SLAM*, now *static driver verifier*.
    -    Torture test 3rd party devices.
-   **Model checking**: check software based on knowledge of its source code.
-   Important to **memoize**, remember what you've already done in order to save time.

### 4.2: Time Flies

-    Given a string S and a grammar G, is string S in the language of G?
-    "Time flies like an arrow, fruit flies like a banana."
    -    Ambiguity. Time is flying, but fruit isn't flying, it's 'fruit flies' liking.

### 4.3: Brute Force

-    **Brute force**: try all options exhaustively.
-    We enumerated all strings in grammar.
-    For countably infinite grammars this is pretty useless!
    
        S -> (S)
        S -> \epsilon
        
        Is '(()' in grammar?
        
-    Key insight - we can stop somewhere during our enumeration.
-    Parsing idea: be lazy, don't duplicate work.
-    Perl: Pathologically Eclectic Rubbish Lister! :).
    -    Virtues of a programmer: laziness, impatience, hubris.

### 4.4: Fibonacci numbers

-    Our basic recursive method is really wasteful!
-    **Memoization**.
-    Solution: write known answers in a a Python dictionary.

        def memofibo(n, chart = None):
            if chart is None:
                chart = {}
            if n <= 2:
                chart[n] = 1
            if n not in chart:
                chart[n] = memofibo(n-1, chart) + memofibo(n-2, chart)
            return chart[n]

### 4.8: Memoization for Parsing

-    Cast your mind back to FSMs and regular expressions.
-    To check if a string is accepted by an FSM we used our finger to keep track.
-    But FSMs have obvious states to put fingers on.
-    Where do you put your finger during parsing?
-    And will need more than one finger!

        S -> E
        E -> E + E
        E -> E - E
        E -> 1
        E -> 2
        
        input = 1 + 2
        
-    When you parse `1 +`, where am I?
-    No states, but we have rules and the next input.
-    There are rules that are more likely to be used next than others.
-    Formally we put a red dot inside one or more of the rules' RHS to keep track of where we are.
    -    Left of red dot: what we've seen.
    -    Right of red dot: what we haven't seen yet.
-    Example of a **parsing state**.

### 4.9: Parsing state

-    If the red dot ends up on the right of the start symbol's rule, you've parsed the string! i.e.

        S -> E <dot>

-    A **parsing state** is a rewrite rule from the grammar augmented with one red dot on the right-hand side of the rule.

### 4.10: Possible States

        Input: 1 +
        State: E -> 1 + <dot> E
        
-    This cannot be true! A parsing state must be a rewrite rule *from the grammar* augmented with one red dot. `E -> 1 + E` is not a rule from the grammar.

### 4.11: Charting Parse States

-    Suppose we have `parse([t_1, T_2, …, t_n, …, t_last])`
-    `chart[N]` = all parse states we could be in after seeing `t_1, t_2, …, t_n` only!
-    e.g.

        E -> E + E
        E -> int
        
        Input = int + int

        chart[0] =
            [E -> <dot> E + E,
             E -> <dot> int]
             
        chart[1] = 
            [E -> int <dot>,
             E -> E <dot> + E]
             
        chart[2] =
            [E -> E + <dot> E]

### 4:14: Magical Power

-    Grammars can be recursive => power.
-    We'll need to keep track of one extra piece of information: how many tokens we've seen so far.

        E -> E + E
        E -> int
        
        Input = int + int

        chart[0] =
            [E -> <dot> E + E,
             E -> <dot> int - seen 0]
             
        chart[1] = 
            [E -> int <dot>,
             E -> E <dot> + E]
             
        chart[2] =
            [E -> <dot> int - seen 2,
             E -> E + <dot> E]

-    Must add **starting position** aka **from position** to our parse states.
-    Because we want to parse. *Parsing* is the *inverse* of *producing strings*.

        int + int
        E + int        # apply E -> int
        E + E          # apply E -> int
        E              # apply E -> E + E
        
-    Parsing is going down.
-    Generating is going up. 

###  4.16: Building the chart

-    If you build the chart, you have solved parsing!

        S -> E
        E -> …
        
        S -> E <dot> - starting at 0 => we've parsed it.
        # We want to be in this state!
        
-    If inputs is T tokens long:

        S -> E <dot> start at 0 in chart[T]
        
-    If we can build the chart, and the above is true, then the string is in the language of the CFG.


### 4.17: Closure

-    Start:

        chart[0], S -> <dot> E from 0
        
-    End:

        chart[T], S -> E <dot> from 0.
        
-    Making intermediate entries
-    Suppose:

        S -> E + <dot> E, from j, in chart[i] (seen i tokens)
        
-    Expecting to see E in the future.
-    Need to find all rules that go to E and "bring them in".

- - -

-    Let's say:

        chart[i] has X -> ab <dot> cd, from j.
        
-    abcd may be terminals, nonterminals, or epsilon.
-    For all grammar rules:
        
        c -> pqr
        
-    We add:

        c -> <dot> pqr, from i
        
-    To `chart[i]`.
   
- - -

-    This is **predicting** aka **computing the closure**.

### 4.18: Computing the Closure

Suppose:

        E -> E -E
        E -> (F)
        E -> int
        F -> string
        
        Input: int - int
        Seen 2 tokens so far
     
        chart[2] has E -> - <dot> E, from 0

    







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