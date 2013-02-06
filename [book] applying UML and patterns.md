# Applying UML and Patterns

## Chapter 1: Introduction

-	A critical ability in OO development is to skillfully **assign responsibilities to software objects**.
-	**Analysis**: investigation of problem and requirements.
	-	*Do the right thing*.
-	**Design**: conceptual solution that fulfills requirements, rather than its implementation.
	-	*Do the thing right*.

-	Object orientation emphasises representation of objects.
	-	e.g. planes.
	-	OO analysis => Plane, Flight, Pilot classes.
	-	OO design => plan has a tailNumber attribute, getFlightHistory method.

-	Short example, p43
	1.	**Define use cases**.
		-	Requirements analysis. Short stories.
		-	e.g. Player rolls two Dice, if they sum to 7 they win.
	2.	**Define a domain model**.
		-	Describe the domain from the perspective of objects.
		-	This is **conceptual**; not a description of software objects.
		-	Concepts, attributes, associations that are *noteworthy*.
		-	e.g. Player, Die, DiceGame.
		-	A Player Rolls a Die. A DiceGame includes two Die. A Player Plays a DiceGame.
	3.	**Assign object responsibilities, draw interaction diagrams**.
		-	UML sequence diagram.
		-	Instances of objects send messages to each other in sequence, get responses.
		-	Software object designs are inspired by the by the domain model, but are not direct 1:1 mappings of it.
		-	e.g. in the real world a Player rolls a Die, whereas here the DiceGame rolls the Die.
	4.	**Define design class diagrams**.
		-	Attributes and methods of classes.

-	Three ways to apply UML
	1.	UML as sketch, rough and often on whiteboards.
	2.	UML as blueprint. More detailed and often for code generation.
	3.	UML as programming language. Complete execution specification.

-	**Agile modelling** emphasises **UML as sketch**.

-	Classes are drawn in UML using a box, but there are two types of classes
	-	**Conceptual classes** aka **domain concepts**: domain-oriented.
	-	**Design classes**: specific or implementation perspective.

-	p53: recommended resources.

## Chapter 2: Iterative, Evolutionary, and Agile

-	**Unified Process* (UP)
	-	Iterative software development process.
	-	A refinement is the **Rational Unified Process** (RUP).
	-	UP encourages mixing practices with Extreme Programming (XP), Scrum, etc.
	-	e.g. XP's test-driven development, refactoring, continuous integration fit in.

-	**Iterative development**: development divided into short, fixed-length mini-projects called **iterations**.
	-	Output of each iteration is a tested, integrated, and executable *partial* system. However, not ready to deliver into production, but it is a production-grade subset of final system.
	-	As system grows with each iteration, this is *iterative and incremental development*.
	-	As we use feedback to adapt and evolve specifications and design, this is *iterative and evolutionary development*.
	-	Often only ready for production in e.g. 10 to 15 iterations.

-	Iterations tackle a subset of requirements quickly, including feedback from users, developers, and tests.
	-	Rather than *speculating* about correct requirements or design, feedback guides us.
	-	Build-feedback-adapt.
	-	Over time feedback and evolution leads towards the desired system, but early on the deltas are large.
	-	Ideal iteration length is between two to six weeks, but always fixed; slippage is illegal.
		-	Rather than slip you push out tasks and requirements to a future iteration.

-	Waterfall is failure-prone mostly because of the assumption that specifications are predictable and stable from the start.
-	But don't make the mistake that no up-front analysis is required.

-	e.g. a 20-iteration project.
	-	Before iteration 1
		-	High-level requirements, use cases and features, key non-functional requirements. (0.5d).
		-	Pick the to 10% requirements in terms of architectural significance, business value, and risk. This is a **requirements workshop**.
		-	For the next 1.5d do intensive, detailed analysis of the top 10%.
		-	Output: top 10% are deeply analysed, other 90% have high-level analysis.
		-	Then pick a subset of the top 10% for iteration 1.
	-	Iteration 1, three to four weeks.
		-	First two days, paired modelling and design using UML-ish on whiteboards.
		-	Then do coding, testing, integrating.
		-	One week before end see if we can meet targets. If not de-scope the iteration, push out requirements to a TODO list.
		-	Code freeze, demo to external stakeholders.
	-	Iterations 2-4 will implement the top 10%, and have detailed requirements for 80-90% of the whole. Each of this iterations involve a requirements workshop.
		-	Take into account what you learned from the last iteration(s).
		-	This requirements output will be much higher quality than with traditional waterfall.
		-	In UP terms this is the end of the **elaboration phase**.
		-	Need to estimate the time remaining, based on detailed requirements.
	-	Continue without requirements workshops.

-	UP emphasies both *risk-driven* and *client-driven* iterative planning.
	-	Requirements workshops should emphasise both architectural importance and risk and business value.
	-	Not having a solid architecture is a common high-risk.

-	p70: The Agile Principles.

-	**Agile Modelling**: the purpose is to *understand*, not to *document*. Sketching UML.
	-	Does not mean "avoid all modelling*.
	-	Model the high risk and important areas, don't exhaustively model everything upfront.
	-	Don't model alone, do it in pairs or triads.

-	p76: critical UP practices.
	-	high-risk, high-value in early iterations.
	-	continuously engage stakeholders and clients for feedback and requirements.
	-	build core architecture in early iterations.
	-	continuous integration: early, often, realistic.

-	UP phases:
	-	**Inception**: vision, business case, vague estimates.
		-	*Not* a waterfall requirements phase. Just enough investigation to make a yes/no decision to continue.
	-	**Elaboration**: iterative implementation of core, high-risk, high-business-value parts.
		-	*Not* a waterfall design phase. You actually implement here.
	-	**Construction**: iterative implementation of the remaining low-risk and easier parts.
	-	**Transition**: beta tests, deployment.

-	p82: UP has **practices** that output **artifacts**, but artifacts are optional.
-	p84: you know you don't understand iterative development if...
-	p86: recommended resources.