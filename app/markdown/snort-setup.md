Snort Setup
============

1. Create a new VM:
    - 1024 MB RAM
    - 8 GB hard drive
    - NAT network connection (to download Snort + rules, will switch to internal network later)
    - Using Debian 7.5 x64 
    - Hostname: `snort`

2. Pre-requisite software

        apt-get update
        apt-get install tcpdump
        apt-get install libcap-dev
        apt-get install libpcre3
        apt-get install libpcre3-dev
        apt-get install libdnet
        apt-get install libdnet-dev
        apt-get install libdumbnet-dev
        apt-get install libdaq0
        apt-get install libdaq-dev
        
        # I don't think barnyard2 binaries are hosted by Debian, so we'll have to compile 
        # it.  It has a few other requirements.
        apt-get install libtool
        apt-get install autoconf
        git clone https://github.com/firnsy/barnyard2.git
        cd barnyard2
        ./autogen.sh
        ./configure
        make && make install

3. Installing Snort

        wget http://www.snort.org/dl/snort-current/snort-2.9.6.1.tar.gz 
        tar -xvf snort-2.9.6.1.tar.gz
        cd snort-2.9.6.1
        ./configure
        make
        make install
There might be a few other dependencies that may or may not already be on your system (e.g. zlib, bison, etc.).
        
4. Switch your virtual network card from NAT to the `internal_net` network.  Be sure you turn on promiscuous mode, otherwise
Snort won't be able to see traffic on your network.

5. Register with snort.org and download the latest free ruleset.  
        
