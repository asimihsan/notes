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
    