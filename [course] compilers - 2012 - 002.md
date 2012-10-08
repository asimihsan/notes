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
-	Then editing, i.e. **optimization**. Retrict usage of some resource(s).
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
	-	EC sections 4.1-4.4
	-	EC
	-	CPTT
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