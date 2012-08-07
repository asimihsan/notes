## Online tutorials

- x 01: Your First iPhone Application (Apple)
- x 02: Your Second iOS App: Storyboards (Apple)
- x 04: iOS App Programming Guide (Apple)
- o 03: Your Third iOS App: iCloud
- x 22: Core Data Tutorial for iOS (Apple)
- o 27: Core Data Utility Tutorial (Apple)

- x 05: Cocoa Fundamentals Guide (Apple)
- x 06: View Controller Programming Guide (Apple)
- o 10: Table View Programming Guide (Apple)
- o 07: Event Handling Guide for iOS (Apple)
- o 08: View Programming Guide for iOS (Apple)
- o 09: View Controller Catalog for iOS (Apple)
- o 11: Design then Code (two tutorials on iOS apps)

- x 12: Networking Overview (Apple)
- x 13: Networking Programming Topics (Apple)
- x 29: Streams Programming Guide
- o 19: CFNetwork Programming Guide, sockets (Apple)
- o 14: Networking Concepts (Apple)
- o 17: Concurrency Programming Guide (Apple)
- o 20: Cryptographic Services Guide (Apple)
- o 18: Keychain Services Programming Guide (Apple)

- o 15: Key-Value Coding Programming Guide (Apple)
- o 16: Key-Value Observing Programming Guide (Apple)

- o 23: iOS Human Interface Guidelines (Apple)
- o 24: iOS Technology Overview (Apple)
- o 25: Core Data Programming Guide (Apple)
- o 26: Location Awareness Programming Guide (Apple).
- o 28: Threading Programming Guide

- o 30: Notification Programming Topics



## Apple samples

- o NavBar
- o Tabster
- o AdvancedTableViewCells
- o AppPrefs
- o iPhoneUnitTests / UnitTests
- o Regions (for changing level of monitoring depending on foreground/background)
- o SimpleDrillDown
- o TableViewSuite
- o TheElements
- o PhotoLocations
- o CoreDataBooks

- CoreTextPageViewer
- DrillDownSave
- GenericKeychain
- HazardMap
- LargeImageDownsizing
- LazyTableImages
- LocateMe
- iPhoneCoreDataRecipes
- PhotoPicker
- PhotoScroller
- Reachability
- StreetScroller (infinite horizontal scrolling)
- SysSound (system sound notifications, vibration)
- TableMultiSelect
- TableViewUpdates
- UICatalog
- URLCache

## Notes

### General

- Good project defaults:
	- Project options -> Build Settings -> All, Buld Options -> Run Static Analyzer = Yes.
	- Menu bar Product -> Edit Scheme -> Run on left menu -> Diagnostics tab -> Enable Zombie Objects

### 01: Your First iPhone Application

- Automatic Reference Counting (ARC) is provided by `@autoreleasepool` around `UIApplicationMain` call in `main`. It's compile-time memory management, not garbage collection.
- App delegates provide the window.
- Storyboard, defined in Info.plist, a supporting file, stores objects, transitions, and connections in the app's UI.
- View controller is an object that manages content.
- Initial view controller is the first view controller that gets loaded.
- View is an object that draws content and handles user events.
- View hierarchies.
- Canvas is the grid background in storyboard.
- Storyboard scene is a view controller.
- Storyboard segue is a transition between two scenes.
- Initial scene indicator is arrow on left of storyboard.
- Outline view is between canvas and project navigator.
- First responder (orange cube) is the object that is first to receive events when app is running (focus, motion, actions).
- target-action mechanism: Cocoa Touch design pattern for UI event binding.
- CTRL-drag to connect UI element to view controller.
- Outlet describes connection between two objects, e.g. view controller and child object.
-	Connections Inspector in the utilities panel lets you examine action / outlet connections.
-	Delegate is a Cocoa Touch design pattern, designate another object to act on your behalf.
-	Delegate in storyboard: CTRL-drag UI element to yellow sphere, which represents the view controller.
-	Property declaration is directive that tells compiler how to generate accessor methods for a variable in .h file, e.g.

		@property (copy, nonatomic) NSString *userName;
			
-	Accessor method gets or sets value of object's property, aka getters and setters. You need to tell the compiler to `synthesize` them in .m just after `@implementation`, i.e.:

		@synthesize userName = _userName;

-	`_username` is the internal variable that stores the value; this line generates a getter and a setter.
-	Keyboard is toggled via which UI element has first responder status; if it's a text field it appears, if not it disappears.
-	A protocol is a list of methods, i.e. Java interface.
-	A delegate protocol specifies all messages an objects might send to its delegte.
-	Recall that in this example the view controller is the delegate for the text field.

### 02: Your Second iOS App: Storyboards

-	Model layer.
-	Master and detail scenes (i.e. view controllers).
-	Navigation controller is also a _container view controller_ because, in addition to its views, it also manages a set of other view controllers. In default app is manages navigation bar, back button, master and detail view controllers.
-	A _segue_ is a transition from one scene (the _source_) to the next (the _destination_).
-	A _push_ segue slides destination over source right-to-left.
-	A _relationship_ is a connection between scenes. Navigation controller has relationship with master scene.
-	p21: `@property` in .h, `@synthesize` underscore-suffixed version in .m.
-	Can directly reference `_var` in `init`, `dealloc`, and getter/setter properties, else reference property `self.var`.
-	Want a pure data model class and a data controller class; consumers go through data controller.
-	Don't `import` class in data controller .h when a forward declaration will do, `@class Name`. `import` in .m.
-	_Class extensions_. Private methods go in `@interface Class ()` section before `@implementation` in .h.
-	_Cell_: a table row.
-	Storyboards have two ways to design cells:
	1. _Dynamic prototypes_: design one cell, use it as a template.
	2. _Static cells_: design overall layout of table.
-	p31: how to set up table cells.
-	Connect the master view controller to the data controller with a forward declaration in .h and a data controller property `(strong, nonatomic)` and `import` in .h.
-	p37: `cellForRowAtIndexPath`.
-	p37: minimize what app delegate does, put as much logic in view controllers as possible.
-	`self.window.rootViewController` = `UINavigationController`.
-	p46: In `viewDidUnload` release any strong references by setting to nil.
-	p47: to create segue:
	-	CTRL-drag table cell from master scene to detail scene, select Push.
	-	select segue, go to attributes inspector, enter a custom ID into the identifier field to differeniate between segues for `prepareForSegue`.
-	p50: making static table cells for a detail view. Connect UILabel views to detail view controller properties
	-	CTRL-right click,
	-	CTRL-drag new referencing outlet circle to yellow sphere, i.e. view controller.
-	p53: pass data between scenes in `prepareForSegue`; when _source_ scene is aboue to transition to _destination_ scene.

-	p58: Adding a scene to a navigation hierarchy is good pracice. Select view controller, Editor -> Embed in -> Navigation controller
	-	Easiest way to add a navigation bar on top, but not necessary if you're not navigating onwards.
	-	Ensure the nav bar is always on top.
	-	Easy to extend to add further scenes.
-	p63: you can (must) add your own buttons to a navigation bar.
-	p69: again, view controller becomes text field delegate (i.e. follows `UITextFieldDelegate` protocol) to handle `textFieldShouldReturn` and revoke text field's first responder status and dismiss keyboard.
-	p70: create delegate protocol to pass data from destination to source after segue.
-	p73: modal segue, slide up/down. CTRL-drag navbar button to the navigation controller of the branch.
-	p75: tricky, how to find actual destination view controller in `prepareForSegue` given `UINavigationController` parent.
-	p77: troubleshooting
-	p79: next steps, come back (or not) after reading more guides

### 03: Your Third iOS App: iCloud

### 04: iOS App Programming Guide

-	Translating design into action
	-	Choose a data model (how, data controllers, structured or not)
	-	Decide whether you need to support documents (`UIDocument`, Core Data, iCloud).
	-	UI approach
		-	Building blocks, existing components
		-	OpenGL ES-based.
-	Starting the app creation process
	-	Basic interface-style?
	-	Universal app or specifically iPad/iPhone.
	-	Storyboards? iOS 5 and later only.
	-	Core Data? Better for structured data.
-	p20: key objects in an iOS app.
-	p21: in iOS 5 and later app delegate is dispatched events if `UIApplication` doesn't handle it. Reference: _`UIResponder` Class Reference_.
- p31: what is in an app bundle.
	-	p34: how to access bundle. References: _Resource Programming Guide_, _Bundle Programming Guide_.
-	p37, fig 3-1: state changes in iOS app.
-	p39: fig 3-2: launching an app into the foreground.
-	p40, fig 3-3: launching an app into the background. no UI, just handles events. can tell on `applicationState` property of shared `UIApplication` object (p41).
-	p42: what to do in app delegate's `application:didFinishLuanchingWithOptions:`.
	-	check launch options dictionary, why was app launched.
	-	initialize critical data structures.
	-	prepare window and views.
	-	use saved preferences and state to restore.
-	p44, fig 3-4: handling alert-based interruptions.
-	p45: what to do when an interruption occurs, i.e. app delegate's `applicationWillResignActive`:
	-	stop timers and periodic tasks
	-	stop any running metadata queries (iCloud)
	-	do not initiate new tasks
	-	pay movie / audio playback
	-	suspend any dispatch queues or operation queues executing non-criticial code.
	-	close references to files protected by `NSFileProtectionComplete`.
	-	you can continue processing network requests and other time-sensitive tasks.
-	reverse the above in `applicationDidBecomeActive`
-	p47, fig 3-5: moving from foreground to background.
-	p48, what to do when moving to background, i.e. `applicationDidEnterBackground`, you have 5 seconds
	-	when `applicationDidEnterBackground` returns the system take a screenshot. Hide sensitive information before this returns.
	-	save user data and state to disk with a background thread.
	-	free up as much memory as possible.
	-	can call `beginBackgroundTaskWithExpirationHandler:` method for long-running tasks.
-	can use default notification cener to register for `UIApplicationDidEnterBackgroundNotification`
-	p50, fig 3-6: transitioning from the background to the foreground, also via `UIApplicationWillEnterForegroundNotification`.
-	p51, table 3-2: notifications delievered to waking apps.
-	be sure to respond to changes in app's settings when coming back to foreground (p53).
-	p54, fig 3-7: processing events in the main run loop.
-	p56: multitasking support in `UIDevice.multitaskingSupported`.
-	p57: call `beginBackgroundTaskWithExpirationHandler` before any critical task you want to protect from immediate termination on backgrounding. Need to `endBackgroundTask` eventually, or killed anyway.
-	p60: declare what long-running background task resources you need in `Info.plist`, e.g. `location`.
-	p61: tracking user location in background. significant-change (recommended), foreground-only, and background.
-	p65: being a responsible background app:
	-	always cancel listening sockets in backgrounding; you can't listen anyway.
	-	prepare to handle socket failure.
	-	always save state on suspension.
	-	release unneeded memory.
	-	stop using shared system resources, e.g. address book.
	-	avoid updating windows and views.
	-	remove sensitive info from screen.
	-	do minimal work.
-	p67: can explicitly opt out of backgrounding, just dies on suspension.
-	p81: using SQLite on iCloud only supported if you use Core Data.
-	p88: declaring `UIRequiredDeviceCapabilities` in `Info.plist`, e.g. `gps` and `location-services`.
-	p98: settings bundle for app settings. use for unfrequently-changed settings, else put directly in app.
-	p105: preserving the state of your app's user interface. walk your view controller hierarchy.
-	p107: protecting data using on-disk encryption.
-	p112: configuring reachability interfaces using `SCNetworkReachabilityRef`. Reference: _System Configuration Framework Reference_.
-	p120: Critical app data in `<Application_Home>/Documents`.
-	p121: Non-critical for iOS 5.1+ in `<Application_Home>/Library/Application Support`, else `<Application_Home>/Library/Caches`
-	p123: can do _Simulate Memory Warning_ in iOS Simulator.
-	p123: `-mthumb` to reduce code size by 35%, but not if you use floating point arithmetic.
-	p128: level-wise, `NSStream` on top then `CFNetwork` then BSD sockets.

### 05: Cocoa Fundamentals Guide

-	Xcode performance tools
	-	Instruments, performance over time.
	-	Shark, trace function calls and allocs over time.
-	Objects support notifications
-	p55: Major classes
-	p65: Categories: add behaviour to a clas, like a Java interface. Cannot add instance variables, don't override existing methods.
-	p67: Protocols
-	p69: Properties
-	p74: how to call:

		NSClassName *variable = [receiver keword1:param1 keyword2:param2];
		
-	p78: summary of what NSObject can do, hence what all objects can do.
-	p88: You own an object if NARC: new, alloc, retain, copy. new === alloc+init. Hence you must release when you're done owning an object.
-	p94: `init` rules, i.e.

		- (id)initWithXXX:(NSString *)id1 {
			if (self != [super init]) {
				return nil;
			}
			// some initialization
			if (!successful) {
				return nil;
			}
			return self;
		}
		
-	p95: multiple initializers should call a designated initializer.
-	p99: class factory methods for e.g. enforcing singletons.
-	p123: how to create a singleton instance.
-	p130: Cocoa API conventions
	-	on error return nil / false
	-	if error last input is pointer is dereferenced and set with NSError
	-	prefer constant strings to literals, i.e. not:
	
			@"foo"
		
		but:
			
			//.h
			extern NSString * const Foo;
			
			//.m
			NSString * const Foo = @"Foo";
			
-	Subclasses need (p155):
	-	`isEqual`, `hash`.
	-	`description`: concise string that describes properties or contents, returned by `print object`
	-	`copyWithZone`: if you expect copying
	-	`initWithCoder`, `encodeWithCoder`, if you expect archiving.
-	p165: Design patterns
	-	p171: Command pattern via `NSInvocation` class and Target-Action mechanism
	-	p184: Observer pattern via notifications. Synchronous: `NSNotification`, async: `NSNotificationQueue`. Management: `NSNotificationCenter`. More details p227.
	-	p185: Receptionist pattern via key-value observing.
	-	p210: Outlets.
	
### 06: View Controller Programming Guide

-	A view controller manages a set of views.
-	You manage your content by creating subclasses of `UIViewController` or `UITableViewController`.
-	Container view controllers manage other view controllers.
- Can temporarily _present_ another view controller; this brings its view on screen and when its dismissed it tells the calling view controller the result. (Reminiscent of Android ActivityWithResult).
- Storyboards link user interface elements into an app interface. Storyboards hold preconfigured instances of view controllers and their associated objects.
- p17, fig 1-5: view controller classes in UIKit, look for subclasses of `UIViewController`.

- _Content View Controllers_ display content.
	-	1:1 between views and parent view controllers.
	-	Content view controller only shows one screen.
	- _Table View Controllers_, i.e. `UITableViewController`. Tabular. You can subclass.
	
- _Container View Controllers_ can combine together, hierarchies of view controllers.
	- _Navigation Controller_: `UINavigationController`, stack-based navigation with nav bar.
	- _Tab Bar Controller_: `UITabBarController`. 2+ modes of operation.
	- _Split View Controller_: `UISplitViewController`. Master-detail. iPad only.
	- _Page View Controller_: page layout, discrete pages like a book. Lazy loading.

-	p25: to display a view controller must be associated with window, by:
	-	making it the window's root view controller.
	-	child of a container view controller.
	-	show it in a popover controller.
	-	present it from another view controller (segue). When presenting can determine how much screen is used, called _presentation context_, default the whole window. Transient.

- p28: combination of views and view controllers establishes _responder chain_ for events.
- p28: navigation controller children are siblings arranged in stack tab view controller children have no relationship.
- p30: source view controller provide properties to destination view controllers. destination view controllers call delegates that implement the delegate's protocol to communicate back with source.

- p37: when are view controllers instantiated by iOS:
	-	if relationship is segue, destination view controller is intantiated when segue is triggered.
	-	if relationship is container, child view controller instantiated when parent is instantiated.
	-	if not destination or child never instantiated automatically, you must do so programmatically.
- p37: label all segues with identifiers.
- p37: can use multiple storyboards.
- p38: programmatically trigger segues using source view controller's `performSegueWithIdentifier:sender:`.
- p39: instantiating a storyboard's view controller programmatically.
	-	obtain storyboard object, `UIStoryBoard`.
	-	call storyboard object's `instantiateViewControllerWithIdentifier:` or `instantiateInitialViewController`.
	-	configure new view controller by setting properties.
	-	display new view controller.
- p41: transitioning to a new storyboard requires a programmatic approach.
- p42: how to display view conroller contents programmatically.
- p47: designing your content view controller:
	-	are you using a storyboard to implement it?
	-	when is it instantiated?
	-	what data does it show?
	-	what tasks does it perform?
	-	how is its view displayed onscreen?
	-	how does it collaborate with other view controllers? contained? segues to/from?
- p50: examples of common view controller designs.
- p55: as you define your view controller you'll probably end up adding:
	-	_declared properties_ pointing to the objects containing the data to be displayed in child views.
	-	_public methods and properties_ to expose view controller's custom behavior to other view controllers.
	-	_outlets_ pointing to views in hierarchy with which the view controller must interact.
	-	_action methods_ that perform tasks associated with buttons and other child views.
- important: define outlets and actions in nameless category, so that other view controllers don't depend on them, i.e.

		@interface MyViewController ()
		// outlets and actions here
		@end
		
		@implementation MyViewController
		// implementation of privately declared category here.
		@end

- p56: when view controller loaded form storyboard it opens an archive.
- p58, fig 4-1: loading a view into memory.
- p60, fig 4-2: unloading a view from memory.
- p62: creating a view programmatically. p63 => don't call `super` in `loadView:`.
- p64, table 4-1: places to allocate and deallocate memory.
- p66: gotchas for scrolling a view.
- p68: how views get sized by view controller, reference _View Programming Guide for iOS_
	-	view controller's view if resized.
	-	view controller calls `viewWillLayoutSubviews`
	-	view controller's view calls its `layoutSubviews` method.
	-	view controller calls `viewDidLayoutSubviews`.
- p70, fig 6-1: responder chain for view controllers. Reference: _Event Handling Guide for iOS_.
- p78, fig 8-1: responding to the appearance of a view.
- p79, fig 8-2: responding to the disappearance of a view.
- p87: presenting a view controller programmatically.
- p100: enabling edit mode in a view controller.
- 

### 07: Event Handling Guide for iOS 

### 08: View Programming Guide for iOS 

### 09: View Controller Catalog for iOS 

### 10: Table View Programming Guide

-	p21: table view is itself instance of `UITableView`, inherits from `UIScrollView`.
-	p21: `UITableView` object must have a delegate and a data source. Often delegate and data source the same object, and often this object is a subclass of `UITableViewController`. (surely could be property too?)
	-	data source mediates between app's data model (model objects) and table view.
	-	data source adopts `UITableViewDataSource` protocol. Two methods: `tableView:numberOfRowsInSection:` and `tableView:cellForRowAtIndexPath:`.
	-	delegate adopts `UITableViewDelegate`, no required methods.
-	p22: can also use convenience class `UILocalizedIndexedCollation` for indexed lists (the A-Z on right side).
-	Many methods return values representing index paths. Use `NSIndexPath`.


### 11: Design then Code (two tutorials on iOS apps)

### 12: Networking Overview

-	p15: design for variable network availability.
	-	for requests made at user's behest:
		-	always attempt to make connection. don't guess if it'll work or not.
		-	if the connection fails, use `SCNetworkReachability` API to diagnose failure. then.
			-	If transient error, try again.
			-	If host unreachable, wait for `SCNetworkReachability` API to call your registered callback. When host reachable, then retry.
		-	try to display connection status in non-modal way, don't block user.
	-	for requests made in background:
		-	attempt to make connection. Use `SCNetworkReachability` to avoid making connection at inconvenient times, e.g. avoid 3G.
		-	if conenction fails use `SCNetworkReachability` API to wait for host to become reachale.
		-	do not display any dialogs.
		-	don't retry too quickly, use exponential backoff up to e.g. 15 minutes.
-	`SCNetwokReachability` is not intended as preflight check of connectivity. It is intended as post-failure diagnostics.
-	Xcode has tool called _Network Link Conditioner_ that simulates network conditions.

### 13: Networking Programming Topics

- For TCP, basically says to refer to _Stream Programming Guide_, provides short summary on p9.

### 17: Concurrency Programming Guide

- _Grand Central Dispatch (GCD)_: define tasks and add them to appropriate dispatch queue.
- _Operation queues_: Objective-C object that act like dispatch queues. Much more startup efficiency than threads.
	- `NSOperationQueue`.
	- Not first-in first-out.
	- Can have task dependencies.
	- Tasks are subclass instances of `NSOperation`, _operation objects_. Use KVO.
	-  p13 => initially assume no task is too small.
- _Dispatch queue_: C-based mechanism for first-in first-out serial or concurrent executing of tasks.
- _Block object_: C-based, similar to function pointers, can be copied onto heap with their own scope.
- _Dispatch source_: C-based, monitor system events asynchronously. Part of GCD. 
- Process
	-	Define your application's expected behaviour.
		-	Enumerate the tasks your application performs and the objects or data structures associated with each task.
		-	Break each task down furhter into a set of steps.
	-	Identify places where code may benefit from concurrency. Maybe change order. No task is too small.
	-	Identify the queues you need.
- p17: `NSInvocationOperation`: as-is object to execute object:selector:. Subclass of `NSOperation`.
- p17: `NSBlockOperation`: as-is object to execute blocks concurrently.
- p19: only need to implement _concurrent operation_ if you need to execute asynchronously without adding to operation queue.
- p19, listing 2-1: creating an `NSInvocationOperation`.
- p20, listing 202: creating an `NSBlockOperation` object.
- p27: `NSOperation` is KVO compliant for all these keys.
- p29: `addDependency:` to `NSOperation`.
- p29: `setQueuePriority:` for `NSOperation`.
- p33: executing operations, adding operations to an operation queue.
- p34: `setMaxConcurrentOperationCount:` sets concurrency for operation queue object.
- p35: cancelling. `cancel` on `NSOperation` or `cancelAllOperations`on `NSOperationQueue`.
- p37: `setSuspended:` to suspend/resume queue.
- p39: _private dispatch queue_: serial queue for GCD. Can create as many as you want.
- p39: _global dispatch queue_: concurrent queue for GCD. There are three of these per application.
- p39: _main dispatch queue_: globally available serial queue that runs on app's main thread.
- p41: _dispatch group_: monitor a set of block objects for completion.
- p41: _dispatch semaphore_: efficient semaphore
- p41: _dispatch source_: generate notifications.
- p43: use context pointer of dispatch queue to share data.
- p43: if blocks have more than a few Objective-C objects enclose parts of the block in an `@autorelease`.
- p43: getting global dispatch queue:

		dispatch_queue_t aQueue = dispatch_get_global_queue(DISPATCH_QUEUE_PRIORITY_DEFAULT, 0);
		
- p44: create/use serial dispatch queues to protect a resource (i.e. not use locks) or synchronize some key behaviour.

		dispatch_queue_t queue;
		queue = dispatch_queue_create("com.example.MyQueue", NULL);

- p45: `dispatch_get_current_queue` to test identity of current queue from block.
- p45: `dispatch_get_main_queue` to get serial dispatch queue associated with app's main thread.
- p46: `dispatch_set_context` and `dispatch_get_context` to associated shared data with queue or block.
- p48: `dispatch_async` and `dispatch_async_f` to asynchronously add task to queue. Example here.
- p49: completion blocks, executed after task complete. Example in listing 3-4.
- p51: `dispatch_apply` or `dispatch_apply_f` to parallelzie loops. Consider using stridling to batch loops (p78).
- p52: suspending and resuming queues.
- p53: example of using dispatch semaphore to limit maximum number of files open.
- p53: waiting on groups of queued tasks.
- p54: don't call `dispatch_sync` from a task on the same queue. If you need to then use `dispatch_async`.
- p56: dispatch sources:
	-	_timer dispatch sources_: periodic notifications.
	-	_signal dispatch sources_: UNIX signals
	-	_descriptor sources_: file/socket data available for read/write, file data and metadata changes.
	-	_process dispatch sources_: process exit/fork.
	-	_custom dispatch sources_: make yourself.
	- replace asynchronous callback functions.
-	dispatch sources submits event handler whenenver corresponding event occurs.
- p57: creating dispatch sources:
	-	`dispatch_source_create`
	-	configure; assign event handler (`dispatch_source_set_event_handler` or `dispatch_source_set_event_handler_f`), or for timers use `dispatch_source_set_timer`.
	-	optional cancelling handler.
	-	call `dispatch_resume` to start processing.
- p59, table 4-1: getting data from a dispatch source.
- p63, listing 4-1: creating a timer dispatch source.
- p65, listing 4-2: reading data from a file.
- p67, listing 4-3: writing data to a file.

### 22: Core Data Tutorial for iOS

- Reference: _Core Data Programming Guide_
- _Stack_: collection of Core Data framework objects that work together to get modelled objects to and from _persistent store_, the file where data is stored. Can be SQLite if you want.
-	_Managed object_ is instance or subclass of `NSManagedObject`, object representation of record in database. Always associated with mananged object context.
-	_Managed object context_ instance of `NSManagedObjectContext`. Manages objects, does life-cycle management, validation, relationship maintenance, undo/redo.
-	_Managed object model_ is instance of `NSManagedObjectModel`, object that represents schema. Collection of `NSEntityDescription` objects. Entity descripiton describes entity in terms of name, class, properties.
-	_Persistent store coordinator_: instance of `NSPersistentStoreCoordinator`. Manages collection of _persistent object stores_. Persistent object store represents external store file.
-	Entity is Event, attributes are creation date, lattitude, and longitude.
-	Many ways to edit the model, reference: _Xcode Tools for Core Data_.
-	Select `Locations.xcdatamodel`, Editor -> Add Entity. Then Add Attributes to the Entity. Rename, define type.
-	p25: common to have custom managed object class
	-	select the entity, select new file, do Core Data -> NSManagedObject subclass.
-	Notice all properties are `@dynamic` in .m. Core Data generates accessor methods at runtime
- Notice that raw types are wrapped as e.g. `NSNumber`.
-	Notice there is no `dealloc`. Core data handles life-cycle of all modelled properties of a managed object. If you add instance variables you're responsible for them.
-	p27: adding events.
-	p28: typically create managed object using `insertNewObjectForEntityForName:inManagedObjectContext:` of `NSEntityDescription`.
-	You accessor methods to set attributes. Nothing saved implicitly. Need to explicitly save with `managedObjectContext save`.
-	p30: displaying data in table. lots of faff but eventually we just read off of the local `self.eventsArray`.
-	p33: how to fetch managed objects. _fetch request_, instance of `NSFetchRequest`, like SQL `SELECT`. Predicates specified using `NSPredicate`, sort order by array of `NSSortOrdering` objects. reference: _Predicate Programming Guide_.
-	p34: Core Data gets related objects for you, like Django.
-	p34: key code for preparing fetch for core data entity.
-	p37: deleting managed objects. `deleteObject:` method of `NSManagedObjectContext` then `save:`.
-	p40: next steps, might be fun.
	-	really want to use `NSFetchedResultsController` to efficiently get many objects.
	-	_faulting_: don't have the complete the object graph. that means if you have .e.g photograph don't fetch all photos. See _PhotoLocations_ example.

### 26: Location Awareness Programming Guide

- p11: call `CLLocationManager::locationServicesEnabled:` to see if location services available.
- p11: can set up `desiredAccuracy` and `distanceFilter`.
- p12: starting the significant-change location service, calls a delegate on event.
	- Significant power savings.
	- Service automatically wakes up application when new location data arrives, but not much time to process data and still in background.
-	p13, listing 1-3, processing an incoming location event. Check timestamp of datum.
-	p14: check reported accuracy of location events and discard less-accurate data and wait for more-accurate data to come. Check that accuracy is actually improving over time and, if it doesn't, abandon effort (p18).
-	p23: can use geocoder objects to convert GPS coordinates to place name. in iOS 5 can do place name to GPS coordinates.   

### 28: Threading Programming Guide

- p38: performing selectors on other threads.
- p42: using run loop objects.
- p44: better to use input sources than to use a periodic timer to poll a run loop to keep secondary thread running.
- p45: skeleton for running a run loop
- p45: better to explicitly tell a run loop to stop than removing all its input sources. Latter only implicitly stops it and might be unable to remove input source.
- p48: custom input source.

### 29: Streams Programming Guide

- p8: generally how to use streams. p22 has how to start socket streams.
- p9 => open stream on secondary thread and schedule the stream on the thread's run loop.
- p10: how to handle bytes-available event on NSStream, i.e. receiving from stream.
- p14: how to handle space-available event on NSStream, i.e. sending to stream.
- p16: how to close stream.
- p20: handling stream errors.
- p22: setting up socket streams.
	-	create and initialize `NSInputStream`.
	-	schedule the stream object on a run loop, open the stream. (but could use polling).
	-	handle events that the stream object reports to its delegate.
	-	when there's no more data dispose of the stream object.