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