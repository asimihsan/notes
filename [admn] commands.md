## Commands

-   `tshark` HTTP traffic on loopback port 8000:

        sudo tshark -i lo -V -T text -f "tcp port 8000" -d "tcp.port==8000,http" -R "http.request"

-	`ffmpeg` conversion for iPad:

		ffmpeg -i ${input_file} -acodec libfaac -ac 2 -ab 192k -s 1024x768 -vcodec libx264 -vprofile baseline -tune film -preset slower -b:v 1200k -f mp4 -threads 0 ${output_file}

-	sort `du -h` output

		du | sort -nr | cut -f2- | xargs du -hs