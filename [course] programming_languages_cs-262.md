# Programming Languages (Udacity, CS-262)

## Student

[Asim Ihsan](http://www.asimihsan.com)

## Unit 1

### 1.4: Breaking Up Strings

-    Input

        <b>Hello 1
        
-    Can use `string.find()`, look for space.

### 1.5: Selecting Substrings

```python
"hello"[1:3] = "el"
"hello"[1:] = "ello"
```
        
### 1.6: Split

```python
"Jane Eyre".split() = ["Jane", "Eyre"]
```
        
### 1.7: Regular Expressions

-    Regular = "simple strings"
-    Expression = "concise notation"
-    Efficiently describe ranges of simple strings.

### 1.9: Import Re

```python
import re
re.findall(r"[0-9]", "1+2==3") = ["1", "2", "3"]
```

### 1.12: Concatenation

```python
r"[a-c][1-2]"

"a1", "a2", "b1", …
```
        
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


```python
impore re
r = r"[a-z]+|[0-9]+"
re.findall(r, "Goethe 1749") = ["oethe", "1749"]
```

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
    
```python
import re
r = r"-?[0-9]+"
re.findall(r, "1861-1941 R. Tagore") = ["1861", "-1941"]
```

### 1.22: Escape Sequences

-    Star, `*`, zero or more copies.

        a+ === aa*
        
-    But how to match actual stars, question marks, brackets?
-    Escape using `\`.

### 1.23: Hyphenation

-    Write a regexp to accept lower-cased words, or singly-hyphenated lowercase words.

```python
r = r"[a-z]+-?[a-z]+"
```
  
-    This is OK, accept can only accept words of length 2 or more.
-    Tempted to make either one a Kleene star. But then accept bad inputs like "-a" or "a-".
-    Would like to group the ? operator!

### 1.26: Quoted Strings

-    `.`: any character except new-line.
-    Note regexps are **non-overlapping**: will not return extra characters!
-    `[^ab]`: any characters that aren't a or b.
          
### 1.27: Structure

```python
(?:xyz)+
```
        
-    Above is grouped, so matches:

        xyz
        xyzxyz
        …
        
-    e.g. want to match any number of any permutation of `do re mi`.

```python
r = r"do+|re+|mi+"
```
        
-    Above doesn't work because the operator binds to the last letter.

```python
r = r"(?:do|re|mi)+"
```
        
-    Above works, operator binds to the groups of letters.

### 1.28: Escaping the escape

-    Find a regexp that matches double-quotes string literals and allows for escaped double quotes.

```python
regexp = r'"(?:(?:\\.)*|[^\\])*"'
```
        
-    Regular expressions can "sing" "ABC 123" and "BINGO", but _not_ "99 bottles of beer on the wall".
    -    Can't count!
    
### 1.29: Representing a FSM

-    "Tracing with a finger" is basically what computers do to evaluate FSMs!
    -    Where you are in the input.
    -    What state you are in.
-    Python dictionaries to represent edges.

```python
edges[(1, 'a')] = 2
```
        
-    edges[(state, input)] = next_state
-    also need to know accepting states

```python
accepting = [3]
```
        
-    don't need a list of states! already encoded in `edges`.

### 1.30: FSM simulator

```python
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
```

### 1.31: FSM Interpretation

-    What are `edges` and `accepting` for `q*`?
-    Start state is `1`.

```python
edges = {(1, 'q'): 1}        
accepting = [1]
```
        
### 1:32: More FSM Encoding

-    What are `edges` and `accepting` for RE:

```python
r"[a-b][c-d]?"

edges = {(1, 'a'): 2,
         (1, 'b'): 2,
         (2, 'c'): 3,
         (2, 'd'): 3}

accepting = [2, 3]
```

### 1.34: Epsilon and Ambiguity

-    An FSM is **ambiguous** if it has epsilon transitions or has multiple outgoing edges leaving the same state with the same label.
-    FSM accepts a string s if *there exists even one path* from the start state to *any accepting state*.
    -    FSMs are generous.
    -    But this doesn't help us.

### 1.35: Phone It In.

-    Recognize phone numbers with or without hyphens.

```python
regexp = r'[0-9]+(?:[0-9]|-[0-9])*'
```

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

```    
s1 = "12+34"
fsmsim() for '[0-9]+'.

call fsmsim("1"), it matches.
call fsmsim("2"), it matches.
call fsmsim("12+"), it doesn't match. Hence one 'token' is '12', and advance input to '3'.

call fsmsim("3"), it matches.
call fsmsim("4"), it matches.
end of string.

result is ["12", "34"].
```


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

```python
def t_RANGLE(token):
    r'>' # I am a regexp!
    return token # return text unchanged, but can transform it.
     
def t_LANGLESLASH(token):
    r'/>'
    return token
```
            
### 2.11: Token values

-    By default the value is the string it matches. But we can transform text!

```python
def t_NUMBER(token):
    r'[0-9]+'
    token.value = int(token.value)
    return token
```

-    This is returned as an integer, not a string.
-    Remember that **maximal munch** is being used.

### 2.12: Quoted Strings

```python
def t_STRING(token):
    r'"[^"]*"'
    return token
```

### 2.13: Whitespace

```python
def t_WHITESPACE(token):
    r' '
    pass
```
            
-    By passing we skip it.

And if we define a word as any number of characters except <, >, or space, leaving the value unchanges:

```python
def t_WORD(token):
    r'[^<> ]+'
    return token
```

### 2.14: Lexical Analyzer

-    **Lexical Analyzer**, or **lexer**, is just a collection of token definitions.

### 2.15: Ambiguity

-    What if token definitions overlap?
-    "We don't just serve hamburgers, we serve people!"
-    **First one wins**, according to where it is in the file.

### 2.17: String snipping

-    For quoted strings really just want the contents of the quotes portion:

```python
def t_STRING(token):
    r'"[^"]*"'
    token.value = token.value[1:-1]
    return token
```

Making a lexer

```python
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
```

-    Output is a list of LexToken objects.
-    They indicate `LexToken(TYPE, line, character)`. Indicate line and character on that line.

### 2.19: Tracking line numbers

-    Lexer keeps track of column number, but not line number.
    -    Column number is character since the beginning of the file.
-    We need to add a rule to help us, right at the top.

```python
def t_newline(token):
    r'\n'
    token.lexer.lineno += 1
    pass
```
   
-    But then we'd have to remove `\n` from `t_WORD`, just like we're currently ignoring spaces.

### 2.21: Commented HTML

-    Start with `<!--`, end with `-->`

How to add to lexer.

```python
states = (
    ('htmlcomment', 'exclusive'),
)
```

If we are in the state `htmlcomment` we cannot be doing anything else at the same time, like looking for strings or words.

```python
def t_htmlcomment(token):
    r'<!--'
    token.lexer.begin('htmlcomment')
    
def t_htmlcomment_end(token):
    r'-->'
    token.lexer.lineno += token.value.count('\n')
    token.lexer.begin('INITIAL')
    
def t_htmlcomment_error(token):
    token.lexer.skip(1)
```
        
-    `INITIAL` just means whatever you were going before coming into this state, i.e. `htmlcomment`.        
-    Note we even exclude our helpful little line number counter! Hence we need to count line breaks in the entire comment when it finishes.
-    Finally, we don't match anything in the comments. They all result in errors! Hence let's skip all the errors.
    -    But instead of `pass` we're actually gathering up all the characters that resulted in the error, so that we can subsequently count for newlines.
    
-    Just because a comment returns no tokens, it isn't ignored. It still splits up other tokens.

### 2.26: Identifier

-    **Identifier**: variable name or function name. Identify a value or storage locations.
    -    factorial, x, tmp, Super, WonderWoman, my_count.
    -    Not: _blah, 123.
    
```python
def t_identifier(token):
    r'[A-Za-z][A-Za-z0-9_]+'
    return token
```

### 2.27: Number

```python
def t_NUMBER(token):
    r'-?[0-9]+(?:\.[0-9]*)?'
    token.value = float(token.value)
    return token
```

### 2.28: The End Of The Line

Comments to the end of the line in JavaScript.

```python
def t_eolcomment(token):
    r'//[^\n]*'
    pass
```

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

```python
def absval(x):
    if x < 0:
        return 0 - x
    else:
        return x
```

-    In JavaScript:

```javascript
function absval(x) {
    if x < 0 { 
        return 0 - x;
    } else {
        return x;
    }
}
```

-    JavaScript uses braces to signify lexical scope. Python uses indentation.

-    In Python

```python
print "hello" + "!"
```
        
-    In JavaScript:

        document.write("hello" + "!")
        
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

```python
def mysquare(x): return x*x
map(mysquare, [1,2,3,4,5]) # = [1,4,9,16,25]

map(lambda(x): x*x, [1,2,3,4,5]) # same!

[x*x for x in [1,2,3,4,5] # same!
```

### 3.37: Generators

-    List comprehensions are declarative, awesome.
-    Downside: need to write down the starting lists.

```python
def odds_only(numbers):
    for n in numbers:
        if n % 2 == 1:
            yield n
```

-    `yield`: not return! A **generator**.
-    Convenient way to filter.
-    Even easier:

```python
[x for x in [1,2,3,4,5] if x % 2 == 1]
```
        
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

```python
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
```

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

```python
def memofibo(n, chart = None):
    if chart is None:
        chart = {}
    if n <= 2:
        chart[n] = 1
    if n not in chart:
        chart[n] = memofibo(n-1, chart) + memofibo(n-2, chart)
    return chart[n]
```

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

        E -> E - E
        E -> (F)
        E -> int
        F -> string
        
        Input: int - int
        Seen 2 tokens so far
     
        chart[2] has E -> E - <dot> E, from 0

Then the result of computing the closure:

        E -> <dot> int from 2
        E -> <dot> (F) from 2
        E -> <dot> E - E from 2
        
The following are not in the result:

        E -> <dot> E - E from 0 # wrong from
        F -> <dot> string from 2 # wrong LHS

### 4.19: Consuming the Input

-    **Closures** are one of three methods required to complete the parsing chart.
-    **Shifting**, aka consuming the input, is another method.

-    Recall parsing state:

           X -> ab <dot> cd, from j in chart [i]
       
-    If c is non-terminal, => closure.
-    If c is terminal, => shift (i.e. consume the terminal).

          X -> abc <dot> d from j into chart [i+1]

-    Remember what this means. We've seen `i` tokens, and the `i+1`th token is `c`, a terminal.
-    We are not updating `from`, because that's where we've come from.

### 4.21: Reduction

        x -> ab <dot> cd
        
-    `c` is non-terminal, => closure
-    `c` is terminal, => shift
-    `cd` is `\epsilon`, i.e. nothing. => reduce.

-    **Reduction**: apply rewrite rules / productions in reverse.

        E -> E + E
        E -> int
        
        <dot> int + int + int
        int <dot> + int + int
        
        # magical reduction!
        E <dot> + int + int
        
        E + <dot> int + int
        E + int <dot> + int
        
        # magical reduction!
        E + E <dot> + int
        
        # magical reduction!
        E <dot> + int
        
        E + <dot> int
        ...

-    Reduction makes a parse tree in reverse.
-    But how to apply reductions?

### 4.23: Reduction Walkthrough

        E -> E + E <dot> from B in chart [A]
        
-    We've seen inputs up to B and are about to encounter `E + E`:

        input_1 input_2 … input_B | E + E
        
-    It's as if we saw the LHS at this point:

        input_1 input_2 … input_B | E
        
-    Where did we come from? Suppose chart[B] has:

        E -> E - <dot> E from C

-    By closure we're predicting to see E. Hence at this point we bring it in (?)
-    Reduction is a combination of closure and shifting.
-    So add:

        E -> E - E <dot> from C to chart[A]

-    Example!

        T -> aBc
        B -> bb
        
        input: abbc
        
        N = 0
        chart[0]
            T -> <dot>aBc, from 0
            
        N = 1, a
        chart[1]
            # shift
            T -> a <dot>Bc, from 0
            
            # and we see a non-terminal, so bring in closure
            B -> <dot>bb, from 1
            
        N = 2, ab
            # shift
            B -> b<dot>b, from 1
            
        N = 3, abb
            # shift
            B -> bb<dot>, from 1
            
            # - red dot at end of rule, so reduce.
            # - came from state 1.
            # - Does anyone in state 1 want to see B? 
            # - Yes! T -> a<dot>Bc is looking for one.    
            # - So transplant that rule here
            T -> aB<dot>c, from 0        
 
### 4.25: Addtochart

Adding state to chart:

```python
def addtochart(chart, index, state):
    if not state in chart[index]:
        chart[index] = [state] + chart[index]
        return True
    else:
        return False
```
 
### 4.26: Revenge of List Comprehensions

Grammar:

        S -> P
        P -> (P)
        P ->
        
In Python:

```python
grammar = [
    ("S", ["P"]),
    ("P", ["(", "P", ")"]),
    ("P", []),
] 
```

Parser state:

        X -> ab<dot>cd from j
        
In Python:

```python
state = ("x", ["a", "b"], ["c", "d"], j)
```

### 4.27: Writing the closure

-    Know how to seed this table, add first rule with dot on left-most position to `chart[0]`.
-    Know how to see if a string is in the language of the grammar, check `chart[n]` for n tokens to see if we're in the final state.
-    Looking at `chart[i]`, we see `x -> ab<dot>cd from j`.
-    We'll call:

        next_states = closure(grammar, i, x, ab, cd, j)
        for next_state in next_states:
            any_changes = addtochart(chart, i, next_state)
                          or any_changes

-    What is `closure()`?

```python
def closure(grammar, i, x, ab, cd, j):
    next_states = [
        (rule[0], [], rule[1], i)
        for rule in grammar
        if len(cd) > 0 and
           rule[0] == cd[0]
    ]
    return next_states
```

### 4.29: Writing shift

-    We're currently looking at `chart[i]` and we see `X -> ab<dot>cd from j`.
-    The input is `tokens`.
-    We'll write:

```python
next_state = shift(tokens, i, x, ab, cd, j)
if next_state is not None:
    any_changes = addtochart(chart, i+1, next_state)
                  or any_changes
```
                          
-    What is `shift()`?

```python
def shift(tokens, i,x, ab, cd, j):
    if len(cd) > 0 and tokens[i] == cd[0]:
        return (x, ab + [cd[0]], cd[1:], j)
    else:
        return None
```
                
### 4.30: Writing reductions

-    We're looking at `chart[i]`, we see `X -> ab<dot>cd from j`.
-    We'll write:

```python
next_states = reductions(chart, i, x, ab, cd, j)
for next_state in next_states:
    any_changes = addtochart(chart i, next_state)
                  or any_changes
                  

def reductions(chart, i, x, ab, cd, j):
    # x -> ab<dot> from j
    # chart[j] has y -> ... <dot>x ... from k
    return [
        (jstate[0],
         jstate[1] + [x],
         jstate[2][1:],
         jstate[3])
        for jstate in chart[j]
        if len(cd) > 0 and
           len(jstate[2]) > 0 and
           jstate[2][0] == x
    ]
```
                
### 4.31: Putting it together

```python
# see notes/src/programming_languages/ps4_parser.py
# above has closure, shift, and reductions in-lined.

def parse(tokens, grammar):
    tokens = tokens + ["end_of_input_marker"]
    chart = {}
    start_rule = grammar[0]
    for i in xrange(len(tokens) + 1):
        chart[i] = []
    start_state = (start_rule[0], [], start_rule[1], 0)
    chart[0] = [start_state]
    for i in xrange(len(tokens)):
        while True:
            changes = False
            for state in chart[i]:
                # State === x -> ab<dot>cd, j
                (x, ab, cd, j) = state
                
                # Current state == x -> ab<dot>cd, j
                # Option 1: For each grammar rule
                # c -> pqr (where the c's match)
                # make a next state:
                #
                # c -> <dot>pqr, i
                #
                # English: We're about to start
                # parsing a "c", but "c" may be
                # something like "exp" with its
                # own production rules. We'll bring
                # those production rules in.
                next_states = closure(grammar, i, x, ab, cd, j)
                for next_state in next_states:
                    changes = addtochart(chart, i, next_state) or changes
                    

                # Current State == x -> ab<dot>cd, j
                # Option 2: If tokens[i] == c,
                # make a next state:
                #
                # x -> abc<dot>d, j
                #
                # £nglish: We're looking for a parse
                # token c next and the current token
                # is exactly c! Aren't we lucky!
                # So we can parse over it and move
                # to j+1.
                next_state = shift(tokens, i, x, ab, cd, j)
                if next_state is not None:
                    any_changes = addtochart(chart, i+1, next_state) or any_changes
                    
                # Current state == x -> ab<dot>cd, j
                # Option 3: if cd is [], the state is
                # just x -> ab<dot>, j
                # For each p -> q<dot>xr, l in chart[j]
                # Make a new state:
                #
                # p -> qx<dot>r, l
                #
                # in chart[i].
                #
                # English: We've just finished parsing
                # an "x" with this token, but that
                # may have been a sub-step (like
                # matching "exp->2" in "2+3"). We
                # should update the higher-level
                # rules as well.
                next_states = reductions(chart, i, x, ab, cd, j)
                for next_state in next_states:
                    changes = addtochart(chart, i, next_state) or changes
                    
        if not changes:
            break

    accepting_state = (start_rule[0], start_rule[1], [], 0)
    return accepting_state in chart[len(tokens)-1]

result = parse(tokens, grammar)
print result
```

### 4.33: Parse Trees

-    We can tell if a string is valid.
-    But we need a parse tree!
-    Going to represent this as nested tuples.

```python
# tokens
def t_STRING(t):
    r'"[^"]*"'
    t.value = t.value[1:-1]
    return t
    
# parsing rules
def p_exp_number(p):
    'exp : NUMBER' # exp -> NUMBER
    p[0] = ("number", p[1])
    # p[0] is returned parse tree
    # p[0] refers to exp
    # p[1] refers to NUMBER.
    
def p_exp_not(p):
    'exp : NOT exp' # exp -> NOT exp
    p[0] = ("not", p[2])
    # p[0] refers to exp
    # p[1] refers to NOT
    # p[2] refers to exp
```

-    `p`: parse trees

### 4.34: Parsing HTML

```python
def p_html(p):
    'html : elt html'
    p[0] = [p[1]] + p[2]
    
def p_html_empty(p):
    'html : '
    p[0] = []
    
def p_elt_word(p):
    'elt : WORD'
    p[0] = ("word-element", p[1])
```

### 4.35: Parsing tags            

```python
def p_elt_tag(p):
    # <span color="red">Text!</span>:
    'elt : LANGLE WORD tag_args RANGLE html LANGLESLASH WORD RANGLE'
    p[0] = ("tag-element", p[2], p[3], p[5], p[7])
```

### 4.36: Parsing JavaScript

```python
def p_exp_binop(p):
    """exp : exp PLUS exp
           | exp MINUS exp
           | exp TIMES exp"""
    p[0] = ("binop", p[1], p[2], p[3])
```

-    Oh no! Ambiguity!
-    input: `1 - 3 - 5`
    -    **Left-associative**: `(1-3)-5 = -7`
    -    **Right-associative**: `1-(3-5) = 3`
-    Function calls

```python
def p_exp_call(p):
    'exp : IDENTIFIER LPAREN optargs RPAREN'
    p[0] = ("call", p[1], p[3])
```

-    Numbers

```python
def p_exp_number(p):     
    'exp : NUMBER'
    p[0] = ("number", p[1])
```

### 4.38: Precedence

-    But even with associativity, we need precedence to resolve mixtures/binding of operators.
-    Below gives precedence and associativity.

```python
precedence = (
    # lower precedence at the top
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIVIDE'),
    # higher precedence at the bottom 
)
```

### 4.41: Optional Arguments

```python
def p_exp_call(p):
    'exp : IDENTIFIER LPAREN optargs RPAREN'
    p[0] = ("call", p[1], p[3])
    
def p_exp_number(p):
    'exp : NUMBER'
    p[0] = ("number", p[1])
    
def p_optargs(p):
    """optargs : exp COMMA optargs 
               | exp
               | """
    if len(p) == 1:
        p[0] = []
    elif len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = [p[1]] + p[3]
        
# or can separate out parsing rules in OR statement
# into its own function. separate rules give better
# performance, as the parser has done all of your 
# len() work for you.
```

## Office Hours 4

-    Why do we create languages? If we parse JavaScript using Python, why not write everything in Python?
    -    Languages have different purposes.
    -    They focus on certain topics, reduce error rates in given domains.
    -    **Domain-specific langauges**: trying to solve a particular language and do it well.
    -    Hardware definition, e.g. VHDL and Prolog.
    -    Game level layout and engines.
    -    Scientific computing, e.g. FORTRAN.
    -    Time taken to write a program, and error rate.
    -    For many applications correctness is more important than performance.
        -    Python dictionaries are one line, no bugs!
        -    C dictionaries are modules and memory allocations, many lines - possibly many bugs!
    -    All languages, however, are Turing complete - fundamentally equivalent.
    
-    Parsing tools
    -    We're using memoization. Why not e.g. LALR(1)?
    -    Memoization is used in more complex methods like GLR.
    -    C++ doesn't fit into simpler LR(k) tools, needs GLR.
        -    e.g. Oink.
    -    All these tools have similar interfaces.
    -    Ultimately the question is "if the real world does X, why are we doing Y?"
    -    Key difference in pedagogy between *knowing how to program* and *knowing how to program in a given language or framework*.
        -    Former is much more important.
    -    LALR(1) and recursive descent are much more difficult than the algorithm we've covered in this class.
    -    Our method is **Earley parsing**, O(n^3) in the worst-case for ambiguous grammars, but handles any grammar. Other methods are faster but handle restricted subsets of grammars.
    -    Also, our method is O(n) for unambiguous, simple grammrs, i.e. these same restricted subsets.
    -    Research over the past 10 years is re-focusing on GLR chart-based parsers, similar to ours.
    -    Just an accident of history that we're using hacks like LALR(1).
    
-    We're using memoization. Are we secretly doing dynamic programming?
    -    **Dynamic programming**: solve a problem by keeping a chart and adding to this chart over time.
    -    Useful when a problem exhibits the **optimal substructure property**: deal with a problem by dealing with smaller problems.
    -    Yes!
    
-    Compiling vs. interpretation.
    -    Interpretation: lex, parse, then act!
    -    Compiling: precompute a lot of this, optimize it, store as a binary file.
    -    Compiling is like packing really well for a trip. Repeatedly going back to your house for stuff vs. packing a suitcase very well.
    -    Java compiles down to byte-code, and the byte-code is interpreted by a JVM.
    -    Even C is compiled down to e.g. x86 assembly, which a processor interprets!

## Problem Set 4

### Problem 1: Parsing States

What is in chart[2], given:

        S -> id(OPTARGS)
        OPTARGS ->
        OPTARGS -> ARGS
        ARGS -> exp,ARGS
        ARGS -> exp

        input: id(exp,exp)

        chart[0]
            S -> <dot>id(OPTARGS)$, from 0
            
        chart[1]
            # shift
            S -> id<dot>(OPTARGS)$, from 0
            
        chart[2]
            # shift
            S -> id(<dot>OPTARGS)$, from 0
            
            # OPTARGS could be epsilon, hence
            # in one world:
            S -> id(OPTARGS<dot>)$, from 0
            
            # In another world we see OPTARGS
            # and it isn't epsilon, so we closure.
            OPTARGS -> <dot>ARGS, from 2
            OPTARGS -> <dot>, from 2
            
            # !!AI I think by recursion we apply closure to ARGS; reminiscent of epsilon-closure during DFA->NFA conversion.
            ARGS -> <dot>exp,ARGS from 2
            ARGS -> <dot>exp from 2

## Unit 5

### 5.1: Formal Semantics

-    Figuring out what code means in context.

### 5.2: Interpreters

-    String of HTML and JavaScript
-    Lexical analysis: break it down into tokens and words.
-    Syntactic analysis: parse these into a tree.
-    **Semantics**, aka **interpreting**: walk the tree and understand it.
    -    For web pages!
    -    What do they look like.
    
### 5.3: Syntax vs. Semantics

-    We've looked at form, not meaning
-    "Colorless green ideas sleep furiously!"
    -    Syntactically correct.
    -    But semantically ambiguous.
-    Programming examples
     
        1 + 2 # = 3
        "hello" + " world" # = "hello world"

        1 + "hello" # ???

### 5.4: Bad Programs

-   **Type checking**: one of the goals of *semantic analysis* is to notice and rule out bad programes; programs that will apply the wrong sort of operations to the wrong sort of object.

### 5.5: Types

-   A **type** is a set of similar objects, like *numbers* or *strings*, with associated operations.
-   Often different types can use the same operations, but for different reasons.
    -   `len` for string vs. list.
    -   `+` for numbers, strings, and lists.
    -   Analogy: the word "execute", and its meanings in different sentences.
-   Some operations make sense for some types, not for others.
    -   Division for numbers vs. strings.
-   **Syllepsis**: humourous semantic incongruity.
    -   "She lowered her standards by raising her glass, her covrage, her eyes, and his hopes."
-   **Mismatched tags**.
    -   In HTML.
    -   Analogous to matching balanced parantheses.

### 5.7: HTML interpreter

-   Interpreting by walking a parse tree.

        ("word-element", "Hello")

        ("tag-element", "b", ..., "b")

        ("javascript-element", "function fibo(N) { ...")
        # Embedded JavaScript in HTML.

### 5.8: Graphics

-   Need to make a picture to render a webpage!
-   We're using `re` for regexps, `ply` for lexing and parsing, `timeit` for benchmarking.
-   Here is our API:

```python
graphics.word(string)
# draw on screen

graphics.begintag(string, dictionary)
# doesn't draw, just makes a note. like changing pen colours.
# dictionary passes in attributes, e.g. href.

graphics.endtag()
# most recent tag.

graphics.warning(string)
# debugging, in bold red color.
```

-   Example:

        Nelson Mandela <b>was elected</b> democratically.

        # how this calls into graphics API

        graphs.word("Nelson")
        graphics.word("Mandela")
        graphics.begintag("b", {})
        graphics.word("was")
        graphics.word("elected")
        graphics.endtag("b")
        graphics.word("democratically.")

-   Interpret code.

```python
import graphics

def interpret(trees): # Hello, friend
    for tree in trees: # Hello,
        # ("word-element","Hello")
        nodetype=tree[0] # "word-element"
        if nodetype == "word-element":
            graphics.word(tree[1])
        elif nodetype == "tag-element":
            # <b>Strong text</b>
            tagname = tree[1] # b
            tagargs = tree[2] # []
            subtrees = tree[3] # ...Strong Text!...
            closetagname = tree[4] # b
            # QUIZ: (1) check that the tags match
            # if not use graphics.warning()
            if tagname != closetagname:
                graphics.warning("Mismatched tag. start: '%s', end: '%s'" % (tagname, closetagname))
            else:
                #  (2): Interpret the subtree
                # HINT: Call interpret recursively
                graphics.begintag(tagname, {})
                interpret(subtrees)
                graphics.endtag()
```

### 5.10: Arithmetic

-   That's almost it for HTML!
    -   `word-element` - done.
    -   `tag-element` - done.
    -   `javascript-element` - not done.
        -   Interpret the JavaScript to a string.
        -   Call graphics.word() on that string.
-   However, JavaScript is *semantically richer* than HTML.
    -   Arithmetic, start here.
    -   Variables.
-   e.g.

        input: (1*2) + (3*4)

-   This is **evaluation**, aka **eval**, for arithmetic.
    -   `eval_exp`.
-   Code:

```python
def eval_exp(tree):
    # ("number" , "5")
    # ("binop" , ... , "+", ... )
    nodetype = tree[0]
    if nodetype == "number":
        return int(tree[1])
    elif nodetype == "binop":
        left_child = tree[1]
        operator = tree[2]
        right_child = tree[3]
        # QUIZ: (1) evaluate left and right child
        left_value = eval_exp(left_child)
        right_value = eval_exp(right_child)
        
        # (2) perform "operator"'s work
        assert(operator in ["+", "-"])
        if operator == "+":
            return left_value + right_value
        elif operator == "-":
            return left_value - right_value
```

### 5.12: Context

-   Variables - need their current value.
-   e.g. "The king of France is bald."
    -   Syntax correctly, but semantic correctness requires knowing what time we're talking about.
    -   Right now there isn't a king of France!
-   **State** of a program execution is a mapping from variable names to values.
-   Evaluating an expression requires us to know the current state. 
-   Tempting to have one dictionary for this state, but one day we might want to make this a bit more complicated.
-   So we'll hide it behind an API

```python
def env_lookup(environment, variable_name):
    ...
```

-   Code:

```python
def eval_exp(tree, environment):
    nodetype = tree[0]
    if nodetype == "number":
        return int(tree[1])
    elif nodetype == "binop":
        # ...
    elif nodetype == "identifier":
        # ("binop", ("identifier","x"), "+", ("number","2"))
        # QUIZ: (1) find the identifier name
        # (2) look it up in the environment and return it
        return env_lookup(environment, tree[1])
```

### 5.15: Control Flow

-   `if`, `while`, `return` change the flow of control.
    -   These tokens are called **statements**.
-   An **expression** is just `2+3` or `x+1`.
-   Statements often contain expressions, but not the other way around.

```python
def eval_stmts(tree, environment):
    stmttype = tree[0]
    if stmttype == "assign":
        # ("assign", "x", ("binop", ..., "+",  ...)) <=== x = ... + ...
        variable_name = tree[1]
        right_child = tree[2]
        new_value = eval_exp(right_child, environment)
        env_update(environment, variable_name, new_value)
    elif stmttype == "if-then-else": # if x < 5 then A;B; else C;D;
        conditional_exp = tree[1] # x < 5
        then_stmts = tree[2] # A;B;
        else_stmts = tree[3] # C;D;
        # QUIZ: Complete this code
        # Assume "eval_stmts(stmts, environment)" exists
        if eval_exp(conditional_exp, environment):
            return eval_stmts(then_stmts, environment)
        else:
            return eval_stmts(else_stmts, environment)
```

### 5.17: Creating an Environment

        Python:
            x = 0
            print x + 1

        JavaScript:
            var x = 0
            write(x+1)

-   Can have multiple values in different contexts.

        x = "outside"
        def myfun(x):
            print x
        myfun("inside")

        # get "inside"

### 5.18: Scope

-   Environment cannot be a flat mapping.
-   Variables have **scope**: can be bound to many values.

### 5.19: Identifiers and storage

-   Identifier (variable) names vs. storage places.
-   Store values for variables in explicit storage locations.
-   And as we move into a scope we create a new *child* environment, that knows who its parent is.
-   Child environments can recurse upwards to get variable values.
-   Setting variables only go upwards if we don't already have it defined.

### 5.20: Environments.

-   Special, **global environment** to start with.
-   Child environments have **parent** pointers. The global environment does not have a parent.

### 5.22: Chained environments

1.  Create a new environment.
    -   Its *parent* is the current environment.
2.  Create storage places in the new environment for each *formal parameter*.
    -   Formal parameters are e.g. arguments to a function.
3.  Fill in these places with the values of the actual arguments.
4.  Evaluate the function body in the new environment.

### 5.23: Greetings

-   Python supports nested functions!
-   These have nested envirnoment frames too.

### 5.24: Environment Needs

```python
def env_lookup(var_name, env):
    # env = (parent, dictionary)
    if var_name in env[1]:
        # do we have it?
        return (env[1])[var_name]
    elif env[0] is None:
        # am global?
        return None
    else:
        # ask parents
        return env_lookup(var_name, env[0])

def env_update(var_name, value, env):
    if var_name in env[1]:
        # do we have it?
        (env[1])[var_name] = value
    elif not (env[0] is None):
        # if not global, ask parents.
        env_update(var_name, value, env[0])
```

### 5.25: Declaring and Calling Functions

-   More trickiness than just environments.

```python
def mean(x):
    return x
    print "one thousand and one nights"
```

-   This is mean! We shouldn't print out anything.

### 5.26: Catching Errors

-   `try`, `except`.
-   Want to harness exceptions.
-   We'll use exceptions to simulate return statements.

```python
def eval_stmt(true, environment):
    stmttype = tree[0]
    if stmttype == "return":
        return_exp = tree[1] # return 1 + 2
        retval = eval_exp(return_exp, environment)
        raise Exception(retval)
```

-   Function calls

```python
def eval_stmt(tree,environment):
    stmttype = tree[0]
    if stmttype == "call": # ("call", "sqrt", [("number","2")])
        fname = tree[1] # "sqrt"
        args = tree[2] # [ ("number", "2") ]
        fvalue = env_lookup(fname, environment)
        if fvalue[0] == "function":
            # We'll make a promise to ourselves:
            # ("function", params, body, env)
            fparams = fvalue[1] # ["x"]
            fbody = fvalue[2]
            fenv = fvalue[3]
            if len(fparams) <> len(args):
                print "ERROR: wrong number of args"
            else:
                #QUIZ: Make a new environment frame
                newfenv = (fenv, {})
                for param, value in zip(fparams, args):
                    newfenv[1][param] = None
                    eval_value = eval_exp(value, environment)
                    env_update(param, eval_value, newfenv)
                try:
                    # QUIZ : Evaluate the body
                    eval_stmts(fbody, newfenv)
                    return None
                except Exception as return_value:
                    return return_value
        else:
            print  "ERROR: call to non-function"
    elif stmttype == "return": 
        retval = eval_exp(tree[1],environment) 
        raise Exception(retval) 
    elif stmttype == "exp": 
        eval_exp(tree[1],environment) 
```

### 5.29: Calling functions

-   In Python and JavaScript functions can be values. Hence we must represent function values.

        def myfun(x):
            return x+1

        function myfun(x) {
            return x+1;
        }

        ("function", fparams, fbody, fenv)

-   We *don't* need the function name.
    -   We'll be adding a mapping from the function name to this tuple in the old environment `fenv`.
-   Code:

```python
def eval_elt(tree, env):
    elttype = tree[0]
    if elttype == "function":
        fname = tree[1]
        fparams = tree[2]
        fbody = tree[3]
        fvalue = ("function", fparams, fbody, env)
        add_to_env(env, fname, fvalue)
```

### 5.31: Double-edged sword

-   We can define functions, call functions, and return from functions.
-   Function bodies are *statements* which contain *expressions*.
-   So much power!
-   Can use Python to simulate any JavaScript program.
-   Can use JavaScript to simulate any Python program.

-   Are natural languages equal?
    -   **Sapir-Whorf hypothesis**, aka **linguistic relativity hypothesis**, states that structure of language influences speakers' ability to reason.
    -   Language influences thought!

### 5.33: Comparing Languages

-   Real world: language influences thought.
-   Computing: languages are equally expressive.
    -   Sometimes easier to express in one language than another.
-   Interpreting is deep.
-   Downside is that simulation a program requires running it.

```python
x = 0
while True:
    x = x + 1
print x
```

-   If we interpret an infinite loop, our interpreter will also loop forever!

### 5.34: Infinite Loop

-   Want: look at program source, see if it loops forever or if it halts.
-   Provably impossible to do this.
-   Assume we have `halts()` which takes a procedure as an argument and returns `True` if that procedure halts and `False` if it loops forever.
-   Consider:

```python
def tsif():
    if halts(tsif):
        x = 0
        while True:
            x = x + 1
    else:
        return 0
```

-   If `tsif` halts, then it loops forever.
-   If `tsif` loops forever, then it halts.
-   *Contradiction*, hence `halts()` **cannot exist**.

-   Other **self-referential** contradictions:
    -   "This sentence is false"
    -   "The town barber only shaves those in the town that don't shave themselves. Who shaves the baber?"

-   Impossible to do it 100%, but there's a market to do it very approximately correctly, 99.99%.
    -   See "The Road Not Taken: Estimating Path Execution Frequency Statically", Weimer.

## Office Hours 5

-   Domain Specific Languages, why are they the future?
    -   Turing completeness, so can use any language to express anything.
    -   But how easy is it, how is the error handling, how is the performance?
    -   *Conciseness of representation*.
    -   *Type checking*, *run-time checking*, i.e. *safety*.
    -   *Compiler and/or runtime optimization*.
    -   e.g. MATLAB and linear algebra.
        -   Could do it all in C or C#.
        -   MATLAB is initially more concise. 
        -   But once you use operator overloading in C# this argument isn't so strong.
        -   However safety and optimization arguments are still strong.
        -   Nowadays contraints are *programmer time*, not *execution time*.
        -   The higher level statements to give to a compiler, i.e. the more *declarative* you are, the more the compiler is able to optimize effectively.
            -   Caches.
            -   Optimum instruction set instructions. 
        -   This higher-level-argument is analogous to the historical push from assembly to C.
    -   At the end of the day maybe there is no difference between a well-crafted library and a DSL.
        -   However, future development will likely include improvements to DSLs first, then libraries.

-   Exceptional Control Flow
    -   Language-level exception handling is super popular.
    -   Previous approach involved setting and getting global flags.
        -   Programmers are consistently poor at safely using global flags.
    -   Even in modern exception handling programmers make mistakes.
        -   Control flow is not visible, very non-local.
        -   Forget to close resources, maintain invariants.
    -   Exception handling is so popular that in average program 1-5% of code text will be catch/finally blocks.
    -   In large programs 3-46% of program is transitively reachable via catch/finally blocks.
    -   Philosophical issue: when you catch an error, you don't have enough time or context to appropriately handle it.
        -   e.g. file didn't save properly. Do I retry immediately, fail loudly, sleep then retry? Maybe I don't know.
        -   !!AI reminiscent of Hawkin's "On Intelligence".

-   Extending the course browser
    -   Right now we're rendering it to static LaTeX.
    -   Should study "elynx" and "Mosaic".
    -   First step, add ability for users to click on links.
        -   After rendering page we should wait for events of user clicking on certain parts of the page, the links.
    -   Another problem: how to lay out text so that it wraps lines properly?
        -   Formally, **minimum raggedness word wrapping problem**.
        -   Can solve this using dynamic programming and memoization.

-   Global Variables
    -   JavaScript can manipulate global variables. Is this a security issue?
    -   Oh my yes!
    -   Huge problem with unintended read and/or write access to variables outside of your scope.
    -   Early versions of PHP automatically copied form values into the global scope, for convenience. *Register global variables*.
    -   It is phenomenally easy to access these global variables and bypass business logic.
    -   PHP `explode()`, aka Python's `string.split()`, assigns to local variables and trusts user to be friendly. Nope!

## Unit 6

-   What we've done so far:
    -   HTML webpage, -> lexing -> list of tokens
    -   List of tokens -> parsing -> parse tree.
    -   Parse tree -> interpreting -> meaning (semantics).
-   Now we're going to put it all together.
-   Web browser architecture
    1.   Web page is lexed and parsed, into an Abstract Syntax Tree (AST)
    2.   HTML interpreter walks AST, calls JavaScript interpreter.
    3.  JavaScript code calls `write()`.
    4.  JavaScript interpeter stores text from `write()`.
    5.  HTML interpreter receives normal HTML, and JavaScript `write()` output, and calls `graphics` library.
    6.  Final image of webpage is created.

### Fitting Them Together

-   HTML interpreter calls JavaScript interpreter.
-   We treat JavaScript as a single HTML token.
    -   e.g. `5<7` or `a>b` is valid JavaScript, but would confuse an HTML lexer.
-   How to grab a chunk of embedded JS:

```python
def t_javascript(token):
    r'\<script\ type=\"text\/javascript\"\>'
    token.lexer.code_start = token.lexer.lexpos
    token.lexer.begin('javascript')

    # note that lexpos is such that we've already
    # stripped off the initial text/javascript part.

def t_javascript_end(token):
    r'\<\/script\>' # </script>
    token.value = token.lexer.lexdata[token.lexer.code_start:token.lexer.lexpos-9]
    token.type = 'JAVASCRIPT'
    token.lexer.lineno += token.value.count('\n')
    token.lexer.begin('INITIAL')
    return token

    # note that lexdata is such that we need to
    # manually strip off </script> 
```

### Extending our HTML grammar

-   Review:

```python
def p_element_word(p):
    'element : WORD'
    p[0] = ("word-element", p[1])

    # p[0] is the parse tree
    # p[1] is the child parse tree
```

-   Now need a JavaScript element:

```python
def p_element_javascript(p):
    'element : JAVASCRIPT'
    p[0] = ("javascript-element", p[1])
```

-   `JAVASCRIPT` in the parser is the same as `token.type` in the lexer. This is intentional: this is the link between the lexer and the parser.
-   Example:

```
HTML input:

    hello my
    <script type="text/javascript">document.write(99);</script>
    luftballons

Parse tree:

[("word-element", "hello"),
 ("word-element", "my"),
 ("javascript-element", "document.write(99)"),
 ("word-element", "luftballons")]
```

### Calling the Interpreter

```python
def interpret(trees):
    for tree in trees:
        treetype = tree[0]
        if treetype == "word-element":
            graphics.word(node[1])

        # covered HTML tags in another quiz...

        elif tree.type == "javascript-element":
            jstext = tree[1] # "document.write(55);"

            # jstokens is an external module
            jslexer = lex.lex(module=jstokens)

            # jsgrammar is another external module
            jsparser = yacc.yacc(module=jsgrammar)

            # jstree is a parse tree for JavaScript
            jstree = jsparser.parse(jstext, lexer=jslexer)

            # We want to call the interpreter on our AST
            result = jsinterp.interpret(jstree)
            graphics.word(result) 
```

### Evil problem

-   JavaScript may call `document.write()` more than once, but we still want to only return one string from the `jsinterp.interpret()` call.
-   Need to store text over time...use our environments from before!

### JavaScript output

-   Assume every call to `write` appends to the special "javascript output" variable in the global environment.

```python
def interpret(trees):
    # recall env = (parent, dictionary), and as this is the global environment the parent pointer is None
    global_env = (None, {"javascript output": ""})
    for elt in trees:
        eval_elt(elt, global_env)
    return (global_env[1])["javascript output"]
```

-   `"javascript output"`, in particular the space, is important; the user is not allowed to use a space in an identifier so they can't ever collide with this.

### Updating output

-	Treating write specially

```python
def eval_exp(tree, env):
	exptype = tree[0]
	if exptype == "call":
		fname = tree[1] # myfun in myfun(a,3+4)
		fargs = tree[2] # [a,3+4] in myfun(a,3+4)
		fvalue = envlookup(fname,env) # None for "write"; built-in
		if fname == "write":
			argval = eval_exp(fargs[0],env)
			output_sofar = env_lookup("javascript output",env)
			env_update("javascript output", \
				output_sofar + str(argval), env)
			return None
```

### Counting Frames

-	Consider the following embedded JS:

```javascript
function factorial(n) {
	if (n == 0) {
		return 1;
	}
	return n * factorial(n-1);
}
document.write(1260 + factorial(6));
```

-	The above has:
	-	One global environment frame, which always exists.
	-	One environment frame per call to `factorial`, so 7.
	-	A total of eight environment frames.
	-	No frame shares the same value of `n`.
	-	(see "`def eval_stmt(tree,environment)`" above).

### Debugging

-	"I would rather have a sandwich *then* be burned alive" (wanted *than*)
-	A good test case gives us confidence that a program implementation adheres to its specification. In this situation, a good test case reveals a bug.

###	Testing

-	We use **testing** to gain confidence that an implementation (a program) adheres to its specification (the task at hand) and meets all the requirements.
-	Not a proof! We can only gain more confidence.
-	If a program accepts an infinite set of inputs, testing alone cannot prove that program's correctness.
-	Our web page lexer, parser, interpreter, as it accepts inputs based on a CFG, has infinite number of inputs.
-	Software maintenance (ie.e. testing, debugging, refactoring) carries a huge cost.

-	When comparing a function's output to the expected output, code read and see what features of our interepeter we're using. If you're not using it, you're not testing it!

### Testing in depth

-	Suppose we make an error in our environment lookup:

```python
def env_lookup(vname,env):
	# env = (parent-poiner, {"x": 22, "y": 33})
	if vname in env[1]:
		return (env[1])[vname]
	else: # BUG
		return None # BUG 
```

-	Consider this valid code:

```javascript
var a = 1;
function mistletoe(baldr) {
	baldr = baldr + 1;
	a = a + 2;
	baldr = baldr + a;
	return baldr;
}
write(mistletoe(5));
```

-	Should be 9.
-	But we're not looking up parent environments properly, so will get an error!
-	Let's suppose we don't know where the bug is. How do we refine this test case?
-	Comment out lines, and see if it still happens. **Fault localisation**.
	-	Comment out the first three lines, just `return baldr`, it works!

### Testing at Mozilla

-	Simple test cases with obvious control flow are better.
-	Removing parts of a test case help localise faults.
-	Complex test cases hit more issues but they're more difficult to debug and track down the actual cause.
-	Linear test cases, with little to no control flow, are easy to "comment out lines" to localise faults.

### Anonymous functions

-	In Python:

```python
greeting = "hola"
def makegreeter(greeting):
	def greeter(person):
		print greeting + " " + person
	return greeter
sayhello = makegreeter("hello")
sayhello("gracie")
```

-	In JavaScript:

```javascript
var greeting = "hola";
function makegreeter(greeting) {
	var greeter = function(person) {
		write(greeting + " " + person);
	}
	return greeter;
}
var sayhello = makegreeter("hello");
```

-	Let's add anonymous functions to our JS interpreter.

```python
def eval_exp(tree,env):
	exptype = tree[0]
	# function(x,y) { return x+y }
	if exptype == "function":
		# ("function", ["x","y"], [ ("return", ("binop", ...) ])
		fparams = tree[1]
		fbody = tree[2]
		return ("function", fparams, fbody, env)
		# "env" allows local functions to see local variables
		# can see variables that were in scope *when the function was defined*
```

### Mistakes in anonymous functions

-	Suppose we get the return statement wrong:

```python
return ("function", fparams, fbody, global_env)
```

-	No test input with only one "function" can show the bug.
	-	However, with one recursive function we could see the bug.
-	Need just one variable in the global environment to see the bug.
-	If there are two functions at the top-level won't see the bug.
-	Need two functions, one nested in the other, to see the bug.

### Optimization

-	An **optimization** improves performance while retaining meaning, i.e. without changing the output.

```javascript
function factorial(n) {
	if (n == 0) { return 1; }
	return 1 * n * factorial(n-1);
}
```

-	This is correct, but we're multiplying by `1` a lot.
-	`1 \* n` can be replaced by `n`.
-	Smaller AST, faster recursive walk, fewer multiplications.

-	Note that modifying a local variable in a function, then not returning it, is redundant and can be removed.
	-	**Dead code**.

### Implementing Optimizations

1.	Think of optimizations

		x \* 1 == x
		x + 0 == x

2.	Transform parse tree

-	Replacing an expensive multiplication with a cheaper addition is an instance of [**strength reduction**](http://en.wikipedia.org/wiki/Strength_reduction).
-	`x/x` can't be optimized to `1` because if `x=0` then raises an exception, and we want to keep the same semantics after optimization.

### Optimizing Timing

-	Change the parse tree before interpreting.
-	Program text -> lexing -> tokens -> parsing -> tree -> *optimization* -> tree (simpler) -> interpreting -> result (meaning)
-	Optimization is optional!

```python
def optimize(tree):
	etype = tree[0]
	if etype == "binop": # a * 1 = a
		a = tree[1]
		op = tree[2]
		b = tree[3]
		if op == "*" and b == ("number","1"):
			return a
        elif op == "*" and b == ("number","0"):
            return ("number","0")
        elif op == "+" and b == ("number","0"):
            return a
		return tree

i.e. this:

("binop",
	("number", "5"),
	("*"),
	("number", "1")
)

becomes:

("number", "5")
```

-	In this class we will optionally perform optimization after parsing but before interpreting. Our optimizer takes a parse tree as input and returns a (simpler) parse tree as output.
	-	We could modify the tree in place but for us returning a new tree is fine.

-	Currently the optimizer is not recursive, so can't optimize e.g. `a \* 1 \* 1`.

### Rebuilding the Parse Tree

1.	Recursive calls
2.	Look for patterns.
3.	Done

```python
def optimize(tree): # Expression trees only
    etype = tree[0]
    if etype == "binop":
        # Fix this code so that it handles a + ( 5 * 0 )
        # recursively! QUIZ!
        a = optimize(tree[1])
        op = tree[2]
        b = optimize(tree[3])
        if op == "*" and b == ("number","1"):
            return a
        elif op == "*" and b == ("number","0"):
            return ("number","0")
        elif op == "+" and b == ("number","0"):
            return a
    return ("binop", a, op, b) # return optimized tree, not original
```

### Bending the Rules

-	Optimization is improving performance without sacrificing correctness.
-	However, in ["Evolutionary Program Repair"](http://genprog.cs.virginia.edu/) use genetic programming to "optimize" a program and alter its semantics to *improve* its correctness, i.e. removing bugs.
-	With creativity the same concepts of e.g. altering parse trees can be used in many contexts, like above.

### Wrap up

-	Lexing
	-	Regular expressions
	-	Finite state machines
-	Parsing
	-	Context Free Grammars, CFG (matching parentheses).
	-	Used Dynamic Programming and memoized Parse States
-	Optimizing
	-	Must retain meaning.
-	Interpreting.
	-	Walks AST recursively.
	-	HTML interpreter calls graphics engine and JavaScript interpreter.
-	Debugging
	-	Gain confidence.

## Unit 7 - The Final unit

### The List

-   A **language** is a set of strings
-   **Regular expressions**: concise notation for specifying some sets of strings (**regular languages**).
-   **Finite State Machines**: pictorial representations and way to implement regular expressions (deterministic or not).
    -   epsilon-transitions or more than one edge means it is non-deterministic.
    -   not a problem: can convert NFA to DFA.
-  **Context-Free Grammars**: concise notation for specifying some sets of strings (context-free languages).
    -   Set of re-write rules.
    -   NonTerminal -> Terminal Nonterminals.
    -   Terminals are the same as tokens, trying to match.
    -   CFGs can match balanced parantheses, this is impossible in regular languages.
-   **Memoization**, also called **Dynamic Programming**: keep previous results in a chart to save computation.
-   **Parsing**: determine if a list of tokens is in the language of a CFG. If so, produce a **parse tree**.
-   **Lexing**: break a big string up into a list of tokens (words).
    -   Specified using regular expressions.
-   **Type**: A type is a set of values and associated safe operations.
    -   Sets of values: Number, string, list.
    -   Operations: `+, -, /, len()`.
-   **Semantics**, i.e. **meaning**: a program may have type errors (or other **exceptions**) or it may produce a value.
-   **Optimization**: replace a program with another that has the *same semantics* (but uses fewer resources).
    -   `x * 1 === x`
    -   `x / x !== 1`
-   **Interpretation**: recursive walk over the (optimized) parse tree. The  meaning of a program is computer from the meanings of its subexpressions.
    -   Typically tracks **state* in **environments**.
    -   Environments are often chained together, particularly when you make function calls.
-   **Web browser**
    -   Lex and parse HTML, treating JS as a special token.
    -   HTML interpreter calls JS interpreter, which itself returns a string.
        -   JS interpreter calls `document.write()`.
    -   HTML interpreter calls graphics library to display words.

### Regular expressions

-   There is a regular expression for `a^N`: it's `a+`.
-   There isn't a regular expression for `a^N b^N`, because this involves memory / context / counting. Same as balancing parantheses.

### Context-Free Grammars

-   A context-free grammar (CFG) can capture `a^N b^N`. It looks like this:

        S -> aSb
        S ->

### Security

-   **Shrinking the trusted computing base**.
-   For any software minimize the components within it that needs to be trusted.
    -   Minimize the number of ways in which disaster may ensue.
-   An instance of the **halting problem**: if I could look at any piece of code and determine whether it was malicious or not this is equivalent to solving the halting problem.
    -   Discussed earlier how this is provably impossible to solve.

### Parsing states

```
S -> aSb
S -> \epsilon
S -> c

Input: acb

What parsing states are in chart[2]?
```

-   `S -> <dot> a S b` is in `chart[0] from 0`, so no.
-   `S -> a <dot> S b` is in `chart[1] from 0`, so no.
-   `S -> <dot>` is in `chart[1] from 1`, so no.
-   `S -> c <dot>` is in `chart[2] from 1`, so yes.
-   `S -> a S <dot> b` is in `chart[2] from 0`, so yes.
    -   note that the `from` is not `1`. `from 1` means that there is one hidden input not shown in this rule, whereas we can see all the input here.

### Interpretation and Evaluation

-   Interpreting doesn't always produce a value or an error.
    -   It can loop forever!
    -   But if it does return yes it always returns either a value or an error.

### Optimization

-   Given `optimization_OK(f, g)`, which compares a function before-and-after optimization and tells you if it's a safe optimization.
-   We can implement `optimization_OK` so that it returns a safe answer for optimization in all cases - just never optimize!
-   We cannot implement an `optimization_OK` that works precisely in all cases - it is undecidable like the Halting Problem.
    -   If we can solve `optimization_OK` in all cases then we could compare any `optimization_OK` itself to an infinite loop `def loops()`, and hence we'd have solved the Halting Problem.
-   `optimization_OK` is commutative; `O(f,g) == O(g,f)`

### What next?

-   Wes Weimer recommends...
    -   **Philosophy** until you've covered epistemology, free will, logic, the philosophy of science, and "what it is like to be a bat."
    -   **Cognitive psychology**, until you've covered perception, consciousness, and the Flynn effect.
    -   **Speech** and **Rhetoric** until you've covered persuasion.
    -   **Anthropology** and **Gender studies** until you've covered Mead and Freeman and have a better feel for which behaviours are socially constructed and which may be essential.
    -   **Statistics** until you can avoid being fooled.
    -   **Religion** and **Ethics** until you've covered the relatonshopi between unhappiness and unrealised desires.
    -   **Phyiscs** and **Engineering** until you can explain how a microphone, radio and speaker all work.
    -   **Government** until you have an opinion about legislating morality and the relative importance of freedom and equality.
    -   **History** until you are n ot condemed to repeat the mistakes of the past.
    -   **Life** until you are happy. They say ignorance is bliss but they are wrong all but finitely often.
-   !!AI hahaha.

## References

### Unit 1

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
