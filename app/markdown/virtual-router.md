Virtual Router
================

So in order to get good at understanding how networks do things, you'll need to create a slightly more complicated
network.  The internal network setting in VirtualBox basically puts everything on the same network; e.g. your attackers
and your targets are both on the same subnet so it's not really giving you a realistic view of attacking from the 
outside.  

We're going to build two networks: an *internal* and an *external* network.  The
internal network will have our target hosts (what we're attacking).  The external network will have our attacking computers, plus
any computers that make external services (these are non-competiting hosts, e.g. a web server that a victim host may be connecting 
to).  

**Internal Network**
    
    VirtualBox network name: internal_net
    Interface eth1
    192.168.3.0/24
    Starting address: 192.168.3.100
    Ending address: 192.168.3.110
    Static IP assignment
    Gateway: 192.168.3.1   <-- This will be the IP of one our NICs on the router
    

**External Network**

    VirtualBox network name: external_net
    Interface eth0
    192.168.4.0/24
    Starting address: 192.168.4.100
    Ending address: 192.168.4.110
    DHCP
    Gateway: 192.168.4.1

We can also have a third network being the real Internet by giving our router a third network interface that uses NAT through
the host.  Honestly though, it's easier if you just configure your hosts to have an extra NAT interface if you want Internet access.

1. Download your favorite Linux distribution.  I'm goign to use Debian 7.5.
2. Create a new virtual machine in VirtualBox called "Debian Router".
    * 512 MB RAM
    * 8 GB Disk (we can probably use less, but we'll just go with the default)
3. Modify your network settings so you have 2 network cards
    * Internal Networking, named `internal_net`. This will be `eth0` as recognized by Linux.
    * Internal Networking, named `external_net`. This will be `eth1` as recognized by Linux.
    * (Optional) NAT, in case we want to connect our router to the Internet.
4. Add your Debian ISO to your virtual machine and install Debian.  Opt for a minimal install since we don't need
   anything fancy.  No desktop or anything.  Just the base OS.
5. When prompted for a hostname, I used `debian-router`.

5. Most routers have some kind of DHCP server running on them.  This is optional, but we might as well have it.  It 
   will make adding new hosts to our external network faster.  We could do this for the internal network, but since we'll be
   attacking those, it's better if they have static IP addresses.
  
        sudo apt-get install dhcp3-server

6. Add the following to `/etc/dhcp/dhcpd.conf`

        subnet 192.168.4.0 netmask 255.255.255.0 {
            range 192.168.4.100 192.168.4.110;
            option broadcast-address 192.168.4.255; ## broadcast
            option routers 192.168.4.1; ## router IP
        }

7. Assign your router interfaces static IPs.  Add/modify the following to `/etc/network/interfaces`

        # Internal Network
        auto eth1
        iface eth1 inet static
            address 192.168.3.1
            netmask 255.255.255.0
            network 192.168.3.0
            broadcast 192.168.3.255

        # External network
        auto eth0
            iface eth0 inet static
            address 192.168.4.1
            netmask 255.255.255.0
            network 192.168.4.0
            broadcast 192.168.4.255

        gateway 192.168.4.1

        # Optional NAT-based network that will get an IP from the VirtualBox software on the host
        # auto eth2
        # iface eth2 inet dhcp

8. Restart networking

        service networking restart

8. Start (or restart) the DHCP server

        service isc-dhcp-server start

9. At this point, try to start up a virtual machine with a network interface connected to the network `external_net` and make
sure it can get an IP address via DHCP.

10. Time to set up routing.  I wrote a script based on the Debian routing tutorial.  
        #!/bin/sh

        PATH=/usr/sbin:/sbin:/bin:/usr/bin
       
        # Modify these for your network cards
        EXTERNAL_IFACE=eth0
        INTERNAL_IFACE=eth1
        LOOPBACK_IFACE=lo

        #
        # delete all existing rules.
        #
        iptables -F
        iptables -t nat -F
        iptables -t mangle -F
        iptables -X

        # Always accept loopback traffic
        iptables -A INPUT -i $LOOPBACK_IFACE -j ACCEPT

        # Allow established connections, and those not coming from the outside
        # This is a legit rule that would be used in a real firewall, but for our lab we can not use it
        # iptables -A INPUT -m state --state ESTABLISHED,RELATED -j ACCEPT
        # iptables -A INPUT -m state --state NEW -i $INTERNAL_IFACE -j ACCEPT
        # iptables -A FORWARD -i $EXTERNAL_IFACE -o $INTERNAL_IFACE -m state --state ESTABLISHED,RELATED -j ACCEPT
        # Don't forward from the outside to the inside.
        # iptables -A FORWARD -i $EXTERNAL_IFACE -o $INTERNAL_IFACE -j REJECT

        # Allow outgoing connections from the LAN side.
        iptables -A FORWARD -i $INTERNAL_IFACE -o $EXTERNAL_IFACE -j ACCEPT
        
        # Allow incoming connections from the external side
        iptables -A FORWARD -i $EXTERNAL_IFACE -o $INTERNAL_IFACE -j ACCEPT

        # Masquerade. You probably don't need this unless you want to connect to the outside.
        # iptables -t nat -A POSTROUTING -o $EXTERNAL_IFACE -j MASQUERADE

        # Enable routing.
        echo 1 > /proc/sys/net/ipv4/ip_forward

11. Connect a virtual machine to the `internal_net` network and give it a static IP.  Add this to its `/etc/network/interfaces`.

        auto eth0
        iface eth0 inet static
        address 192.168.3.100
        netmask 255.255.255.0
        network 192.168.3.0
        broadcast 192.168.3.255

12. Try pinging the external host from the internal host and vice versa.  

You should now have a working router.  Now what to do with it?  You can add various firewall rules to filter traffic going to the
internal network.  
