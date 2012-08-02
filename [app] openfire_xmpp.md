# Openfire XMPP setup

This document goes over my experience attempting to set up the Openfire XMPP server. It wasn't easy, pay attention.

## Initial steps

- Download the RPM for the latest version of Java, or yum/apt-get it, as you wish. [RPMs here](https://www.java.com/en/download/manual.jsp).
- Download the RPM for Openfire and install here. [RPM here](http://www.igniterealtime.org/projects/openfire/).
- Install PostgreSQL, follow [Linode's excellent instructions](https://library.linode.com/databases/postgresql).
- Create a database called `openfire` use `\l /usr/local/openfire/resources/database/openfire_postgresql.sql` to create the necessary tables.
- Make sure you enable PostgreSQL to allow connections over IP. Create a new user, grant it password access to this box over IP.
- Actual use this IP connection, check it works.
- Go to `http://localhost:9090`, this is the Openfire admin panel. By default when you start off you get a setup wizard. If you mess up and want to go back through the wizard add `<setup>true</setup>` to `/usr/local/openfire/conf/openfire.xml`.
- TODO Oddly enough Openfire will claim the PostgreSQL connection works but then revert to the embedded database. I need to figure this out.

## More!

- Admin panel default username is `admin`, password `admin`.
- Add a user via the admin panel, log in via a client like [Ignite Spark](http://www.igniterealtime.org/projects/spark/). This should work.
- At this point you'll notice your user's domain name is "127.0.0.1". This is annoying, and will really upset programming APIs that expect the domain name to be usable over a remote socket. To change this, go to the Openfire admin panel, -> Server -> Server Manager -> Server Properties, set `xmpp.domain` to `domain.fqdn`.
- Use a library like [Python Wokkel](http://wokkel.ik.nu/documentation/current/client.html) and explicitly confirm that you can log in as `username@domain.fqdn`.
- an API for adding/removing users is available via the "User Service" plugin. Easiest way to install it is via the admin page, Plugins -> Plugin Admin -> Available Plugins. The gotcha is that you need to enable it afterwards in Server -> Server Settings -> User Service. API thereafter is according to README file, e.g.

`http://example.com:9090/plugins/userService/userservice?type=add&secret=bigsecret&username=kafka&password=drowssap&name=franz&email=franz@kafka.com`



