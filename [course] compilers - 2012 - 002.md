# Compilers - 2012 - 002

(via Coursera)

## Lecture notes

### 01-01: Introduction

-	Interpreters are online, just run program directly.
-	Compilers are offline, preprocess program into executable.
-	FORTRAN I first compile, 1954 - 1957. 1958 had 50% adoption.
	-	Lexical analysis. (syntactic)
	-	Parsing. (syntactic)
	-	Semantic analysis. (types, scopes)
	-	Optimization.
	-	Code generation.

### 01-02: Structure of a Compiler

-	First step: recognize words.
	-	**Lexical analysis**. Divide program into **tokens**.
-	Next step: understand the sentence.
	-	**Parsing**. Group into higher-level constructs.
-	Then understand the meaning. Very hard!
	-	Compilers do limited **semantic analysis**, too hard otherwise.
		-	Variable bindings wrt scope.
		-	Type mismatching.
-	Then editing, i.e. **optimization**. Restrict usage of some resource(s).
	-	Run faster.
	-	Use less memory.
	-	Power.
	-	Network messages.
	-	Database accesses.
-	Finally **codegen**, code generation. Assembly.
-	Compared to FORTRAN, modern compilers:
	-	Have very small lexing and parsing stages.
	-	Larger semantic analysis stage.
	-	Much larger optimization stage, dominant stage.
	-	Much smaller codegen stage.
	
### 01-03: The Economy of Programming Languages

-	Many programming languages, why?
	-	*Distinct application domains.*
		-	Scientific computing, e.g. FORTRAN.
			-	Good FP.
			-	Good arrays.
			-	Parallelism.
		-	Business applications, e.g. SQL.
			-	Persistance.
			-	Report generat	ion.
			-	Data analysis.
		-	Systems programming, e.g. C/C++.
			-	Control of resources.
			-	Real time constraints.
-	Why are there new programming languages?
	-	*Programmer training is the dominant cost of a language.*
	-	Widely used languages are slow to change - many users!
	-	Easy to start a new language - no users!
	-	Productivity > training cost => switch.
	-	So languages adopted to fill a void, get work done.
	-	New languages tend to resemble old ones.
-	What is a good programming language?
	-	No universally accepted metric.
				
	
## 02-01: Cool Overview

-	Classroom Object Oriented Language.
-	Designed to be implementable in a short time.
-	COOL -> MIPS assembly language.
-	main class *Main*, which has procedure *main*.
-	compile using *coolc*. (`coolc <filename.cl>`)
-	Run .s file using *spim*. (`spim <filename.s>`)

First:

		class Main {
			i : IO <- new IO;
			main():Int { { i.out_string("Hello world!\n"); 1; };
		};

Later, no need for 1 and dont care about return type:

		class Main {
			i : IO <- new IO;
			main():Object { { i.out_string("Hello world!\n"); };
		};
		
No need to allocate:

		class Main inherits IO {
			main():Object { { self.out_string("Hello world!\n"); };
		};

But no need to explicitly name self:

		class Main inherits IO {
			main():Object { { out_string("Hello world!\n"); };
		};

## 02-02: Cool Example II

Converting string to integer from stdin:

		class Main inherits A2I {
		
			main() : Object {
				(new IO).out_string(i2a(a2i(new IO)+1).in_string())).concat("\n"));
			};
		};

-	`let` defines a local variable.
-	`<-` for assignment.
-	`while (condition) loop { .. } pool;`
-	`=` is comparison.

## 02-03: Cool Example III

Complex!

## 03-01: Lexical Analysis

-	Divide strings into tokens.
	-	In English e.g. noun, verb
	-	In programming language e.g. identifier, keywords, integer, whitespace.
-	**Lexical analysis** classify substrings according to their role. Communicate tokens to the parser.
	-	Output of LA (a token) is <Class, String>.
-	Some strings are the only ones in their own class, e.g. '(', ')', ';'.

## 03-02: Lexical Analysis Examples

-	LA always requires lookahead, but we want to minimize and bound it.

## 03-03: Regular langauges

-	**Lexical structure** = set of token classes.
-	What set of strings in a token class?
	-	Use regular languages.
	-	Usually use regular expressions.
-	**Regular expressions**
	-	"c" = {"c"}. One string is a one string language.
	-	$$\epsilon$$ = {""}. Empty string. Not an empty set.
	-	Union. $$A + B = {a | a \in A} U {b | b \in B}$$.
		-	Is commutative.
	-	Concatenation (cross product). $$AB = {ab | a \in A ^ b \in B}$$.
	-	Iteration, Kleen closure. $$A^* = \bigcup_{i \geq 0} A^i$$. A^i = A … A (i times), A^0 = epsilon.
	
-	**Regular expressions over Sigma** are the smallest set of expressions.
	-	R = epsilon | 'c' (each c in alphabet ($$\Sigma$$)) | R + R | RR | R*.
	-	This is a **grammar**.
-	Examples of RLs.

---

$\Sigma = {0, 1}$

$1^* = \bigcup_{i\geq0}1^i = \epsilon + 1 + 11 + …$

---

$(1 + 0)1 = \{ab | a \in 1 + 0 \wedge b \in 1\}$
$= \{11, 01\}$

---

$0^* + 1^* = \{0^i | i \geq 0\} U \{1^i | i \geq 0\}$ 

---

$(0+1)^* = \bigcup_{i \geq 0}(0 + 1)^i$
$= "", 0+1, (0+1)(0+1), …, (0+1), … i times, …(0 + 1)$

all strings of 0's and 1's. In fact this is the alphabet, so all the strings of the alphabet as many times as you like.

$=\Sigma^*$.

---

-	RLs are not equations. They express languages, i.e sets of strings.
	-	Hence:
	
(0+1)* . 1 . (0+1)* = (0+1)* . (10+11+1) . (0+1)*

-	LHS => make sure there is a 1 in the middle, preceded or followed by any any combination of alphabet.
-	RHS guarantees the same!

## 03-04: Formal languages

-	Regular expressions are an example of a formal language.
-	FL has an alphabet $\Sigma$, a set of characters. A **language** over $\Sigma$ is a set of strings of characters drawn from$$\Sigma$.
-	e.g. alphabet = ASCII characters, language = C programs.
-	*Meaning function L* maps syntax to semantics.
	-	$L(e) = M$. e is language, e.g. RE.  M is set of strings.
	-	L maps from expressions (e.g. epsilon) to sets (e.g. {""}).
	-	L: Exp -> Sets Strings
	-	Recursive. L(A + B) = L(A) U L(B), etc.
-	Why use a meaning function?
	-	Clearly delineate syntax from semantics.
	-	Allows us to consider that notation is a separate issue.
		-	Consider arabic numbers vs. roman numerals.
			-	Meaning is same, but arithmetic in roman numerals is painful.
	-	Expression -> meaning is not 1:1.
		-	Syntax -> semantics is many:1.
		-	Never 1:many! Means ambigious output.
		-	Consider below, all are the same:

$0^*$

$0 + 0^*$

$\epsilon + 00^*$

$\epsilon + 0 + 0^*$

## 03-05: Lexical Specifications

-	Conditional
	-	'i' . 'f' = "if"
	-	"if" + "then" + "else"
-	Integer, nonempty.
	-	digit = "0" + … + "9"
	-	digit+ = digit digit^*
-	Identifier
	-	letter = [a-zA-Z]
	-	letter (letter + digit)*
-	Whitespace
	-	' ' + '\n' + '\t'
-	Email address
	-	Username, domains.
	-	letter+ '@' letter+ '.' letter+
	-	(surely not valid?)
-	Optional => (RE)?, is + epsilon.

## 03-06: DeduceIt Demo

-	Conclusion, rule, justification.

## 04-01: Lexical Specification

-	Summary of RE notation
	-	*At least one*: A^+ = A . A*
	-	*Union*: A | B = A + B
	-	*Option*: A? = A + \epsilon
	-	*Range*: 'a' + 'b' + … = 'z' = [a-z]
	-	*Excluded range*: Complement of [a-z] = [^a-z]
	
-	Hypothetical specification for a predicate.
	-	s in set L( R ).
	- 	i.e. string s in language( R ). Latter is set of strings.
	-	Not enough! We need to *partition* input into words.
	
1.	First, write regexp for lexemes or each token class.
	-	Integer = digit+
	-	Whitespace - ' ' + '\n' + '\t'
	-	etc.
2.	Construct R, matching all lexemes for all tokens
	-	R = Integer + Whitespace + …
	-	R = R_1 + R_2 + …
3.	For every prefix in input check if it is in L( R ).
4.	If it is then we know the prefix is one of the constituent regexps, i.e. token classes.
5.	Remove that prefix and continue checking.

-	**Maximal munch**. Longest prefix match.
-	What if more than one token matches? e.g. an Identifier called if.

$x_1 … x_i \in L( R ), R = R_1 + … + r_N$

$x_1, …, x_i \in L(R_j)$

$x_1, …, x_i \in L(R_k)$

e.g.

$'if' \in L(Keywords)$ and $L(Identifiers)$

-    **Priority ordering**. Choose the one listed first. Keywords before Identifiers.
-    What is no rule matches?

$x_1, …, x_i \notin L( R )$

-    **Error token class**. regexp for all strings not in the lexical specification. Put it last.

## 04-02: Finite Automata

-    Implementation of regular expressions.
-    FA consists of:
    -    Input alphabat $\Sigma$.
    -    A finite set of states $S$.
    -    A start state $n$.
    -    A set of accepting states $F \subseteq S$.
    -    A set of transitions $state \overrightarrow{input} state$.
-    Transition (read)
    -    $s_1 \overrightarrow{a} s_2$.
-    If end of input and in accepting state then accept.
-    Terminates in any state other than accepting state, reject.
-    Gets stuck, no transition, reject.
-    **Configuration of FA**: state it is in and input it is processing (input pointer). 
-    **Language of a FA**: set of accepted strings.
-   $\epsilon$-move. Transition without consuming input (without moving input pointer).
-   **Deterministic Finite Automata** (DFA)
    -    One transition per input per state.
    -    No $\epsilon$-moves.
-    **Non-deterministic Finite Automata** (NFA)
    -    Multiplate transitions for one input in given state.
    -    Can have $\epsilon$-moves.
    -    As we can transform multiple states into epsilon moves it's epsilon moves that tell us if an FA is NFA or not.
-    A DFA takes only one path through state graph, NFA can choose.
-    An NFA accepts if some choices lead to accepting state.
-    **Configuration of a NFA**: the set of states it could be in and the input it's processing.
-    NFAs and DFAs recognise same set of languages, regular languages.
-    DFAs faster (no choices)
-    NFAs are generally smaller.

## 04-03: Regular Expressions into NFAs

-    Lexical specification -> Regular expressions.
-    Regular expressions -> NFA.
-    NFA -> DFA.
-    DFA -> Table-driven implementation of DFA.
-    For epsilon or input A, simple.
    -    s_1: start state.
    -    input: epsilon or a, goes to s_2, accepting state.
-    *Concatenation*, AB.
    -    Final state of A has an epsilon transition to start state of B.
-    *Union*, A + B
    -    Make a new start state with two epsilon transitions. One to A, one to B.
    -    Make a new accepting state with two epsilon transitions, from accepting states of A and B.
-    *Kleene closure*, A*
    -    Complex.
    -    New start state. Epsilon edge to A.
    -    Epsilon edges from accept of A to start and new accept state.
    -    Epsilon edge from new start state to new accept state.
    
## 04-04: NFA to DFA

-    **epsilon-closure of a state**: set of states that can be reached on *recursive* epsilon transitions and the state itself.
    -    Keep following epsilons.
-    NFA may have many states at any time.
-    How many different states?
    -    N states in total.
    -    |S| <= N.
    -    $2^N - 1$ non-empty subsets of N states.
    -    **Finite state of possible configurations**. So in principle DFA can simulate NFA.
-    NFA characterisation:

states: $S$.
start state: $s \in S$.
final states: $F \subseteq S$.
$a(X) = {y | x \in X ^ x \overrightarrow{a} y}$

(i.e. for a set of states X and input a what are all states that can be reached).

$\epsilon$-clos

-    DFA characterisation:

states: subsets of S (except empty set)
start state: epsilon-clos of start state of NFA.
final states: ${X | X \cap F \neq 0}$. (can be more than one).

transition from X to Y given a if:

$Y = \epsilon-clos(a(X))$

- So for given input you can reach the epsilon closure of the ending state.

- !!AI Pretty tricky! Do on paper, watch end of lecture for example.

## 04-05: Implementing Finite Automata

-    DFA. **Table of input vs. state**. Value is the next state.
    -    Downside is that many duplicate rows.
-    Instead **one-dimensional column, pointer** to possible moves as a row. Can share moves amongst states.
    -    Could be 2^N - 1 states in DFA for an NFA with N states.
    -    But pointer dereferencing takes time.
-    Or could implement **NFA in table**.
    -    States are rows, columns are alphabet (e.g. 0, 1, and epsilon).
    -    But values are sets of states, i.e. the configuration is multiple states. Much slower.

## 05-01: Introduction to parsing

-	Regular languages are weakest formal language.
-	Consider the language of all balanced parentheses:

$\{(^i )^i | i \geq 0\}$

-	Applies also to nested if/then.
-	Regular expressions cannot handle all balanced parentheses or nested if/then.
-	Regular languages can only count "mod k", where k is finite number of states. Not arbitrary.
-	Lexer: string of characters -> string of tokens
-	Parser: string of tokens -> parse tree.
	-	Parse tree may be implicit.

## 05-02: Context-Free Grammars

-	We need:
	-	Language for *describing valid strings of tokens*.
	-	Method for *distinguishing valid from invalid* strings of tokens.
-	CFGs are natural notation for describing recursive structures.
-	A CFG consists of:
	-	A set of terminals, T
	-	A set of non-terminals, N
	-	A start symbol, S ($S \in N$).
	-	A set of productions, where production is $X \to Y_1 ... Y_N, X \in N, Y_i \in N \bigcup T \bigcup \epsilon$.

e.g. two productions

$S \to (S)$
$S \to \epsilon$

This implies:

$N = \{S\}$
$T = \{(, )\}$

-	Productions can be read as rules.
	-	Begin with a string with only the start symbol S.
	-	Replace any non-terminal X by the right-hand side of some production $X \to Y_1 ... Y_n$.
	-	Repeat until no non-terminals left.
	-	*One step of a context-free derivation*

One step of a context-free derivation reads as:

$X_1 ... X_i X X_{i+1} ... X_N \to X_1 ... X_i Y_1 ... Y_k X_{i+1} ... X_N$

$S \to \alpha_0 \overrightarrow{*} \alpha_n$ (in 0 or more steps, where alpha is some string).

-	Language L(G) of a context-free grammar G:

$\{a_1 ... a_b | \forall_i a_i \in T\} ^ S \overrightarrow{*} a_1 ... a_n\}$

-	i.e. set of all strings that I can drive just from the start symbol.
-	Terminal symbols do not have rules for replacing them, permanent. e.g. tokens in language.

## 05-03: Derivations

-	**Derivation**: a sequence of productions.
-	Can draw a derivation as a tree. Add the result as children.
	-	Obviously root is start symbol, interior nodes are non-terminals, leaves are terminals.
	-	In-order traversal of the leaves is the original input.
-	**Left-most derivation**: at each step replace left-most non-terminal.
-	**Right-most derivation**: at each step replace right-most non-terminal.
-	Left-most and right-most derivation have the same parse tree.
-	Many kinds of derivations.
-	We don't just care if string s in L(G). We need a parse tree for s!

## 05-04: Ambiguity

-	**Ambiguous grammar**: grammar has more than one parse tree for some string.
	-	Equivalently, more than one left-most or right-most derivation for some string.
-	Dealing with ambiguity.
	-	Most direct is to re-write grammar.

E -> E' + E | E'
E' -> id * E' | id | (E) * E' | (E)

-	Notice that E controls plus, E' controls multiplication.
-	Notice higher precedence towards bottom of parse tree.
-	E is a Kleene closure over plus, zero or more. Final E becomes E'.
-	E' is a Kleene closure over multiplication, zero or more. Final E' becomes id.
-	Notice we use (E), not (E'). We can put pluses in brackets.

-	How to match if/then/else

``
E -> MIF
   | UIF // matched if or unmatched if
MIF -> if E then MIF else MIF
	 | OTHER
UIF -> if E then E
	 | if E then MIF else UIF
``

-	Instead of rewriting grammer, tools can use precedence and associativity to do it for you.
	-	bison does this, e.g.

E -> E + E | int

becomes

%left +
E -> E + E | int

and

E -> E + E | E * E | int

becomes:

%left +
%left *
E -> E + E | E * E | int

## 06-01: Error handling

-	Error types:
	-	*Lexical*, e.g. a $ b.  Detected by lexer.
	-	*Syntax*, e.g. a *% b. (Lexically correct). Detected by parser
	-	*Semantic*, e.g. int x; y = x(3). (Syntax correct). Detected by type checker.
	-	*Correctness*. Detected by user.
-	**Panic mode**
	-	Simplest, most popular.
	-	On error discard tokens until one with a clear role is found. Then continue.
	-	**Synchronizing tokens**: statement or expression terminations.
	-	e.g.: (1 + + 2) + 3
	-	On second plus discard input until it finds the next integer, then continue.
	-	In bison use a terminal "error" to descibe how much input to skip.

E -> int | E + E | (E) | error int | ( error )

-	**Error productions**
	-	Specify known common mistakes in the grammar.
	-	e.g. You write 5x instead of 5 * x
	-	Add production E -> ... | E E
	-	Disadvantage
		-	Complicates the grammar.

-	**Error correction** (not common any more)
	-	Find a correct "nearby" program.
	-	Try token insertions and deletions. Minimize edit distance.
	-	Exhaustive search.
	-	Disadvantages:
		-	Hard.
		-	Slows down parsing.
		-	Nearby doesn't necessarily imply "intended".
	-	e.g. PL/C. Always parses to running program.
	-	But this was developed in the 70's
		-	Slow recompilation cycle, even one day.
		-	Want to find as many errors in one cycle as possible.

## 06-02: Abstract Syntax Trees

-	Review:
	-	Parser traces derivation of a sequence of tokens.
	-	But later parts of compiler needs structural representation.
	-	**Abstract syntax trees** (AST). Like a parse tree but ignores some details.
-	e.g.: E -> int | ( E ) | E + E
	-	5 + (2 + 3).
	-	Parse tree has too much informaion: parentheses, single-successor nodes.

## 06-03: Recursive Descent Parsing

-	Top-down, left to right.
-	Terminals seen in order of appearance in token stream.
-	Try production rules in order, e.g.

E -> T | T + E
T -> int | int * T | ( E )

( 5 )

-	For start symbol E we try T then T + E. On failure may have to do back-tracking.
-	Notice while generating that when we generate non-terminal don't know if we're on the right track.
-	Once you generate a terminal you can check the input at the input pointer to see if it's right. If not, try another production.
-	Don't be too smart. Recursive descent parser tries all productions in order, so you should too.

## 06-04: Recursive Descent Algorithm

-	Let *TOKEN* be type of a TOKEN, i.e. INT, OPEN, CLOSE, PLUS, or TIMES.
-	Let global *next* be pointer to next input token.
-	Define boolean fuctions.
	-	`bool term(TOKEN tok) { return *next++ == tok; }`
		-	Is the token currently pointed to? Also increment next.
	-	`bool S_n() { ... }`
		-	nth production of S. Does particular production match input?
	-	`bool S() { ... }`
		-	Try all productions of S. Do any of all productions match input?
-	For production E -> T
	-	`bool E_1() { return T(); }`
-	For production E -> T + E
	-	`bool E_2() { return T() && term(PLUS) && E(); }`
	-	Notice short-circuited AND.
	-	Notice each bool function increments input pointer.
	-	Notice it's called E_2, second production of E.
-	For all productions of E with backtracking

```
bool E() {
	TOKEN *save = next;
	return (next = save, E_1())
		|| (next = save, E_2());
}
```
-	Notice short-circuited OR. If first condition true don't evaluate second.
-	Notice we restore next after failing an OR condition.
-	Notice on failing all productions of E we don't restore anything, because we're passing the error back up to a higher production.

-	Functions for non-terminal T
	-	T -> int
		-	`bool T_1() { return term(INT); }`
	-	T -> int * T
		-	`bool T_2() { return term(INT) && term(TIMES) && T(); }`
	-	T -> ( E )
		-	`bool T_3() { return term(OPEN) && E() && term(CLOSE); }`

```
bool T() {
	TOKEN *save = next;
	return (next = save, T_1())
		|| (next = save, T_2())
		|| (next = save, T_3());
}
```

-	To start parser.
	-	Initialize next to first token
	-	Invoke start symbol, E().

## 06-04-1: Recursive Descent Limitations

-	From before try to parse int * int.
-	We parse as E -> E_1 -> T -> int, but input not exhausted, so reject input string.
-	What happened?! String is definitely in language of grammar.
-	Problem: there is no backtracking once we have found a matching production; ideally we'd try all productions, and then maximal munch.
-	If a production for non-terminal X succeeds cannot backtrack to try a different production for X.
-	General recursive-descent algorithms do however support such "full" backtracking.
-	Presented RA algorithm is not general but easy to implement by hand.
-	Sufficient for grammars where for any non-terminal at most one production can succeed.

## 06-05: Left Recursion

-	Consider S -> S a.

``
bool S_1() { return S() && term(a); }
bool S() { return S_1(); }
``

-	S() goes into an infinite loop.
-	**Left-recursive grammar**: has some non-terminal S such that S ->+ S alpha for some alpha.
	-	One or more productions that refer to same non-terminal.
	-	There is always a non-terminal in the derivation, can't finish.
-	Recursive descent does not work with left-recursive grammars.
-	Consider: `S -> S alpha | beta`
	-	S generates all strings starting with one beta followed by any number of alphas.
	-	But it does so right to left.
-	Can rewrite using right-recursion:

S -> beta S'
S' -> alpha S' | epsilon

e.g.

S -> B S' -> B A S' -> B A A S' -> ... -> B A ... A S' -> B A ... A

-	So in general take one left-recursive production S and rewrite into right-recursive productions S and S'.
-	But above is not the most general form of left-recursion, e.g.

S -> A alpha | beta
A -> S beta

-	Above is also left-recursive.
-	!!AI don't get it, can't do the quiz question. Look at EC later.
    -    EC p100 is pretty good.
    -    Quiz includes question about eliminating indirect left-recursion, so midterm will have it too.
-	Summary of recursive descent (general form not presented here)
	-	simple and general parsing strategy.
	-	left-recursion must first be eliminated, but can be automatically eliminated.
	-	Used in gcc.

## 07-01: Predictive Parsing

-	Like recursive descent but parser can predict what production to use.
	-	By looking at next few tokens, no backtracking, always right.
-	Accept LL(k) grammars.
	-	First L: left-to-right scan.
	-	Second L: left-most derivation.
	-	k tokens of lookahead.
		-	In practice k always 1.
-	Review, in recursive descent:
	-	At each step many choices of production.
	-	Backtrack to undo bad choices.
-	In LL(1)
	-	Only one choice of production.
-	Recall our favourite grammar:

E -> T + E | T
T -> int | int * T | ( E )

-	Hard to predict:
	-	For T two predictions start with int.
	-	For E not clear how to predict, both start with T.
-	Need to **left-factor** the grammar.
	-	Eliminate the common prefixes of multiple productions for one non-terminal.

E -> T X
X -> + E | epsilon

T -> int Y | ( E )
Y -> * T | epsilon

-	Use left-factored grammar to generate an LL(1) parsing table.
	-	Rows: leftmost non-terminal, i.e. current non-terminal.
	-	Columns: next input token.
	-	Value: RHS of production to use.
-	How to use the table:
	-	For the leftmost non-terminal S.
	-	Look at next input token a.
	-	Choose production shown at [S, a].
-	A stack records frontier of parse tree.
	-	Non-terminals that have yet to be expanded.
	-	Terminals that have yet to be matched against input.
	-	Top of stack = leftmost pending terminal or non-terminal.
-	Reject on error state.
-	Accept on end of input and empty stack.
-	Dollar sign ($) is special end-of-input symbol, put it on the end of the input and in the stack.

``
initialize stack = <S $> and next
repeat
	case stack of
		<X, rest>:	if 	 T[X, *next] = Y_1 ... Y_n
					then stack <- <Y_1 ... Y_n rest>;
					else error();
		<t, rest>:	if 	 t == *next++
					then stack <- <rest>;
					else error();
until stack == < >
``

-	Note: after processing symbol X or t we pop it off the stack. In case of X after popping we push on its children such that first (leftmost) child is top of stack.
-	When doing this take your LL(1) parse table and draw a new table with columns "stack", "input", "action". Stack starts as "S $", input is "input $".
-	14:23: worked example.
-	Quiz at the end is useful, but would like to see parse tree too. Worked example at 14:23 has this.

## 07-02: First Sets

-	Consider leftmost non-terminal A, production $A \to $\alpha$, next input token t.
-	T[A, t] = $\alpha$ in two cases.
-	If $\alpha \to* t \beta$.
	-	alpha can derive t in the first position in zero or more moves.
	-	We say that that $t \in First(\alpha)$.
		-	t is one of the terminals that $\alpha$ can produce in the first position.
-	If $A \to \alpha$ and $\alpha \to * \epsilon$ and $S \to * \Beta A t \delta$.
	-	Useful if stack has A, input t, and *A cannot derive t*.
	-	$\alpha$ cannot derive t. t is not in $First(\alpha)$.
	-	Only option is to get rid of A by deriving $\epsilon$.
	-	We say that $t \in Follow(A)$.
	-	Must be a derivation where t comes immediately after A.
-	Definition

$First(X) = \{ t | X \to * t \alpha} \bigcup \{ \epsilon | X \to * \epsilon \}$

-	All terminals t that can be derived by alpha in the first position.
-	Also need to keep track of X deriving $\epsilon$.
-	Trying to figure out all the terminals in the First set.

1. $First(t) = \{ t \}$.

2. $\epsilon \in First(X)$ if
	-	$X \to \epsilon$, or
	-	$X \to A_1 ... A_n$ and $\epsilon \in First(A_i)$ for $1 \leq i \leq n$.
		-	The entire RHS must derive to $\epsilon$, all the A_i. All A_i must be non-terminal.

3. $First(\alpha) \subseteq First(X)$ if $X \to A_1 ... A_n \alpha$.
	-	and $\epsilon \in First(A_i)$ for $1 \leq i \leq n$.
	-	All A_i goes to epsilon, i.e. X can go to alpha.

-	Recall our favourite grammar, left-factored:

E -> T X
X -> + E | epsilon

T -> ( E ) | int Y
Y -> * T | epsilon

First( + ) = { + }
First( * ) = { * }
First( ( ) = { ( }
First( ) ) = { ) }
First(int) = { int }

$First(E) \subseteq First(T)$
First(T) = { (, int}

-	Can T go to epsilon? If it can then First(X) also in First(E).
-	But no! T can't go to epsilon. So First(X) can never contribute to First(E).

Hence:

$First(E) = First(T)$.

First(X) = { +, epsilon }
First(Y) = { *, epsilon }

## 07-03: Follow sets

-    First sets for what is produced, Follow sets for where the symbol is used.

Follow(X) = { t | S ->* B X t d }

$Follow(X) = \{ t | S \to * \Beta X t \delta\}$

-    All t that immediately follow X in derivations.
-    Intuition:
    -    *If X -> A B then $First(B) \subseteq Follow(A)$.*
        -    Suppose that X -> A B ->* A t beta, implies that anything in the First of B is in the Follow of A.
    -    Also, *$Follow(X) \subseteq Follow(B)$.*
        -    Suppose on S -> X t. -> A B t.
        -    We say that the Follow of X is in the Follow of the last symbol, here B.
    -    If B ->* epsilon, $Follow(X) \subseteq Follow(A)$.
    -    If S is the start symbol then $ \in Follow(S). (end of input marker).

-    Algorithm
    1.    $ \in Follow(S).
    2.    First(beta) - { epsilon } \subseteq Follow(X)
        -    For each production A -> alpha X beta.
        -    epsilon never appears in Follow sets. Follow sets are always sets of terminals.
    3.    Follow(A) \subseteq Follow(X).
        -    For each production A -> alpha X beta where epsilon in First(beta).
        
-    Recall:

E -> T X
X -> + E | epsilon

T -> ( E ) | int Y
Y -> * T | epsilon

Follow(E)
-    = { $, … } (get this for free, always true)
-    Close paren must be in Follow(E) because it's a terminal following E in first production of T.
-    E is last symbol in X's first production, so Follow(X) in Follow(E).

Follow(X)
-    Last symbol in production of E, so Follow(E) in Follow(X).
-    Hence Follow(X) = Follow(E).

Now nothing else to learn about X or E, so Follow(E) is concluded, and hence Follow(X) is concluded.

Follow(E) = Follow(X) = { $, ) }

Follow(T):
-    Recall that First(X) = { +, epsilon } (from previous lecture).
-    First(X) \in Follow(T).
-    Follow(T) = { + , …} (don't put epsilon there because epsilon never in Follow sets).
-    As X can go to epsilon, it can disappear, so Follow(E) in Follow(T).
-    Hence Follow(T) = { +, $, ), …}
-    T is in rightmost spot of Y, so Follow(Y) in Follow(T).

Follow(Y)
-    Y appears in rightmost spot of T, so Follow(T) in Follow(Y).
-    So Follow(T) = Follow(Y).

And now we're done!

Follow(T) = Follow(Y) = { +, $, ) }

Now consider terminals:

Follow('(')
-    First(E) \in Follow( '(' ).
-    From first lecture First(E) \in First(T), and T never goes to epsilon, hence First(E) = First(T).
-    First(E) = First(T) = { (, int }
-    Hence Follow('(') = { (, int }
    -    Makes sense because only things that follow open paren is open paren and int.
    
Follow(')')
-    Right end of T, so Follow(T) in Follow(')').
-    Follow(T) = { +, $, ) }.
-    Hence Follow(')') = { +, $, ) }.

Follow('+')
-    First(E) in Follow('+').
-    First(E) = First(T) = { '(', int }
-    Hence Follow('+') = { '(', int }
-    If T went to epsilon we'd need to consider other rules, but it doesn't.

Follow('\*')
-    First(T) in Follow('\*')
-    First(T) = { '(', int }
-    Hence Follow('\*') = { '(', int }
-    If T went to epsilon we'd need to consider other rules, but it doesn't.

Follow(int)
-    First(Y) in Follow(int).
-    First(Y) = { '\*', epsilon }
-    Hence Follow(int) = { '\*', … }
-    But Y can go to epsilon!
-    Hence int could be right end of T's second production.
-    Hence Follow(T) in Follow(int)
-    Hence Follow(int) = { '\*', '+', $, ')' }

## 07-04: LL(1) Parsing Tables

-    Construct a parsing table T for CFG G.
-    For each production A -> \alpha in G do:
    -    For each terminal t \in First(\alpha) do:
        -    T[A, t] = \alpha.
    -    If \epsilon \in First(\alpha), for each t \in Follow(A) do:
        -    T[A, t] = \alpha.
        -    If we need to get rid of A.
    -    If \epsilon in First(\alpha) and $ \in Follow(A) do:
        -    T[A, $] = \alpha.

-    02:38: worked example, see paper. If it doesn't make sense watch again and work through.
-    Blank entry in parsing table is parsing error.

-    Consider:

S -> Sa | b

-    This is not an LL(1) grammar, it is left recursive.
-    First(S) = {b}.
-    Follow(s) = { $, a }
-    Small LL(1) table (draw it out).
-    Given non-terminal S and input b we have multiple moves: b and Sa.
-    If you build an LL(1) parsing table and some entry has more than one move in it then the CFG G is not LL(1).

-    Quick checks if grammar is not LL(1):
    -    We know that any grammar that is not left-factored will not be LL(1).
    -    Also not LL(1) is left recursive.
    -    Also if ambiguous.
-    However, other grammars are not LL(1) too.
-    Most programming language CFGs are not LL(1).
 
## 07-05: Bottom-Up Parsing

-    Bottom-up parsing is more general than top-down parsing.
    -    Just and efficient.
    -    Builds on top-down parsing.
    -    Preferred method.
-    Don't need left-factored grammars.
-    Revert to "natural" grammars.

E -> T + E | T
T -> int * T | int | ( E )

-  *Reduces* a string to the start symbol by inverting productions.
-    Consider:

int * int + int

-    Productions, read backwards, trace a rightmost derivation.
-    We parse downwards in *reductions*.
-    But read upwards it's a right-most derivation.

-    Important fact #1: **A bottom-up parser traces a rightmost derivation in reverse**.

## 07-06: Shift-Reduce Parsing

-    Let abw be a step of a bottom-up parse.
-    Assume the next reduction is by X -> b (replace b by X, remember we run productions backwards).
-    Then w is a string of terminals.
-    Why?
    -    aXw -> abw is a step in a right-most derivation. X must be the right-most non-terminal as we're operating on it. Hence w is a string of terminals.
    
-    Idea: Split string into substrings.
    -   if aXw, w is unexamined input.
    -    Left substring has terminals and non-terminals.
    -    Pipe separates the two.
    -    aX | w.
    
 -    Two kinds of moves, shift and reduce.
 -    Shift:
     -    Move pipe one place to the right.
     -    ABC | xyz => ABCx | yz.
-    Reduce:
    -    Apply an inverse production at the right end of the left string.
    -    If A -> xy is a production then:
    -    Cbxy | ijk => CbA | ijk
    
05:00: Example of shift-reduce on int * int + int.

-    Left-string can be implemented by a stack.
    -    Top of stack is the pipe.
    -    Shift pushes a terminal on the sack.
-    Reduce:
    -    pops symbols off of the stack (production RHS)
    -    pushes a non-terminal on the stack (production LHS).
    
-    **Shift-reduce conflict**: if it is legal to shift or reduce. (Almost expected, use precedence declarations to remove).
-    **Reduce-reduce conflict**: if it is legal to reduce by two different productions. (Bad!)

## 08-01: Handles

-	Review:
	-	Shift: move pipe operator by one.
	-	Reduce: apply inverse production to the right end of the left string.
	-	Left string can be implemented by stack.
		-	Top of the stack is the pipe.
	-	Shift pushes terminal onto the stack.
	-	Reduce:
		-	pops >= 0 symbols off stack (production RHS)
		-	pushes a non-terminal onto the stack (production LHS)
-	How to decide when to shift or reduce?
-	Example grammar:

	E -> T + E | T
	T -> int * T | int | ( E )

-	Consider step:

	int | * int + int

-	Could try reduce T -> int.
	-	Fatal mistake! Can't then reduce to start symbol E. No production that says "T *".
-	Intution: only reduce if result can still be reduced to start symbol.
-	Assume rightmost derivation:

	S ->* aXw -> abw

-	Remember we're going in reverse, reductions.
-	ab is a **handle** of abw.
-	A **handle** is a reduction that also allows further reductions back to the start symbol.
-	Only reduce at handles.

-	Important fact #2: **In shift-reduce parsing, handles appear only at the top of the stack, never inside.**
	-	Informal proof by induction on number of reduce moves.
	-	True initially, stack empty.
	-	Immediately after reducing a handle:
		-	We reduce to a non-terminal, handle on top of the stack, hence right-most non-terminal on top of the stack.
		-	Next handle must be to right of right-most non-terminal, because this is a right-most derivation.
		-	Sequence of shift moves reaches next handle.
-	Handles never to the left of the rightmost non-terminal.
	-	Shift-reduce moves sufficient; pipe never need move left.
-	Bottom-up parsing algorithms based on recognizing handles.

## 08-02: Recognizing Handles

-	Bad news:
	-	No known efficient algorithms.
-	Good news:
	-	Some good heuristics.
	-	On some CFGs the heuristics always guess correctly.
-	All CFGs $\subset$ Unambiguous CFGs $\subset$ LR(k) CFGs $\subset$ LALR(k) CFGs %\subset$ SLR(k) CFGs.
	-	LR(k) means left-to-right, rightmost derivation, k lookahead.
	-	SLR(k): simple left-to-right rightmost.
-	$\alpha$ is a **viable prefix** if there is an $\omega$ such that $\alpha | \omega$ is a state of a shift-reduce parser.
	-	alpha is the stack.
	-	omega is the rest of the input.
	-	Parser know about alpha.
	-	Parser knows about a little of omega due to lookahead but certainly not all of it.
-	What does this mean?
	-	Viable prefix does not extend past right end of the handle.
	-	It is a viable prefix because it is a prefix of the handle.
	-	As long as the parser has viable prefixes on the stack no parsing error has been detected.
-	Important fact #3 about bottom-up parsing: **For any grammar, the set of viable prefixes is a regular language**.
-	Going to show how to compute automata to accept viable prefixes.
-	An **item** is a production with a "." somewhere on the RHS.
-	The items for T -> ( E ) are:

	T -> .(E)
	T -> (.E)
	T -> (E.)
	T -> (E).

-	For X -> epsilon only X -> .
-	Items are often called **LR(0) items**.
-	Stack has only bits and pieces of the RHS of productions.
	-	Bits and pieces always *prefixes* of RHS of productions.

-	Consider:

	E -> T + E | T
	T -> int * T | int | ( E )

-	and input:
	
	( int )

-	Then `( E | )` is a state of a shift-reduce parse.
-	`(E` is a prefix of the RHS of `T -> (E)`.
	-	Will be reduced after next shift.
-	Item `T -> (E.)` says that so far we have seen `(E` of this production and hope to see `)`.

-	Stack is actually composed of prefixes of RHS's.

	Prefix_1 Prefix_2 ... Prefix_n

-	Let Prefix_i be prefix of RHS of X_i -> alpha_i.
	-	Prefix_i eventually reduces to X_i.
	-	Missing part of alpha_{i-1} starts with X_i.
	-	i.e. there is a X\_{i-1} -> Prefix\_{i-1} X_i Beta for some Beta.
-	Recursively, Prefix_{k+1} ... Prefix_n eventually reduces to the missing part of alpha_k.

-	Favourite grammar with `(int * int)`.
-	`(int * | int)` is a state of the shift-reduce parse.
-	`(` is prefix of the RHS of `T -> (E)`.
-	`epsilon` is prefix of RHS of `E -> T`.
-	`int *` is prefix of the RHS of `T -> int * T`.

-	The "stack of items" (bottom is the top of the stack):

	T -> (.E)
	E -> .T
	T -> int * . T

-	Says:
	-	We've seen `(` of `T -> (E)`.
	-	We've seen epsilon of `E -> T`.
	-	We've seen `int *` of `T -> int * T`.
	-	Notice each item's LHS becomes part of the RHS of the item below it on the stack.

-	Idea, to recognize viable prefixes:
	-	Recognize a sequence of partial RHS's of productions.
		-	Each partial RHS can eventually reduce to part of the missing suffix of its predecessor.

## 08-03: Recognizing Viable Prefixes

-	Algorithm.
	-	Should watch the video as explanation.

1.	Add a dummy production S' -> S to G.
2.	The NFA states are the items of G
	-	Including the extra production.
	-	Remember that we claim that the set of viable prefixes is a regular language, so can recognise using NFA.
	-	NFA(stack) = { yes, no } (viable prefix or not).
3.	For item E -> a.Xb ($E \to \alpha . X \beta$) add transition.
	-	E -> a.Xb ->X E -> aX.b
	-	Seen alpha on the stack, next input terminal or non-terminal.
	-   Shift.
4.	For item E -> a.Xb and production X -> y add
	-	E -> a.Xb ->e X -> .y
	-   Seen alpha, next input is non-terminal.
	-	(epsilon move).
	-	We only have partial RHS's of productions.
	-	It's possible that we see alpha but then see something that will *eventually* reduce to X.
5.	Every state is an accepting state.
6.	Start state is S' -> .S

S' -> E
E -> T + E | T
T -> int * T | int | (E)

-	Draw start state.

S' -> .E

-	See E on the stack, so draw ->E to:

S' -> E.

-	This is the state if you've read the entire input and finished parsing.
-	Then draw an epsilon move from S' -> .E to:

E -> .T

-	Then draw an epsilon move from S' -> .E to:

E -> .T+E

-	Notice this is using the power of an NFA, and not even left factored.
-	E -> .T ->T E -> T.
-	When the dot reaches all the way to the right-hand side we say that we've recognised a handle.

-	If we don't see a T then need to see something that reduces to T.
	-	E -> .T ->e -> T -> .int
	-	E -> .T ->e -> T -> .(E)
	-	E -> .T ->e -> T -> .int * T

-	For terminals nothing reduces to them, so you need to see the terminal in order to shift the dot.

## 08-04: Valid items

-	Can convert viable prefix NFA to DFA. !!AI watch lecture 04-04 again.
-	The states of the DFA are **canonical collections of LR(0) items**.
	-	The Dragon book gives another way of constructor LR(0) items.
-	Item X -> b.y is **valid** for viable prefix ab if:

	S' ->* aXw > abyw

	(by a right-most derivation)

-	After parsing ab, the valid items are the possible tops of the stack of items (?).

-	An item I is valid for a viable prefix a if the DFA recognizing viable prefixes terminates on input a in a state s containing I.
-	The items in s describe what the top of the item stack might be after reading input a.

-	An item is often valid for many prefixes.
-	e.g. item T -> (.E) is valid for prefixes:

		(
		((
		(((
		((((
		...

## 08-05: SLR Parsing

-	Define very weak bottom-up parsing algorithm called LR(0) parsing.
-	Assume:
	-	stack contains $\alpha$.
	-	Next input is t.
	-	DFA on input $\alpha$ terminates in state s.
-	Reduce by $X \to \beta$ if:
	-	s contains item $X \to \beta .$
-	Shift if:
	-	s contains item $X \to \beta . t \omega$
	-	Equivalent to saying s has transition labelled t.

-	LR(0) has a reduce/reduce conflict if:
	-	Any state has two reduce items, i.e.
	-	$X \to \beta .$ and $Y \to \omega .$
-	LR(0) has a shift/reduce conflict if:
	-	Any state has a reduce item and a shift item, i.e.
	-	$X \to \beta .$ and $Y \to \omega . t \delta$.

-	Example of DFA state with shift-reduce conflict:

		E -> T.
		E -> T. + E

-	First suggest reduce, second suggest shift, if the input is '+'.

-	SLR = "Simple LR".
-	SLR improves on LR(0) shift/reduce heuristics.
	-	Fewer states have conflicts.
-	Same assumptions as LR(0).
-	Reduce by $X \to \beta$ if:
	-	s contains item $X \to beta .$
	-	**new** $t \in Follow(X)$.
		-	(if t can't follow X it doesn't make sense to perform this reduction).
-	Shift if:
	-	s contains item $X \to \beta . t \omega$.
-	If there are any conflicts under these rules, the grammar is not SLR.

-	Take another look at shift-reduce conflict under LR(0):

		E -> T.
		E -> T. + E

-	Will only reduce on input '+' if '+' in Follow(E).
-	Follow(E) = { $, ')' }

-	Lots of grammar aren't SLR.
	-	including all ambiguous grammars.
-	We can parse more grammars by using precedence declarations.

-	Our favourite ambiguous grammar:

		E -> E + E | E * E | (E) | int

-	The DFA for the viable prefixes for this grammar contains a state with the following items, hence shift/reduce conflict:

		E -> E * E .
		E -> E . + E

-	Declaring "\* has a higher precedence than \+" resolves this conflict in favour of reducing.
-	These declaration don't define precedence; they define conflict resolutions.

-	SLR parsing algorithm.
	1.	Let M be DFA for viable prefixes of G.
	2.	Let `| x_1 ,... x_n $` be the initial configuration.
	3.	Repeat until configuration is `S | $`.
		-	Let `$\alpha | $\omega$` be current configuration.
		-	Run M on current stack $\alpha$.
		-	If M rejects $\alpha$, report parsing error.
			-	Stack $\alpha$ is not a viable prefix.
			-	Rule not needed, rejection below prevents bad stacks.
		-	If M accepts $\alpha$ with items I, let a be next input.
			-	Shift if `X -> b . a y` in I.
			-	Reduce if `X -> b .` in I and a in Follow(X).
			-	Report parsing error if neither applies.

## 08-06: SLR Parsing Example

-	!!AI just watch it!
-	Columns: Configuration, DFA Halt State, Action

##	08-07: SLR Improvements

-	Rerunning the viable prefixes automaton on the stack at each step is wasteful.
	-	Most of work is repeated.
-	Remember the state of the automaton on each prefix of the stack.
-	Change stack to contain pairs:

		< Symbol, DFA State >

-	Bottom of stack is `<any, start>`.
	-	`any` is any dummy symbol.
	-	`start` is the start state of the DFA.

-	Define `goto[i, A] = j` if state_i ->A state_j.
	-	goto is just the transition function of the DFA.
		-	One of the two parsing tables (the other one is the action table).

-	SLR parsing algorithm has four possible moves.
	-	Shift x
		-	Push `<a, x>` on the stack.
		-	a is current input.
		-	x is a DFA state.
	-	Reduce $X \to \alpha$
		-	As before.
	-	Accept.
	-	Error.	

-	For each state s_i and terminal a

	-	If s_i has item $X \to \alpha . a \beta$ and `goto[i, a] = j` then `action[i, a] = shift j`.
		-	State is s_i, next input is a.
		-	goto for state_i with input a is state j.
		-	Hence action on state i with input a is shift j; it's OK to shift.

	-	If s_i has item $X \to \alpha .$ and $a \in Follow(A)$ and $X \neq S'$ then `action[i, a] = reduce $X \to \alpha$`.
		-	S' is special new start symbol; don't do this if we're reducing to S'.

	-	If s_i has item $S' \to S .$ then `action[i, $] = accept`.

	-	Otherwise, `action[i, a] = error`.

-	Full algorithm

``
Let I = w$ be initial input
Let j = 0
Let DFA state 1 have item S' -> .S
Let stack = < dummy, 1>
repeat
	case action[top_state(stack), I[j]] of
		shift k: push <I[j++], k>
		reduce X -> A:
			pop |A| pairs,
			push <X, goto[top_state(stack), X]>
		accept: halt normally
		error: halt and report error
``

-	I is input array, indexed by j
-	Say first DFA state is 1.
-	pop |A| pairs mean pop number of pairs equal to A (?)

-	Note that we only use DFA staes and the input.
	-	We don't use stack symbols!
-	We still need the symbols for semantic actions.

-	Some common constructs are not SLR(1)
-	LR(1) is more powerful.
	-	Lookahed built into the items.
	-	LR(1) item is a pair: LR(0) item, and x lookahead.
	-	[T -> . int * T, $ ] means
		-	After seeing T -> int * T reduce if lookahead sees $.
	-	More accurate than just using follow sets.
	-	Actual parser will show you LALR(1) automaton.

## 08-08: SLR Examples

``
S -> Sa
S -> b
``

-	Is `b a*`
-	Left-recursive, but not a problem for LR(k) parsers.
-	First step: add new production:

``
S' -> S
S -> Sa
S -> b
``

-	Rather than build NFA and then using subset construction let's just build the DFA.
-	Start DFA state:

``
S' -> .S
``

-	Remember all NFA epsilon moves are due to not seeing a non-terminal on a stack but rather something that derives a non-terminal.
	-	epsilon moves to all the productions of S.
	-	We know subset production performs an epsilon closure of the start state of NFA to get the start states of DFA.
	-	Hence we know all the items in the start state of DFA:

``
S' -> .S
S -> .Sa
S -> .b
``

-	What symbols may we see on the stack?
	-	b
		- Next state is `S -> b`.
	-	S
		-	Next state has two items.
			-	`S' -> S.` (complete, dot all the way on the right)
			-	`S -> S.a` (not complete)
-	Last state `S -> Sa.` on input a.
-	Look for shift-reduce conflicts and reduce-reduce conflicts.
	-	Any two items that reduce on same start symbol?
	-	Any ambiguity between needing to shift and needing to reduce on an input? Remember Follow(X) rule.
-	Key state that may contain problems is:

``
S' -> S.
S -> S.a
``

-	On input a we may either reduce to S' or shift.
-	Will only reduce if a is in Follow(S').
-	Follow(S') = { $ }.
	-	Nothing can follow it, because it is the start symbol.
-    Dot all the way on the right => reduction.


Readings notes

-	CPTT: Compilers: Principles, Techniques, and Tools
-	EC: Engineering a Compiler
-	Read EC first, then CPTT.
-	Week 2 (Lexical Analysis and Finite Automata)
	-	CPTT sections 3.1, 3.3, 3.4, 3.6, 3.7, 3.8
	-	EC: Chapter 2 through Section 2.5.1, except 2.4.4
	
- - -

EC, lexical analysis and finite automata

-	**Recognizer**: program that identifies specific words in a stream of characters.
-	**Syntactic category**: each output from recognizer is classified according to grammatical usage.
-	**Microsyntax**: lexical structure of language.
	-	e.g. English groups alphabetic letters. Spaces terminate words.
	-	After English word identified use dictionary lookup to see if valid.
-	Typical programming language has **keywords**, reserved for particular syntactic purpose and cannot be used as an identifier.
-	Compiler writer starts with microsyntax specification, encodes into notation used by scanner generator.

Recognizing words

-	FSM states are circle, above arrow are letters that cause transition.
	-	Double-circle is recognized word.
	-	Else, move to an error state.	
-	**Finite automaton (FA)**: a formalism for recognizers that has:
	-	a *finite* set of states (S) and an error state s_e.
	-	an alphabet (big sigma), usually union of edge labels in transition diagram.
	-	a transition function $$\delta(s, c)$$ -> next state, s is state and c is character.
	-	a start state (s_0), and
	-	one or more accepting states (S_A), the double circles in a transition diagram.
-	Recognizer takes one transition per input character, run time is O(n), n is length of input string.
-	**Lexeme**: actual text for a word recognized by an FA. An actual instance of a syntactic category.
	-	113 is a specific unsigned integer; latter is lexeme.
-	Infinite sets, like set of integers, require cyclic transition diagrams.

Regular expressions

-	Set of words accepted by FA (F) forms a language L(F).
-	For any FA we can also describe L(F) using a **regular expression** (RE).
-	Zero or more instances is * operator, or *Kleene closure*.
-	RE is made up of three basic operations:
	-	*Alternation* (R | S).
	-	*Concatenation* (xy)
	-	*Closure* ($$R^*$$).
		-	*Finite closure* ($$R^i$$). One to i instances of R.
		-	*Postiive closure* ($$R^+$$). One or more instances of R. 
	- $$\epsilon$$ is empty string and is itself an RE.
-	**Complement operator**: notation ^c specific set $$(\Sigma - c)$$. High precedence than *, |, or $$^+$$.
-	**Escape sequence**: two or more characters that a scanner translates into another character, e.g. \n.
-	**Regular languages**: Any language that can be specified by an RE.
-	Programming languages vs. natural languages.
	-	In natural languages words require understanding of context to derive meaning.
	-	In programming languages words are almost always specified lexically.
-	REs are closed under concatenation, union, closure, and complement. e.g. RE_1 | RE_2 => RE.
-	**Complete FA**: an FA that explicitly includes all error transitions.
-	**e-transition**: A transition on the empty string $$\epsilon$$, that does not advance the input.
	-	Combine FAs.
-	**Nondeterministic FA**: An FA that allows transitions on the empty string, $$\epsilon$$, and states that have multiple transitions on the same character.
	-	Depends on future characters.
-	**Deterministic FA**: A DFA is an FA where the transition function $$\delta(s, a)$$ is single-values. DFAs do not allow $$\epsilon$$-transitions.
-	**Configuration of an NFA**: the set of concurrently active states of an NFA.
	-	On multi-values transition function NFA clones itself once per possibility.
	-	Always finite, but could be exponential.
-	To simulate an NFA, we need a DFA with a state for each configuration of the NFA.
-	**Powerset of N**: the set of all subsets of N, denotes $$2^N$$.


-	p46, figure 2.4: trivial NFAs for REs.
-	**Thompson's construction**: REs -> NFA.
	-	Use trivial NFAs in order consistent with precedence of operators.
-	**Subset construction**: NFA to DFA.
-	**Valid configuration**: configuration of an NFA that can be reached by some input string.
-	Subset construction example, p50-51.
-	(not in class) **Hopcroft's algorithm**: DFA to minimal DFA.

Table-driven scanners


	
- - - 


CPTT, lexical analysis and finite automata

- - -

	
-	Week 3 (Parsing)
	-	CPTT section 4.1-4.6, 4.8.1, 4.8.2
	-	EC sections 3.1-3.4
	-	CPTT
	
- - -

EC 3.1-3.4

-    **Parsing**: given a stream s of words and a grammar G, find a derivation in G that produces s.
-	**Context-free grammar**: for a language L its CFG defines the set of strings of symbols that are valid sentences in L.
-	**Sentence**: a string of symbols that can be derived from the rules of a grammar.
-	**Language defined by G**: the set of sentences that can be derived from G.
-	**Production**: a rule in a CFG.
-	**Nonterminal symbol**: a syntactic variable used in a grammar's productions.
-	**Terminal symbol**: a word that can occur in a sentence.
-	**Word**: a lexeme and its syntactic class. Words are repesented in a grammar by their syntactic category.
-	**Start symbol or goal symbol**: a nonterminal symbol that represents the set of all sentences in L(G).
-	**Derivation**: sequence of rewriting steps that begins with the grammer's start symbol and ends with a sentence in the language.
-	**Sequential form**: a string of symbols that occurs as one step in a valid derivation.
-	**Parse tree or syntax tree**: a graph that represents a derivation.
-	p89 is good diagram of derivation and corresponding parse tree.
-	**Rightmost derivation**: a derivation that rewrites, at each step, the rightmost nonterminal.
-	**Leftmost derivation**: a derivation that rewrites, at each step, the leftmost nonterminal.
-	Despite using rightmost or leftmost derivation the corresponding parse trees are identical.
-	**Ambiguity**: a grammar G is ambiguous if some sentence in L(G) has more than one rightmost (or leftmost) derivation.
	-	p91, if-then-else ambiguity example.
-	p93, figre 3.1: classis expression grammar for operator precedence, and p94 has an excample derivation and corresponding parse tree.
-	Classes of CFGs and their parsers.
	-	Arbitary CFGs take O(n^3) to parse, usually not used.
	-	LR(1) are a large subset of unambigous CFGs. Parsed buttom-up, linear left-to-right, looking ahead at most one symbol. Favourite.
	-	LL(1) are a subset of LR(1). Parsed top-down, linear left-to-right, looking ahead at most one symbol.
	-	Regular grammars (RGs) are CFGs that generate regular languages. Subset of LL(1). Equivalent to regexp's.
-	Why is top-down parsing efficient? A large subset of context-free grammers can be parsed without backtracking.

TOREAD from p97

- - - 

	
-	Week 4 (Semantic Analysis and Types)
	-	CPTT section 5.1-5.3, 6.3, 6.5
	-	EC sctions 4.1-4.4
-	Week 5 (Runtime Systems and Code Generation)
	-	CPTT section 6.2, 7.1-7.4, 8.1-8.3, 8.6
	-	EC chapter 5, sections 7.1-7.2
-	Week 6 (Optimization)
	-	CPTT section 8.5, 8.7, 9.1-9.4
	-	EC section 8.1-8.4, 8.6, 9.1-9.3
-	Week 7 (Advanced topics: Register allocation and Garbage Collection)
	-	CPTT sections 7.5-7.6, section 8.8
	-	EC sections 13.1-13.2, 13.4


## Assignment notes

-	Quiz 2
	-	Question 3
		-	When does a grammar not produce a regular language?
			-	Look for any notion of counting, which a NFA cannot do as it only has a finite number of states. Compare these two grammars:

					A -> (A( | epsilon
					A -> (A) | epsilon

			-	The first is a regular grammar; just pairs of open parens.
			-	The second is not a regular grammar; we're matching open parens with closing ones, hence we need to "count" how many open parens we have in order to close them.
	-	When looking for left-recursive grammars make sure the left-most token in some chain is a non-terminal, not a terminal, for production (even the ORs).
    -    For a CFG to encode operator precedence we need:
        -    Addition associates to the left.
        -    Multiplication binds more tightly than addition.
    -    Context-free => grammar requires no memory. Same as regular language?
    -    A NFA can determine parity, i.e. even or odd number of something, it can't count.
	

## General notes