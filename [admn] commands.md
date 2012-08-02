## Commands

-   `tshark` HTTP traffic on loopback port 8000:

        sudo tshark -i lo -V -T text -f "tcp port 8000" -d "tcp.port==8000,http" -R "http.request"
