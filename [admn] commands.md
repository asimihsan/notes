## Commands

-   `tshark` HTTP traffic on loopback port 8000:

        sudo tshark -i lo -V -T text -f "tcp port 8000" -d "tcp.port==8000,http" -R "http.request"

-	`ffmpeg` conversion for iPad:

		ffmpeg -i ${input_file} -acodec libfaac -ac 2 -ab 192k -s 1024x768 -vcodec libx264 -vprofile baseline -tune film -preset slower -b:v 1200k -f mp4 -threads 0 ${output_file}

-	sort `du -h` output

		du | sort -nr | cut -f2- | xargs du -hs

-	streaming tcpdump directly to a Windows Wireshark instance (untested)

		tcpdump -w - -v -i eth0 http | "c:\program files\wireshark\wireshark.exe" -k -i -"

-	Python profiling

		# Execute command with profiling
		python -u -m cProfile -o profile.stats script.py arg1 arg2 --hostname blah

		# Sort stats by total time spent in function
		python -c "import pstats; p = pstats.Stats(\"profile.stats\"); p.sort_stats('time').print_stats(20)"

-    How to run Wireshark on Mac OS X

        # Install XQuartz, install Wireshark.
        # Run XQuartz via Spotlight
        # Open a new Terminal, run:
        
        open /Applications/Wireshark.app/
        
        # A new xterm instance opens, but Wireshark isn't visible. In the xterm instance run:
        
        export DISPLAY:=0
        
        # Wireshark should now be visible.
        
-    Useful httrack one-liner to index a site and all 'near' non-HTML resources and all first-links away in useful directory structure.

        httrack http://www.cs.columbia.edu/~smaskey/CS6998/ -W -O "/Users/ai/websites/smaskey" --extended-parsing --mirrorlinks --structure=4 +*.pdf
    
-	Setting up SAMBA on RedHat
	-	`yum install samba samba-client`
	-	Replace `/etc/samba/smb.conf` contents with the following, replacing `${ip_address}` with local IP address:

			[global]
			
			workgroup = DCL
			local master = no
			preferred master = no
			server string = %L Samba %v
			interfaces = 127.0.0.1 ${ip_address}
			socket address = ${ip_address}
			log file = /var/log/samba/log.%m
			max log size = 50
			security = share
			passdb backend = tdbsam
			load printers = no
			cups options = raw
			
			[root]
			
			comment = Root Directory
			path = /
			read only = no
			writable = yes
			printable = no
			public = yes
			force user = root

	-	Add a root user to SAMBA by executing

			smbpasswd -a root

	-	Set SAMBA to load on startup by executing:

			chkconfig smb on && chkconfig nmb on

	-	Enable SAMBA by executing:

			service smb start && service nmb start

	-	Browse to `\\${hostname}`

-	Setting up IP connectivity on a fresh RedHat install
	-	Edit `/etc/sysconfig/network-scripts/ifcfg-eth0` and make sure at least the following lines are present (adjust values as appropriate):

			DEVICE=eth0
			BOOTPROTO=none
			DNS1=172.19.1.83
			DNS2=172.18.10.55
			DOMAIN=datcon.co.uk
			GATEWAY=10.224.0.1
			IPADDR=10.224.104.2
			NETMASK=255.255.0.0
			ONBOOT=yes
			DEFROUTE=yes

	-	Assign the IP address to the Ethernet interface:

			ip addr add 10.224.104.2/16 broadcast 10.224.255.255 gateway 10.224.0.1 dev eth0

	-	Add a default IP route to the default gateway:

			route add default gw 10.224.0.1 eth0

	-	Turn up the Ethernet interface:

			ifconfig eth0 up

	-	Set IP connectivity to enable in startup:

			chkconfig network on

-    Install latest GCC on Mac OS X

        # Install homebrew.
        brew update
        brew tap homebrew/dupes
        brew install gcc --use-llvm --enable-all-languages --enable-profiled-build
        
-    To get GCC 4.7 working on Mac we have to force distutils to give up using `-Qunused-arguments`. It's painful, so we hack it real hard:

        import distutils.sysconfig
        for key in distutils.sysconfig._config_vars:
            if key in ['CONFIG_ARGS', 'PY_CFLAGS', 'CFLAGS']:
                distutils.sysconfig._config_vars[key] = distutils.sysconfig._config_vars[key].replace("-Qunused-arguments ", "")
