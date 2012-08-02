## Online tutorials

- o Your First iPhone Application (Apple) (http://goo.gl/mkYmJ)
- o Cocoa Fundamentals Guide (Apple) (http://goo.gl/wp7gl)
- o View Controller Programming Guide (Apple) (http://goo.gl/EFfd7)
- o Table View Programming Guide (Apple) (http://goo.gl/J4SkT)
- o iOS App Programming Guide
- o Design then Code (two tutorials on iOS apps) (http://goo.gl/5rok6)

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

### Your First iPhone Application (Apple)

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

### Cocoa Fundamentals Guide

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
	
### View controller guide

