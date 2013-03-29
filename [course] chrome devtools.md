# Chrome DevTools

via Code School

## 1.1: DOM Manipulation

History:

-    `alert()` calls
-    Cumbersome edit / reload / edit / reload cycle.

Now:

-    Live edit.
-    Debug JS.
-    Optimise with profilers.

We'll start off with the **elements** panel of DevTools.

### Finding elements

-    Can right click on any element then "Inspect Element" to see it in the DOM.
-    Or within the Elements panel can use the magnifying class button.

### Editing elements

-    Double-click on it's DOM element in the HTML source in the Elements panel.
-    Can add attributes, add additional elements.
-    Can click and drag elements.
-    Can delete elements with right click, or delete key.

## 1.2: Updating Styles

-    **Computed style** combines styles for all applicable CSS files.
-    The **styles** section is ordered from most specific (starting at inline styles) to lease specific).
-    Can *enable/disable* properties (use checkboxes)
-    Can *modify* (double click).
-    Can *delete* (double click, delete all the text for the value).
-    To *add* a style click the plus icon in the styles panel.
    -    If you add a style and then change it such that it no longer applies to the currently selected DOM object it'll dim gray. Avoid this.
-    To *force active/hover/focus/visited* state on an element, select the element then click the dotted rectangle icon in the styles panel.
-    Click on the file name : line number link to open the **source** panel.
-    Click on the colour value to get a swatch to easily pick a colour.

## 2.1: Editing in the Source Tab

If you want to make *permanent changes* use the Sources panel. Can *export* and track *versions*.

-    After changes use *CTRL-S (MAC-S) to save the file to the browser storage*.
-    Right-click -> "Local modifications" for *timestamped diffs*.
    -    Next to each revision click "apply revision content" to apply that partilcular diff.
    -    Next to each revision can also click "revert", or "apply original content" to go to original.
-    Right-click -> *"Save as…" to save file*, even the original.

## 3.1: Working with the Console

-    Interact with app's views and scripts.
-    Run JS commands.
-    View log output.

-    `console.log("blah blah blah");`
-    Selecting objects
    -    `document.getElementById('hello');`
    -    `var list = document.querySelector('#myList');`
-    Can get meta: `console.log(console)`
    -    Show Console's objects methods, including `assert`.
-    `console.assert(1 == 1)`, fine.
-    `console.assert(1 == 2)`, assert fails with stack.
-    Count how many times a line has been hit:

        function login(user) {
            console.count("Login called");
        }

-    Group logging output into collapsible sections (can be nested)

        console.group("Authentication user '%s'",user);
        console.log("User authenticated");
        console.groupend();

-  Can toggle profiling, `console.profile()`, `console.profileEnd()`.
-  Print current stack trace: `console.trace()`.
-  Reference: [Console API reference](https://developers.google.com/chrome-developer-tools/docs/console-api).

## 3.2: Examining Exceptions

-    Errors come with *stack traces*, and can click on file name : line number links to get into source.
-    Click on second button on bottom left to jump into console.

## 3.3: Element Selector Shortcuts

Shortcut for `document.querySelector('#title');`:

        $('#title');
        
Dollar sign pronounced as "bling". Note that if you use a JavaScript library like jQuery it'll overwrite Chrome's blind with a jQuery bling. They behave differently.

We can tell Chrome to highlight any selected DOM node:

        inspect($('#title'));
        
And the most recent selection is in `$0`. Next is `$1`. etc.

## 4.1: Debugging JavaScript

Meh.

## 4.2: Pause on Exception

In the bottom left the fourth button from left is **Pause on exception**. We'll break, then you can hover to find out what variables are.

-    If you click this button a *second time* it'll only break on **uncaught exceptions**.

Minifying JS files makes things much more difficult to debug; but if you click on the fifth buttom from left in bottom left it'll **prettify code**, even minified code.

Click on line number to **set breakpoint**.

-    Execution controls on the right-hand side can:
    -    resume
    -    step over
    -    step into (down)
    -    step out (up)
    -    deactivate all breakpoints.

## 4.3: Local Storage

Go to "Resources -> Local Storage -> file://". Shows you HTML5 Local Storage.

## 5.1: The Network Tab

-    Resource info (size, type)
-    Server response
-    Timeline

Disabling the cache in three ways:

-    Select Network panel, then SHIFT-refresh to avoid the cache and hence you won't see HTTP 304s.
-    Use an Incognito tab.
-    In the bottom-right, click on the gear, preferences, then select "no caching".

Timeline has two *shades*:

-     Initial translucent shade is when the browser realises it needs to get this resource.
-     Solid region until the end is when the browser actually starts the request, and then completes receiving it.

Timeline has *Colours*:

-    HTML: blue
-    Images: purple
-    JavaScript: orange
-    CSS: green

The **initiator** column indicates what is requesting this resource; "Other" in the beginning is the user.

Main JavaScript loading events are indicating by **lines**:

-    **DOM content loaded event** (body finished, but may be waiting for resources): *blue line*.
-    **Load event** (all resources are done downloading): *red line*.

## 5.2: Network Performance

Install Google PageSpeed extension. Adds a **PageSpeed** panel to your DevTools. Then click red "Analyze" button to analyze your page for issues.

Want to minify JS, or minify+combine into one, etc. One tool that does this is [Google Closure](https://developers.google.com/closure/). Or can use [Google Closure webapp](http://closure-compiler.appspot.com/home).

## 5.3: Removing Unneeded Requests

-    Identify requests that 404, or aren't shown on the page, and avoid them.
-    *Load JavaScript as late as possible*; HTML/CSS needed first to render page.
    -    You'll see the difference in the timeline; images and other resources needed for rendering requested earlier.
 -    *Load JavaScript asynchronously*; when requested it will be fetched after the HTML is loaded, it won't block.
 
        <script async src="script.js"></script>
        
-    If you set JS to be async you should see the DOM page  loaded event (blue line) being hit earlier.

## 5.4: Serving Correctly Sized Images

-    *Pre-scale your images*, don't shove big images to browser, leaving it to resize it for you.
-    *Serve appropriate formats*: GIFs for icons, JPG/PNG for photo-quality images.

## 6.1: Rendering Performance

Sometimes the problem isn't the network, it's what you're asking the browser to do.

**Frame rate** (FPS): number of images that get rendered on your browser per second.

-    If this drops below 30FPS, particularly 10FPS, it'll look like it's stutttering. What can slow down?
-    HTML loading. ("Loading"), blue
-    JS executon. ("Scripting"), yellow
-    Styling. ("Rendering"), purple
-    Painting to screen. ("Painting"), green

The **Timeline -> Frames** view tells you when this happens.

Hit record to start, then interact, then hit record to stop.

-    Horizontal lines indicate at what frame rate we're at.
-    Colours indicate what's happening.
    -    Idling is transparent.
-    But even if you know if JavaScript is slow, you'll need the CPU profiler (next section) to see *what* is slow.

## 6.2: CPU Profiling

**"Profiles" -> "Collect JavaScript CPU Profile" -> Start.**

You can then sort this by percentage occupied, and then see what functions are slow.

Frames is a good first step to know if it is slow; then you use CPU profiling to dive into JavaScript issues.

## 7.1: Memory Profiling

**Timeline -> Memory**

Hit record to start, then interact, then hit record to stop.

You'll be able to see if you have a memory leak or not, not where it is…but!

## 7.2: Pinpointing leaks

**Profiles -> Take Heap Snapshot -> Start**

Where is the memory leak? Usually you:

-    take a heap snapshot,
-    do something that exacerbates the memory leak, then
-    take another heap snapshot.
-    click the newest snapshot, change "Summary" to "Comparison", and compare against the older snapshot.

DOM elements that are highlighted red are detached from the DOM but haven't been garbage collected.

-    Avoid permanent references to DOM elements; look them up every time, particularly in event handlers.

## Other references

-    [The Breakpoint](http://www.youtube.com/playlist?list=PLNYkxOF6rcIBQ8j3J_PyM8JLAGKqZRByw): YouTube video channel.
-    [Chrome Developer Tools](https://developers.google.com/chrome-developer-tools/).
s