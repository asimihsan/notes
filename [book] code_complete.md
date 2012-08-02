## Requirements

### Specific functional requirements

- Are all the inputs to the system specified, including their source, accuracy, range of values, and frequency?
- Are all the outputs from the system specified, including their destination, accuracy, range of values, frequency, and format?
- Are all output formats specified for web pages, reports, and so on?
- Are all the external hardware and software interfaces specified?
- Are all external communication interfaces specified, including handshaking, error-checking, and communication protocols?
- Are all the tasks the user wants to perform specified?
- Is the data used in each task and the data resulting from each task specified?

### Specific non-functional (quality) requirements

- Is the expected response time, from the user’s point of view, specified for all necessary operations?
- Are other timing considerations pecified, such as processing time, data-transfer rate, and system throughput?
- Is the level of security specified?
- Is the reliability specified, including the consequences of software failure, the vital information that needs to be protected from failure, and the strategy for error detection and recovery?
- Is maximum memory specified?
- Is the maximum storage specified?
- Is the maintainability of the system specified, including its ability to adapt changes in specific functionality, changes in the operating environment, and changes in its interfaces with other software?
- Is the definition of success included? Of failures?

### Requirements quality

- Are the requirements written in the user’s language? Do the users think so?
- Does each requirement avoid conflicts with other requirements?
- Are acceptable trade-offs between competing attributes specified - for example, between robustness and correctness?
- Do the requirements avoid specifying the design?
- Are the requirements at a fairly consistent level of detail? Should any requirement be specified in more detail? Should any requirement be specified in less detail?
- Are the requirements clear enough to be turned over to an independent group for construction and still be understood?
- Is each item relevant to the problem and its solution? Can each item be traced to its origin in the problem environment?
- Is each requirement testable? Will it be possible for independent testing to determine whether each requirements has been satisfied?
- Are all possible changes to the requirements specified, including the likelihood of each change?

### Requirements completeness

- Where information isn’t available before development begins, are the areas of incompleteness specified?
- Are the requirements complete in the sense that if the product satisfies every requirements, it will be acceptable?
- Are you comfortable with all the requirements? Have you eliminated requirements that are impossible to implement and included just to appease your customer or your boss?

## Architecture

### Specific topics

- Is the overall organization of the program clear, including a good architectural overview and justification?
- Are major building blocks well defined, including their areas of responsibility and their interfaces to other building blocks?
- Are all the functions listed in the requirements covered sensibly, by neither too many nor too few building blocks?
- Are the most critical classes described and justified?
- Is the data design described and justified?
- Is the database organization and content specified?
- Are all the key business rules identified and their impact on the system described?
- Is a strategy for the user interface design described?
- Is the user interface modularized so that changes in it won’t affect the rest of the program?
- Is a strategy for handling I/O described and justified?
- Are resource-use estimated and a strategy for resource management described and justified?
- Are the architecture’s security requirements described?
- Does the architecture set space and speed budgets for each class, subsystem , or functionality area?
- Does the architecture describe how scalability will be achieved?
- Does the architecture address interoperability?
- Is a strategy for internationalization/localization described?
- Is a coherent error-handling strategy provided?
- Is the approach to fault tolerance defined (if any is needed)?
- Has technical feasibility of all parts of the system been established?
- Is an approach to overengineering specified?
- Are necessary build vs. buy decisions included?
- Does the architecture describe how reused code will be made to conform to other architectural objectives?
- Is the architecture designed to accommodate likely changes?
- Does the architecture describe how reused code will be made to conform to other architectural objectives?

### General quality

- Does the architecture account for all the requirements?
- Is any part over- or under-architected? Are expectations in this area set out explicitly?
- Does the whole architecture hang together conceptually?
- Is the top-level design independent of the machine and language that will be used to implement it?
- Are the motivations for all major decisions provided?
- Are you, as a programmer who will implement the system, comfortable with the architecture?

### Upstream Prerequisites

- Have you identified the kind of software project you’re working on and tailored you approach appropriately?
- Are the requirements sufficiently well-defined and stable enough to begin construction (see the requirements checklist for details)?
- Is the architecture sufficiently well defined to begin construction (see the architecture checklist for details)?
- Have other risks unique to your particular project been addressed, such that construction is not exposed to more risk than necessary?

### Key points

- The overarching goal of preparing for construction is risk reduction. Be sure your preparation activities are reducing risks, not increasing them.
- If you want to develop high-quality software, attention to quality must be part of the software-development process from the beginning to the end. Attention to quality at the beginning has a greater influence on product quality than attention at the end.
- Part of a programmer’s job is to educate bosses and coworkers about the software-development process, including the importance of adequate preparation before programming begins.
- The kind of project you’re working on significantly affects construction prerequisites - many projects should be highly iterative, and some should be more sequential.
- If a good problem definition hasn’t been specified, you might be solving the wrong problem during construction.
- If a good requirements works hasn’t been done, you might have missed important details of the problem. Requirements changes cost 20 to 100 times as much in the stages following construction as they do earlier, so be sure the requirements are right before you start programming.
- If a good architectural design hasn’t been done, you might be solving the right problem in the wrong way during construction. The cost of architectural changes increases as more code is written for the wrong architecture, so be sure the architecture is right too.
- Understand what approach has been taken to the construction prerequisites on your project and choose your construction approach accordingly.

## Design in construction

### Design practices

- Have you iterated, selecting the best of several attempts rather than the first attempt?
- Have you tried decomposing the system in several different ways to see which way will work best?
- Have you approached the design problem both from the top down and from the bottom up?
- Have you prototyped risky or unfamiliar parts of the system, creating the absolute minimum of throwaway code needed to answer specific questions?
- Has your design been reviewed, formally or informally, by others?
- Have you driven the design to the point that its implementation seems obvious?
- Have you captured your design work using an appropriate technique such as a Wiki, email, flipcharts, digital camera, UML, CRC cards, or comments in the code itself?

### Design goals

- Does the design adequately address issues that were identified and deferred at the architectural level?
- Is the design stratified into layers?
- Are you satisfied with the way the program has been decomposed into subsystems, packages, and classes?
- Are you satisfied with the way the classes have been decomposed into routines?
- Are classes designed for minimal interaction with each other?
- Are classes and subsystems designed so that you can use them in other systems?
- Will the program be easy to maintain?
- Is the design lean? Are all of its parts strictly necessary?
- Does that design use standard techniques and avoid, hard-to-understand elements?
- Overall, does the design help minimize both accidental and essential complexity?

### Key points

- Software’s Primary Technical Imperative is managing complexity. This is accomplished primarily through a design focus on simplicity.
- Simplicity is achieved in two general ways: minimizing the amount of essential complexity that anyone’s brain has to deal with at any one time and keeping accidental complexity from proliferating needlessly.
- Design is heuristic. Dogmatic adherence to any single methodology hurts creativity and hurts your programs.
- Good design is iterative; the more design possibilities you try, the better your final design will be.
- Information hiding is a particular valuable concept. Asking, “What should I hide?” settles many difficult design issues.
- Lots of useful, interesting information on design is available outside this book. The perspectives presented here are just the tip of the iceberg.

## Class quality

### Abstract data types

- Does the class have a central purpose?
- Is the class well named, and does its name describe its central purpose?
- Does the class’s interface present a consistent abstraction?
- Does the class’s interface make obvious how you should use the class?
- Is the class’s interface abstract enough that you don’t have to think about how its services are implemented? Can you treat the class as a black box?
- Are the class’s services complete enough that other classes don’t have to meddle with its internal data?
- Has unrelated information been moved out of the class?
- Have you through about subdividing the class into component classes, and have you subdivided it as much as you can?
- Are you preserving the integrity of the class’s interface as you modify the class?

### Encapsulation

- Does the class minimize accessibility to its members?
- Does the class avoid exposing member data?
- Does the class hide its implementation details from other classes as much as the programming language permits?
- Does the class avoid making assumptions about its users, including its derived classes?
- Is the class independent of other classes? Is it loosely coupled?

### Inheritance

- Is inheritance used only to model “is a” relationships?
- Does the class documentation describe the inheritance strategy?
- Do derived classes adhere to the Liskov Substitution Principle?
- Do derived classes avoid “overriding” non-overridable routines?
- Are common interfaces, data, and behaviour as high as possible in the inheritance tree?
- Are inheritance trees fairly shallow?
- Are all data members in the base class private rather than protected?

### Other implementation issues

- Does the class contain about seven data members or fewer?
- Does the class minimize direct and indirect routine calls to other classes?
- Doe the class collaborate with other classes only to the extend absolutely necessary?
- Is all member data initialized in the constructor?
- Is the class designed to be used as deep copies rather than shallow copies unless there’s a measured reason to create shallow copies?

### Language-specific issues

- Have you investigated language-specific issues for classes in your specific programming language?

## High-quality routines

### Big-picture issues

- Is the reason for creating the routine sufficient?
- Have all parts of the routine that would benefit from being put into routines of their own been put into routines of their own?
- Is the routine’s name a strong, clear verb-plus-object name for a procedure or a description of the return value for a function?
- Does the routine’s name describe everything the routine does?
- Have you established naming conventions for common operations?
- Does the routing have strong, functional cohesion - doing one and only one thing and doing it well?
- Do the routines have loose coupling - are the routine’s connections to other routines small, intimate, visible, and flexible?
- Is the length of the routine determined naturally by its function and logic, rather than by an artificial coding standard?

### Parameter-passing issues

- Does the routine’s parameter list, taken as a whole, present a consistent interface abstraction?
- Are the routine’s parameters in sensible order, including matching the order of parameters in similar routines?
- Are interface assumptions documented?
- Does the routine have seven or fewer parameters?
- Is each input parameter used?
- Is each output parameter used?
- Does the routine avoid using input parameters as working variables?
- If the routine is a function, does it return a valid value under all possible circumstances?

### Key points

- The most important reason to create a routine is to improve the intellectual manageability of a program, and you can create a routine for many other good reasons. Saving space is a minor reason; improved readability, reliability, and modifiability are better reasons.
- Sometimes the operation that most benefits from being put into a routine of its own is a simple one.
- The name of a routine is an indication of its quality. If the name is bad and it’s accurate, the routine might be poorly designed. If the name is bad and it’s inaccurate, it’s not telling you what the program does. Either way, a bad name means that the program needs to be changed.
- Functions should be used only when the primary purpose of the function is to return a specific value described by the function’s name.
- Careful programmers use macro routines and inline routines with care, and only as a last resort.

## Defensive programming

### General

- Does the routine protect itself from bad input data?
- Have you used assertions to document assumptions, including preconditions and postconditions?
- Have assertions been used only to document conditions that should never occur?
- Does the architecture or high-level design specify a specific set of error handling techniques?
- Does the architecture or high-level design specify whether error handling should favor robustness or correctness?
- Have barricades been created to contain the damaging effect of errors and reduce the amount of code that has to be concerned about error processing?
- Have debugging aids been used in the code?
- Has information hiding been used to contain the effects of changes so that they won’t affect code outside the routine or class that’s changed?
- Have debugging aids been installed in such a way that they can be activated or deactivated without a great deal of fuss?
- Is the amount of defensive programming code appropriate - neither too much nor too little?
- Have you used offensive programming techniques to make errors difficult to overlook during development?

### Exceptions

- Has your project defined a standardized approach to exception handling?
- Have you considered alternatives to using an exception?
- Is the error handled locally rather than throwing a non-local exception if possible?
- Does the code avoid throwing exceptions in constructors and destructors?
- Are all exceptions at the appropriate levels of abstraction for the routines that throw them?
- Does each exception include all relevant exception background information?
- Is the code free of empty catch blocks? (Or if an empty catch block truly is appropriate, is it documented?)

### Security issues

- Does the code that checks for bad input data check for attempted buffer overflows, SQL injection, HTML injection, integer overflows, and other malicious inputs?
- Are all error-return codes checked?
- Are all exceptions caught?
- Do error messages avoid providing information that would help an attacker break into the system?

### Key points

- Production code should handle errors in a more sophisticated way than “garbage in, garbage out”.
- Defensive programming techniques make errors easier to find, easier to fix, and less damaging to production code.
- Assertions can help detect errors early, especially in large systems, high-reliability systems, and fast-changed code bases.
- The decision about how to handle bad inputs is a key error-handling decision, and a key high-level design decision.
- Exceptions provide a means of handling errors that operates in a different dimension from the normal flow of the code. They are a valuable addition to the programmer’s toolkit when used with care, and should be weighed against other error-processing techniques.
- Constraints that apply to the production system do not necessarily apply to the development version. You can use that to your advantage, adding code to the development version that helps to flush out errors quickly.

## The pseudocode programming process

- Have you checked that the prerequisites have been satisfied?
- Have you defined the problem that the class will solve?
- Is the high level design clear enough to give the class and each of its routines a good name?
- Have you through about how to test the class and each of its routines?
- Have you thought about efficiency mainly in terms of stable interfaces and reusable implementations, or in terms of meeting resource and speed budgets?
- Have you checked the standard libraries and other code libraries for applicable routines or components?
- Have you checked reference books for helpful algorithms?
- Have you designed each routine using detailed pseudocode?
- Have you mentally checked the pseudocode? Is it each to understand?
- Have you paid attention to warnings that would send you back to design (use of global data, operations that seem better suited to another class or another routine, and so on)?
- Did you translate the pseudocode to code accurately?
- Did you apply the PPP recursively, breaking routines into smaller routines when needed?
- Did you document the assumptions as you made them?
- Did you remove comments that turned out to be redundant?
- Have you chosen the best of several iterations, rather than merely stopping after your first iteration?
- Do you thoroughly understand your code? Is it easy to understand?

### Key points

- Constructing classes and constructing routines tends to be an iterative process. Insights gained while constructing specific routines tend to ripple back through the class’s design.
- Writing good pseudocode calls for using understandable English, avoiding features specific to a single programming language, and writing at hthe level of intent - describing what the design does rather than how it will do it.
- The Pseudocode Programming Process is a useful tool for detailed design and makes coding easy. Pseudocode translates directly into comments, ensuring that the comments are accurate and useful.
- Don’t settle for the first design that you think of. Iterate through multiple approached in pseudocode and pick the best approach before you begin writing code.
- Check your work at each step and encourage others to check it too. That way, you’ll catch mistakes at the least expensive level, when you’ve invested the least amount of effort.

## General considerations in using data

### Initializing variables

- Does each routine check input parameters for validity?
- Does the code declare variables close to where they’re first used?
- Does the code initialize variables as they’re declared, if possible?
- Does the code initialize variables close to where they’re first used, if it isn’t possible to declare and initialize them at the same time?
- Are counters and accumulators initialized properly and, if necessary, reinitialized each time they are used?
- Are variables reinitialized properly in code that’s executed repeatedly?
- Does the code compile with no warnings from the compiler?
- If your language uses implicit declarations, have you compensated for the problems they cause?

### Other general issues in using data

- Do all variables have the smallest scope possible?
- Are references to variables as close together as possible - both from each reference to a variable to the next and in total live time?
- Do control structures correspond to the data types?
- Are all the declared variables being used?
- Are all variables bound at appropriate times, that is, striking a conscious balance between the flexibility of late binding and the increased complexity associated with late binding?
- Does each variable have one and only one purpose?
- Is each variable’s meaning explicit, with no hidden meanings?

### Key points

- Data initialization is prone to errors, so use the initialization techniques described in this chapter to avoid the problems caused by unexpected initial values.
- Minimize the scope of each variable. Keep references to it close together. Keep it local to a routine or class. Avoid global data.
- Keep statements that work with the same variables as close together as possible.
- Early binding tends to limit flexibility, but minimize complexity. Late binding tends to increase flexibility, but at the price of increased complexity.
- Use each variable for one and only one purpose.

