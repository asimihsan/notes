# erlang notes

## using rebar

-	References:
	-	Erlang application management with rebar: [http://alancastro.org/2010/05/01/erlang-application-management-with-rebar.html](http://alancastro.org/2010/05/01/erlang-application-management-with-rebar.html)
	-	http://www.slideshare.net/konstantinvsorokin/kostis-sagonas-cool-tools-for-modern-erlang-program-developmen
		-	_Dialyzer_: Automatically identifies bugs
		-	_Typer_: Displays/adds type information
		-	_Tidier_: Cleans up Erlang code.
		-	_Proper_: Performs semi-automatic property based testing.
		-	_CED_: Auto test suite, concurrency issues.

-	Install:

		wget https://github.com/basho/rebar/wiki/rebar -O rebar
		chmod u+x rebar

-	To get list of commands:

		./rebar -c

-	Create application:

		./rebar create-app appid=tcpproxy
	
-	Use a Makefile as shown in the `tcpproxy` app in `travelbot`.
-	Add dependencies to a `rebar.config` file inside the root, again consult app as reference.
-	Run `make`.
-	`tcpproxy` has other good tidbits in it.

- Display function specs:

        typer --plt .dialyzer.plt --show-exported src/