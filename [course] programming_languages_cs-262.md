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