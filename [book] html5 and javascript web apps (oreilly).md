# HTML5 and JavaScript Web Apps

O'Reilly, 2012

## Ch1 - Client-Side Architecture

-    Fat clients are back.
-    Before HTML5, server-side templating and JS for nicities.
-    Browsers are becoming application platforms.
-    Cross-browser DOM libraries like jQuery are not enough, do not give a client-side architecture.
-    Architecture of heavy, HTML5-driven UI still in its infancy, but this is the topic of the book.

## Ch2 - The Mobile Web

-    Support mobile first, then desktop.
-    Why?
    -    You think about constrained resolutions, flexible layouts.
    -    Device sensors.
    -    Code-quality, battery life.
    -    Bleeding edge.
-    WebKit on iOS and Android
-    Android moving to Dolphin.
-    Opera Mobile.
-    Internet Explorer Mobile.
-    QA
    -    Preferable to use actual devices.
    -    Emulators available at [mobilexweb](http://www.mobilexweb.com/emulators).
    
## Ch3 - Building for the Mobile Web

-    Success dependent on design and performance.
    -    Consistent across all platforms.
    -    Constrained by CPU/GPU and network throughput/latency.
-    Reference: Mobile Design Pattern Gallery (O'Reilly), for UI patterns for native apps.
-    Want to use hardware acceleration where possible.
    -    Functions like `translate3d`, `scale3d`, `translateZ`.
-    CSS features like `gradient`, `box-shadow`, `borders`, `background-repeat` cause many repaints, taxing on GPU and battery life.
-    p36: use JavaScript to swap class names, and let CSS handle animation.
    -    Decouples JavaScript from CSS.
-    Sliding, flipping, and rotating animations.
-    How to debug frames per second and hardware acceleration in Safari.
-    p50: fetching and caching
    -    Code for looking for pages with a `fetch` class name and then using `ajax()` to pre-fetch and then insert into `localStorage`.
    -    p53: write AJAX response text into a sandboxed `iframe`.
        -    Browser does DOM parsing and sanitisation for you.
        -    Just as fast, sometimes faster, than usual `innerHTML` approach.
-    p56: network detection. online? slow?
-    p61: *single page* approach
    -    All content in one page. Each subpage wrapped in a div.
    -    **jQuery Mobile.**
        -    p61: example.
    -    **jQTouch**
        -    Basic widgets and animations.
        -    Lacks support for multiple platforms.
        -    p63: example
    -    In jQuery Mobile and jQTouch you write specially structures HTML. When loaded library reconfigured pages and turns regular links into AJAX-based animated ones.
-    p64: *no page structure* approach
    -    Light markup, not tied to specific DOM structure.
    -    **[xui](http://xuijs.com/)**
        -    Comes from PhoneGap.
        -    DOM manipulation for mobile environment.
        -    Very light.
-    p65: *100% JavaScript Driven* approach
    -    **Sencha Touch**
        -    Don't write HTML. UI and app in JavaScript.
        -    p66: example
    -    **Wink Toolkit**
        -    Small following.
        -    JavaScript helpers, UI via JavaScript.
        -    p68: example
    -    **The-M-Project**
        -    On top of jQuery and jQuery Mobile.
        -    MVC, Content Binding, Dynamic Value Computing, Event Handling.
        -    Much more than just fancy UI.
        -    p70: example.
    -    Other frameworks: SproutCore, Jo, Zepto, LungoJS, …, but not fit-for-purpose.
-    Mobile debugging
    -    **[weinre](http://people.apache.org/~pmuellr/weinre/)**
        -    Like a remote Firebug.
    -    **Adobe Shadow.**
        -    Again like remote Firebug.
    -    **Opera Dragonfly**
        -    For Opera Mobile Emulator.
        
## Ch4 - The Desktop Web

-    Moving towards client-side generation of view. Backend delivers just data over JSON / XML.
-    Pros: better UX, less bandwidth, offline capable.
-    Cons: security of locally stored data, speed.
-    Feature detection
    -    **modernizr.js** or simple JavaScript to detect client-side capabilities.
    -    **FormFactor.js** for detecting resolution.
    -    Sometimes, however, you unfortunately need to parse `userAgent` string, especially for bugs.
    -    **ua-parser** for parsing useragent.
    -    **Platform.js** is another userAgent detection method.
    -    **MobileESP** for server-side userAgent detection.
-    Compression.
    -    GZIP resources and JSON/XML responses.
-    Minification, p90
    -    **JSLint** then **JSMin**
    -    **Packer**, popular and advanced.
    -    **Dojo ShrinkSafe**, popular.
    -    **YUI Compressor**, safety of JSMin with high compression of ShrinkSafe.
    -    p91, **CompressorRater** to compare.
-    p91, **grunt**.
    -    Command-line build tool for frontend projects.
    -    node.js package.
-    **Jawr**, tunable JavaScript/CSS packager.
-    **Ziproxy**, forwarding, noncaching, compressing HTTP proxy.
-    MVC
-    TodoMVC for comparing many MVC frameworks with a simple Todo app.
-    **Backbone**
    -    Framework of choice.
    -    Uses **Undescore.js** heavily.
    -    Data is models. Created, validated, destroyed, saved to server.
    -    Any UI action change to model triggers `change` event. Views notified and update themselves.
    -    p99: `Model` and `Collection` example.
    -    RESTful URI endpoints for models.
-    **Ember**, p101
    -    Formerly Amber.js and SproutCore 2.0.
    -    Made by Apple
    -    less wiring than Backbone.
    -    p101: example
-    **Angular**, p102
    -    Made by Google.
    -    p103: example.
    -    Dependency injection.
-    **Batman**
    -    Created by Shopify.
    -    Similar to Knockout and Angular    
    -    p104: model, server synch.
-    **Knockout**
    -    Three core features
        -    Observable and dependency tracking.
        -    Declarative bindings.
        -    Templating.