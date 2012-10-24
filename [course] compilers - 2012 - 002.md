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

## Readings notes

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

## General notes