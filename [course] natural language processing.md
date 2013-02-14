# Natural Language Processing

Columbia University, via Coursera

## Readings policy

There are excellent readings assigned to the class. They're explicitly inlined into the respective lecture, to save typing stuff out twice.

Other readings (papers, textbooks, other courses) are explicitly inlined as well.

## Rendering

In order to use pandoc run (need to include custom LaTeX packages for some symbols):

        pandoc \[course\]\ natural\ language\ processing.md -o pdf/nlp.pdf --include-in-header=latex.template

or, for Markdown + LaTex to HTML + MathJax output:

        pandoc \[course\]\ natural\ language\ processing.md -o pdf/nlp.html --include-in-header=latex.template --mathjax

and, for the ultimate experience, after `pip install watchdog`:

        watchmedo shell-command --patterns="*.md" --ignore-directories --recursive --command='pandoc \[course\]\ natural\ language\ processing.md -o pdf/nlp.html --include-in-header=latetemplate --mathjax' .

## Week 1 - Introduction to Natural Language Processing

### Introduction (Part 1)

-   What is NLP?
    -   Computers using natural language as input and/or output.
    -   NLU: understanding, input
    -   NLG: generation, output.

Tasks

-   Oldest task: **machine translation**. Convert between two languages.
-   **Information extraction**
    -   Text as input, structure of key content as output.
    -   e.g. job posting into industry, position, location, company, salary.
    -   Complex searches ("jobs in Boston paying XXX").
    -   Statistical queries ("how has jobs changed in IT changed over time?")
-   **Text summarization**
    -   Condense one or many documents into a summary.
    -   [*Columbia Newsblaster*](http://newsblaster.cs.columbia.edu/) is an example.
-   **Dialogue systems**
    -   Humans can interact with a computer to ask questions and achieve tasks.

Basic NLP problems

-   **Tagging**
    -   Map strings to tagged sequences (each word is lexed and tagged with an appropriate label).
    -   **Part-of-speech tagging**: noun, verb, preposition, ...
        -   Profits (N) soared (V) at (P) Boeing (N)
    -   **Named Entity Recognition**: companies, locations, people
        -   Profits (NA) soared (NA) at (NA) Boeing (C)

-   **Parsing**
    -   e.g. "Boeing is located in Seattle" into a parse tree.

### Introduction (Part 2)

Why is NLP hard?

-   **Ambiguity**
    -   "At last, a computer that understands you like your mother"; three intrepretations at the *syntactic* level.
    -   But also occurs at an *acoustic* level: "like your" sounds like "lie cured".
        -   One is *more likely* than the other, but without this information difficult to tell.
    -   At *semantic* level, words often have more than one meaning. Need context to disambiguate.
        -   "I saw her duck with a telescope".
    -   At *discourse* (multi-clause) level.
        -   "Alice says they've built a computer that understands you like your mother"
        -   If you start a sentence saying "but she...", who is she referring to?

What will this course be about

-   **NLP subproblems**: tagging, parsing, disambiguation.
-   **Machine learning techniques**: probabilistic CFGs, HMMs, EM algorithm, log-linear models.
-   **Applications**: information extraction, machine translation, natural language interfaces.

Syllabus

-   Language modelling, smoothed estimation
-   Tagging, hidden Markov models
-   Statistical parsing
-   Machine translation
-   Log-linear models, discriminative methods
-   Semi-supervised and unsupervised learning for NLP

## Week 1 - The Language Modeling Problem

### Introduction to the Language Modeling Problem (Part 1)

-   We have some finite vocabulary, i.e.

$$V = \{the, a, man telescope, Beckham, two, ...\}$$

-   We have countably infinite set of strings, which are the set of possible sentences in the language:

$$V^+ = \{"the\:STOP", "a\:STOP", "the\:fan\:STOP", ...\}$$

-   STOP is a stop symbol at the end of a sentence. Convenient later on.
-   Sentences don't have to make sense, just every sequence of words.
-   Also a sentence could just be {"STOP"}, empty.

-   We have a *training sample* of example sentences in English.
    -   Sentences from the New York Times in the last 10 years.
    -   Sentences from a large set of web pages.
    -   In the 1990's 20 million words common, by the end of the 90's 1 billion words common.
    -   Nowadays 100's of billions of words.

-   With this training sample we want to "learn" a probabiliy distribution p, i.e. p is a function that satisfies:

$$\sum_{x \in V^+} p(x) = 1, \quad p(x) \ge 0 \; \forall \; x \in V^+$$

-   For any sentence x in language, p(x) >= 0.
-   If we sum over all sentences x in language, p(x) sums to 1.
-   A good language model assigns high probabilities to likely sentences in English (the fan saw Beckham STOP), low probabilities to unlikely sentences in English (Beckham fan saw the STOP)

### Introduction to the Language Modeling Problem (Part 2)

-   But...why do we want to do this?!
    -   **Speech recognition** was original motivation; related problems are optical character recognition and handwriting recognition.
    -   Input: sound wave time series.
    -   Preprocess: split into relatively short time periods, e.g. 10ms.
    -   For each frame do a Fourier transform, get energies of frequencies.
    -   Problem is to output recognised speech, sequence of words.
    -   Main course notes: it's useful to have prior probabilities so that if we can choose between alternatives we can ask "which is most likely?".  
        -   "recognise speech" vs "wreck a nice beach"
    -   The estimation techniques developed for this problem will be very useful for other problems in NLP.

-   Naive method of language modelling
    -   We have N training sentences.
    -   For any sentence $x_1, ..., x_n$, define $c(x_1, ..., x_n)$ as the number of times the sentences is seen in our training data.
    -   Naive estimate:

$$p(x_1, \ldots, x_n) = \frac{c(x_1, \ldots, x_n)}{N}$$

-   This is a valid, well-formed language model (p(x) sums to 1, they're all >= 1).
-   However, they'll assign a probabiliy of 0 to any unseen sentences; no ability to generalise to new sentences.
-   How can we build language models that generalise beyond the test sentences?

### Markov Processes (Part 1)

-   Markov Processes
    -   Consider a sequence of random variables $X_1, X_2, \ldots, X_n$.
    -   Each random variable can take any value in a finite set V.
    -   For now assume n is fixed, e.g. = 100. Every sequence is the same length.
    -   Our goal: model the joint probability distribution of the values of these n variables:

$$P(X_1 = x_1, X_2 = x_2, \ldots, X_n = x_n)$$

-   This is huge: for vocabulary V, number of sequences of length n is $|V|^n$.

-   First-Order Markov Processes
-   Going to use the chain rule of probabilities to decompose the expression into a product of expressions.
-   For two expressions, this rule is:

$$P(A,B) = P(A) \times P(B|A)$$
$$P(A,B,C) = P(A) \times P(B|A) \times P(C|A,B)$$

-   Hence:

$$P(X_1 = x_1, X_2 = x_2) = P(X_1 = x_1) \times P(X_2 = x_2 | X_1 = x_1)$$
$$P(X_1 = x_1, X_2 = x_2, X_3 = x_3) = ... P(X_3 = x_3 | P(X_2 = x_2, X_1 = x_1)$$

-   This kind of decomposition is *exact*: this is always true, and no assumptions are involved.
-   Hence the general decomposition:

$$P(X_1 = x_1, X_2 = x_2, \ldots, X_n = x_n)$$
$$=P(X_1 = x_1) \prod_{i=2}^{n} P(X_i = x_i\;|\;X_1 = x_1, \dots, X_{i-1} = x_{i-1})$$

-   Continuing on, with first-order Markov assumption:

$$= P(X_1 = x_1) \prod_{i=2}^{n} P(X_i = x_i\;|\; X_{i-1} = x_{i-1})$$

-   The first-order Markov assumption: for any $i \in {2, \dots, n}$, for any $x_1, \dots, x_n$:

$$P(X_i=x_i|X_1=x_1, \ldots, X_{i-1} = x_{i-1}) = P(X_i=x_i | X_{i-1} = x_{i-1})$$

-   Random variable at position i depends on just the previous value, on the variable at position (i-1).
    -   $X_i$ is conditionally independent of all the other random variables once you condition on $X_{i-1}$.

