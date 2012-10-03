#	transmission-cli

-	Build transmission from source.

```
sudo apt-get install build-essential automake autoconf libtool pkg-config intltool libcurl4-openssl-dev libglib2.0-dev libevent-dev libminiupnpc-dev libminiupnpc5 libappindicator-dev

wget http://download.transmissionbt.com/files/transmission-2.61.tar.bz2
bunzip2 transmission-2.61.tar.bz2
tar -xvf transmission-2.61.tar
rm -f transmission-2.61.tar
cd transmission-2.61/

./configure --disable-gtk --disable-mac --enable-lightweight
make
sudo make install

cd ..
rm -rf transmission-2.61/ 
```

-	Copy on relevant `settings.json` and `transmission.sh` file into e.g. `~/transmission`.
-	Run `./transmission.sh`.

