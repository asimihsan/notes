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

