# Head First Object-Oriented Design and Analysis

## Appendix 2 - Objectville

-	UML stands for **Unified Modeling Language**.
-	UML helps you communicate the structure of your application to other developers, customers, and managers.
-	A **class diagram** gives you an overview of your class, including its methods and variables.
	-	Class name on top.
	-	Then instance variables (default, private).
	-	Then methods (default public).

-	**Inheritance** is when one class extends another class to reuse or build upon the inherited class's behaviour.
-	In inheritance, the class being inherited from is called the **superclass**; the class that is doing the inheritance is called the **subclass**.
-	A subclass gets all the behaviour of its superclass automatically.
-	A subclass can **override** its superclass's behaviour to change how a method works.

-	**Polymorphism** is when a subclass "stands in" for its superclass.
-	Polymorphism allows your applications to be more flexible, and less resistant to change.

-	**Encapsulation** is when you separate or hide one part of your code from the rest of your code.
-	The simplest form of encapsulation is when you make the variables of your classes private, and only expose that data through methods on the class.
-	You can also encapsulate groups of data, or even behaviour, to control how they are accessed.

## Chapter 1 - Well-Designed Apps Rock

-	What is great software?
	-	Customer-friendly programmer
		-	**Do what the customer wants**.
		-	Even if the customer thinks of new use-cases the software doesn't break or give unexpected results.
	-	Object-oriented programmer
		-	No duplicate code.
		-	Each object controls its own behaviour.
		-	**Well-designed**, **well-coded*, and easy to **maintain**, **reuse**, and **extend**.
	-	Design-guru progammar
		-	Use tried-and-tested design patterns and principles.
		-	Keep objects loosely coupled.
		-	Code is open for extension, but closed for modification.

-	Three easy steps.
	1.	Make sure your software does **what the customer wants it to do**.
		-	**Requirements analysis**.
		-	An incorrect well-designed app is still incorrect.
	2.	Apply basic OO principles to **add flexibility**.
		-	Find duplicate code, use OO programming techniques.
	3.	Strive for a **maintainable, reusable design**.
		-	Once you have a goods OOP app, it's time to apply patterns and principles.

-	Don't use `String` where you'd actually want to use an `enum`, i.e. a restricted set of values.
-	Requirements often change. It should be possible to reflect these changes in your UML class diagrams (and other diagrams), rather than only being able to express them in the code.
-	Try to have basic functionality down before spending a lot of time applying OO design, patterns, and principles.
	-	Functionaltiy informs design. How you want it to work will affect how the app is designed.
	-	!!AI be agile not waterfall.

-	So now we have `Guitar` and `Inventory`, and `Inventory.search(guitar)` returns a `List<Guitar>`.
-	First: what should `Inventory.search()` do? Use a **textual description** of the problem you're trying to solve to make sure that **your design lines up** with the intended **functionality** of your application.
	-	Client specifies general properties of a guitar.
	-	Search looks through the inventory.
	-	Each guitar is compared to the specifications.
	-	Return a list of matching guitars to the client.

-	Well-designed objects hate being used for something that isn't its true purpose.
-	The `Guitar` object is being used to do `search`, and it's quite unhappy. Clients aren't actually providing a proper `Guitar` object.
-	**Objects should do what their names indicate**.
	-	`Jet`'s `takeOff()`, they don't `takeTicket()`.
-	**Each object should represent a single concept**.
-	**Unused properties are a dead giveaway**.
	-	If you rarely specify a property, what does the object have it?
	-	Would there be a better object to use with just a subset of those properties?

-	In our case, **encapsulation** is useful
	-	(it doesn't just mean make all member variables private!)
	-	We can keep the generic properties of a guitar separate from the Guitar object itself.
	-	Guitar then just has a variable pointing to a new object type that stores all its properties.
	-	`GuitarSpec` class with all properties.
