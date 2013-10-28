# Dart

## Dart tutorial

[http://www.dartlang.org/docs/tutorials/](http://www.dartlang.org/docs/tutorials/)

-   Selectors:
    -   `elem = query('<CSS selector>');` to select one element.
    -   `elems = queryAll('<CSS selector>');` to select a List of elements.

-   Can set text:

        query(...).text = "oh hi";

-   By default we have a launch that runs a special Chromium build with a Dart VM baked into it. You can, however, configure a launch to compile to JavaScript and then run a regular browser:
    -   Click next to Run, "Manage Launches"
    -   Click "New Dart2js launch" button in toolbar
    -   Name the launch, e.g. "<project>-with-js" or "<project>-with-js-in-firefox"
    -   In the "HTML file" field browse to the single main HTML file.

-   A web app project has one HTML file, one Dart file, one CSS file.

-   Elements are a subclass of Nodes. You generally work with Elements.
    -   `<input>` -> `InputElement`
    -   `<ul>` -> `UIListElement`
    -   `<li>` -> `LIElement`
-   `Element.parent` refers to its parent and is immutable; you can't move an Element by changing its parent.
-   The `List` datatype is a generic, can be typed e.g.
    -   `List<String>`
    -   `List<int>`
    -   `List<Element>`
-   `Element.children` is a `List<Element>` of children and is mutable.
    -   `Element.children.add(newChild);`

-   Function with one expression:

        int square(int a) => return a * a;

### Event handlers

-   Adding event handlers to an Element:

        `element.on<Event>.listen(<EventListener>);`

-   Event handlers are e.g.

        `void eventHandler(Event e) { ... }`

-   One-line event handler registration:

        element.onClick.listener((e) => element.children.clear());

-   Events e.g.
    -   `onClick`
    -   `onChange`
    -   `onKeyDown`


### CRUD elements

-   Creating Elements:

        `var newToDo = new LIElement();`

-   Removing an element from the DOM:

        `element.remove();`

-   Removing all children from an element:

        `element.clear()`

### Package manager

-   Specified as YAML in `pubspec.yaml`.
-   On e.g. adding package then saving "Pub install" is automatically run to update packages.
-   To import e.g. `vector_math`:

        import 'package.vector_math/vector_math.dart';

### Web UI

-   Web UI is another package that provides web components and MVC-type separation.
-   Offers data binding, and data updates on event handlers.
-   Need to use the Dart UI to automatically call Web UI compiler `dwc`.
-   To start using it add `web_ui` as a package dependency.

-   To set up background compilation:
    1.  Create a file `build.dart` in same dir as `pubspec.yaml`. Contents e.g.

```
import 'package:web_ui/component_build.dart';
import 'dart:io';

void main() {
  build(new Options().arguments, ['web/littleben.html']);
}
```

    2.  Select `build.dart` and click the play button to build. You'll notice a new `out` directory under `web`.
    3.  Run your app as before, and this will continue to rebuild.

-   With Web UI you can use templates to attach to variables that are just defined in the Dart code, e.g.

        <!-- HTML -->
        {{ variable_name }}

        // DART
        variable_name = "oh hi there";

-   Web UI attaches a watcher such that whenever the variable changes the template will update.
-   Web UI will trigger watchers "at sensible points", like clicking or after loading.
-   To trigger watchers manually, import:

        import 'dart:async';
        import 'package:web_ui/watcher.dart' as watchers;

-   Then use:

        void main() {
            var oneSecond = new Duration(seconds:1);
            var timer = new Timer.periodic(oneSecond, updateTime);
        }

        var updateTime(Timer _) {
            // update something
            watchers.dispatch();
        }   
i

-   You can do **two-way bindings**, which mean changes in an input field on the HTML side go to Dart, and vice-versa.

        <input type="text" bind-value="shoutThis" ...>
        <div>Length: {{ shoutThis.length }}</div>

-   Can also do `bind-checked` with radio buttons, and `bind-selectedIndex` with select elements.
-   Template expressions in `{{ }}` can be any valid Dart code.

### Web UI - declarative event handlers

-   Can add event handlers on the HTML side:

        <button on-click="startwatch()" id="..">

-   Also:
    -   `on-double-click`, double clicking
    -   `on-change`, change events on input fields.
    -   Reference: [http://api.dartlang.org/docs/releases/latest/dart_html/Element.html](http://api.dartlang.org/docs/releases/latest/dart_html/Element.html)

-   If you want to pass the event itself:

        <!-- HTML -->
        <button on-click="startwith("$event")">

        // DART
        void startwatch(Event d) { ... }

-   More information about Web UI: [http://www.dartlang.org/articles/web-ui/](http://www.dartlang.org/articles/web-ui/)

### Use <template>

-   In your HTML:

        <template instantiate="if show">
        ... {{ value1 }} ...
        </template

-   In Dart:

        bool show=false;
        ...

-   Can also iterate over containers:
    -   In your HTML:

            <template iterator="wrongchar in wrongletters">{{ wrongcar }}</template>

    -   In your Dart:

            List<String> wrongletters = new List();

### Define a Custom DOM Tag

-   Wrap all HTML and Dart together into a Web UI package.
-   How to define an element, and what it extends, and what corresponding Dart class will construct it.

```
<element name="x-fancy-button" extends="button" constructor="FancyButtonComponent">...</element>
```

-   To create an instance:

```
<x-fancy-button>...</x-fancy-button>
```

-   The custom element gets its own pair of HTML/Dart files.
-   TOREAD

### Fetch Data Dynamically

[http://www.dartlang.org/docs/tutorials/fetchdata/](http://www.dartlang.org/docs/tutorials/fetchdata/)

Parsing from string to JSON Map:

```
import 'dart:json' as json;

Map jsonData = json.parse(jsonDataAsString);
```

Seralizing from JavaScript to string:

```
import 'dart:json' as json;

intAsJson = json.stringify(1);
...
```

-   Practically, can only make HTTP requests to co-located resources (from the same origin).
-   See example: "portmanteux_simple"

