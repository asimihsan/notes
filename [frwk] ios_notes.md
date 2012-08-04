## Online tutorials

- x 01: Your First iPhone Application (Apple)
- x 02: Your Second iOS App: Storyboards (Apple)
- x 04: iOS App Programming Guide (Apple)
- o 03: Your Third iOS App: iCloud
- o 22: Core Data Tutorial for iOS (Apple)
- o 27: Core Data Utility Tutorial (Apple)

- x 05: Cocoa Fundamentals Guide (Apple)
- o 06: View Controller Programming Guide (Apple)
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


## Apple samples

- o NavBar
- o Tabster
- o AdvancedTableViewCells
- o AppPrefs
- o iPhoneUnitTests / UnitTests
- o Regions (for changing level of monitoring depending on foreground/background)
- o SimpleDrillDown

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
- TableViewSuite
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
- Canvas is the grid backgrond in storyboard.
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
-	p75: tricky, how to find actual desintation view controller in `prepareForSegue` given `UINavigationController` parent.
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
	-	can call `beingBackgroundTaskWithExpirationHandler:` method for long-running tasks.
-	can use default notification cener to register for `UIApplicationDidEnterBackgroundNotification`
-	p50, fig 3-6: transitioning from the background to the foreground, also via `UIApplicationWillEnterForegroundNotification`.
-	p51, table 3-2: notifications delieverd to waking apps.
-	be sure to respond to changes in app's settings when coming back to foreground (p53).
-	p54, fig 3-7: processing events in the main run loop.
-	p56: multitasking support in `UIDevice.ultitaskingSupported`.
-	p57: call `beginBackgroundTaskWithExpirationHandler` before any criticl task you want to protect from immediate termination on backgrounding. Need to `endBackgroundTask` eventually, or killed anyway.
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

### 07: Event Handling Guide for iOS 

### 08: View Programming Guide for iOS 

### 09: View Controller Catalog for iOS 

### 10: Table View Programming Guide

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


### 26: Location Awareness Programming Guide

- p11: call `CLLocationManager::locationServicesEnabled:` to see if location services available.
- p11: can set up `desiredAccuracy` and `distanceFilter`.
- p12: starting the significant-change location service, calls a delegate on event.
	- Significant power savings.
	- Service automatically wakes up application when new location data arrives, but not much time to process data and still in background.
-	p13, listing 1-3, processing an incoming location event. Check timestamp of datum.
-	p14: check reported accuracy of location events and discard less-accurate data and wait for more-accurate data to come. Check that accuracy is actually improving over time and, if it doesn't, abandon effort (p18).
-	p23: can use geocoder objects to convert GPS coordinates to place name. in iOS 5 can do place name to GPS coordinates.   

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