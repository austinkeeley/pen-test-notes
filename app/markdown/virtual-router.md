Virtual Router
================

So in order to get good at understanding how networks do things, you'll need to create a slightly more complicated
network.  The internal network setting in VirtualBox basically puts everything on the same network; e.g. your attackers
and your targets are both on the same subnet so it's not really giving you a realistic view of attacking from the 
outside.  

We're going to build two networks.  Both of which are considered, "internal" by VirtualBox, but one will be simulating
an internal network while the other will be simulating an external net where crazy stuff happens.

Here's a quick look at what the networks will look like.

**Internal Network**
    
    192.168.3.0/24
    Starting address: 192.168.3.100
    Ending address: 192.168.3.110
    DHCP Enabled
    VirtualBox network name: internal_net
    Gateway: 192.168.3.1   <-- This will be the IP of one our NICs on the router
    

**External Network**

    192.168.4.0/24
    Starting address: 192.168.4.100
    Ending address: 192.168.3.110
    VirtualBox network name: internal_net
    Gateway: 192.168.3.1   <-- This will be the IP of one our NICs on the router

Fortunately, we can build a virtual router pretty quickly.  

1. Download your favorite Linux distribution.  I'm goign to use Debian 7.5.
2. Create a new virtual machine in VirtualBox called "Debian Router".
    * 512 MB RAM
    * 8 GB Disk (we can probably use less, but we'll just go with the default)
3. Modify your network settings so you have 2 network cards
    * Internal Networking (name the network anything; I'm going to use "internal_net") because this will be the
      interface that connects to the private network.
    * The other network card can connect anywhere.  We'll have it use NAT for now so our router will be able to
      route to the Internet.  Later, we'll make this point to a second internal net that will simulate being 
      on the outside.
4. Add your Debian ISO to your virtual machine and install Debian.  Opt for a minimal install since we don't need
   anything fancy.  No desktop or anything.  Just the base OS.
5. When prompted for a hostname, I used `debian-router`.
5. Most routers have some kind of DHCP server running on them.  This is optional, but we might as well have it.  It 
   will make adding new hosts to our internal network easier.  
        sudo apt-get install dhcp3-server

6. Add the following to `/etc/dhcp/dhcpd.conf`
        subnet 192.168.3.0 netmask 255.255.255.0 {
            range 192.168.3.100 192.168.1.110;
            option broadcast-address 192.168.3.255; ## broadcast
            option routers 192.168.3.1; ## router IP
        }

7. Assign your router a static IP
        ifconfig eth1 up 192.168.3.1 up  # Note that it's eth1 because it's the NIC that's connected to internal_net

8. Start (or restart) the DHCP server
        service isc-dhcp-server start

9. At this point, I connected a Metasploitable Linux machine to the `internal_net` network and did `dhclient` and 
   successfully received an IP address.
