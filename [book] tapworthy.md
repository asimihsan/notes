# Tapworthy

## 1. Touch and Go

-	Each screen is a big blur, only partial attention.
-	No depth. Users spend order of seconds using your app in sprints.
-	"Right tool for the right job". You perform a single, well defined task, among a user's toolbox of other apps.
-	No loyalty, average of 20 uses of app before abandoned or uninstalled.
-	Users may never understand all your app's features, gestures, or buttons.
-	Fat fingers. Mistakes.
-	You will rarely get praise for elegance. You will always get anger for inelegance.

## 2. Is It Tapworthy?

-	What does your app do, and why?
-	What specific problem does your app uniquely solve for users?
-	Elegant, precise, focused use cases. Who, what, when, where, why.
-	Why would you use this app when you're away from your desk or computer? Why is it especially convenient to have anytime-anywhere access to this app?
-	_Accessory app_: augments an activity.
-	Easy to assume the use cases are obvious when you're making it, but can only tell once consumers handle it.
-	Don't show/hide, enable/disable. Python zen: "Explicit is better than implicit".
-	Primary use cases must be painfully obvious.
-	Too much flashy design distracts attention, might be difficult on other platforms.
-	Raison d'etre:
	1.	"I'm Microtasking".
		-	Short dashes of activity.
		-	Quick, simple, sharp focus.
		-	Shallow.
	2.	"I'm Local".
		-	Sensors provide personal context.
		-	GPS, motion, camera, microphone, compass.
	3.	"I'm Bored".
		-	Distraction.
		-	Exploration. Somewhere _else_ to be. Story, escape.
-	Personality, uniqueness.
-	Think big, bold, brash in the beginning. Then "Murder your darlings" ruthlessly. Think big but build small.
-	Identify key activity, then how your app can help users microtask the activity in a hurry.
-	Subset features for _most_ users to achieve _key_ activities.
-	What is value-add over a website?
	-	Efficiency is a feature. 
	-	Native polish makes content shine.
	-	Save it for later, offline access.

## 3. Tiny Touchscreen

-	Left-handed and right-handed one-hand access? Fat fingers? Thumb only?
-	Physical metaphors.
-	Thumbs access left/bottom or right/bottom edges, depending on handedness.	
-	Non-idempotent actions should go in difficult areas for thumb, i.e. right/top or left/top depending on handedness.
-	For left-handedness, only rarely permit flipping screen controls. Usually either ignore or use full-width controls in a stack.
-	44px is the size of a fingertip. Practical minimum size for any tap target is 44x30 or 30x44. Actual visuals may _look_ smaller but _target_ should meet this.
-	Don't crowd the screen.
-	Error feedback shouldn't use audio, flash screen and maybe vibrate.
-	Important information at the top, controls at the bottom.
-	Layout loosely on a 44px grid.