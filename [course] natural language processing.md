# Natural Language Processing

Columbia University, via Coursera

(There are excellent readings assigned to the class. They're either implicitly or explicitly inlined into the respective lecture, to save typing stuff out twice).

In order to use pandoc run:

        pandoc \[course\]\ natural\ language\ processing.md -o pdf/nlp.pdf --include-in-header=latex.template

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

## Week 2 - The Language Modeling Problem

### Introduction to the Language Modeling Problem (Part 1)

-   We have some finite vocabulary, i.e.

$V = \{the, a, man telescope, Beckham, two, ...\}$

-   We have countably infinite set of strings:

$V^+ = \{"the\:STOP", "a\:STOP", "the\:fan\:STOP", ...\}$



