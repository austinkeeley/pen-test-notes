# Setting up the Virtual Machines

We will have two virtual machines in use:
- A Kali Linux machine that we'll use for attacking
- A Metasploitable Linux machine that will act as a target

## VirtualBox
You can use any VM hosting environment, but I like to use VirtualBox because it's free
and seems to be more straight forward than VMWare.  I also happen to already be using it
with [Vagrant](http://www.vagrantup.com/).

Download the latest .deb package from the VirtualBox Linux binaries [download page](https://www.virtualbox.org/wiki/Linux_Downloads) and install it with

    sudo dpkg -i virtualbox-4.3_4.3.12-93733~Ubuntu~precise_amd64.deb

That should create menu shortcuts for the VirtualBox manager.  

## Kali Linux (Formerly BackTrack Linux)
1. Download the ISO image of the latest version of Kali Linux from the [official download page](http://www.kali.org/downloads/).  
2. In the VirtualBox manager, create a new VM.
3. Good settings:
    - 4096 MB of RAM
    - Enable PAE/NX on the processor
    - Enable 3D Acceleration
    - 16 GB of disk storage (**Required!** If you use the default 8 GB, the system will fail to boot up)
    - Two network adaptors
        - NAT (for Internet access through your host)
        - Internal Network (to connect to the target Metasploitable machine).  Network name can be anything.
4. Add the ISO image to the virtual DVD-ROM drive and boot up the VM.
5. Select install from the bootup menu and go with all the default options.
6. Be sure to set up a network mirror for software updates.
7. For a hostname, pick something easy to remember.  I called this one `austin-kali.home`.
8. Reboot.
9. Take a snapshot.
10. We'll want to install the VirtualBox Guest Additions so that it's easier to work with the VM.  The version of Kali doesn't come with the Linux headers so we'll need to get them.  See [this page](http://docs.kali.org/general-use/kali-linux-virtual-box-guest) for more details.
        apt-get update && apt-get install -y linux-headers-$(uname -r)
        cd /media/cdrom
        sh VBoxLinuxAdditions.run
11. You can now increase the screen resolution to something better.  Change the desktop wallpaper while you're at it. The black background with a black application bar is not a good choice.
12. Add a second non-root user and give him/her sudo privilages.
    - `adduser` (follow the prompts)
    - `adduser <your name> sudo`
    - Edit the `.bashrc` file to fix the path (only `root` has this initially).
            export PATH=$PATH:/usr/sbin
13. Assign a static IP to your internal network adapter
        sudo vim /etc/networking/interfaces
    - Find the interface for the internal network (probably `eth1`) and remove the DHCP setting.
    - Add the following:
            auto eth0
            iface eth0 inet static
            address 192.168.2.100
            netmask 255.255.255.0
            network 192.168.2.0
            broadcast 192.168.2.255
    - Note that for this, we'll be using `192.168.2.x` for the internal network.  Your NAT settings are most likely using `10.0.0.x` for the adapter that's connected through the host and a lot of people use `192.168.1.x` for their home networks, so this is to keep things from getting too confusing.  

### Nessus
14. Download the Nessus Home .deb file from the [Nessus](http://www.tenable.com/products/nessus/select-your-operating-system) website. 
15. Install it using
        sudo dpkg -i nessus-**.deb
16. Fire up the nessus server 
        sudo /etc/init.d/nessusd start
17. Open a web browser to https://localhost:8834 (note the https)
18. Follow the setup instructions and register for a subscription key.
19. Upgrade all the installed packages.  This takes a while.  You can either do this through the UI or from the command line with
        sudo apt-get update && sudo apt-get upgrade
20. Add the Metasploitable host to your `/etc/hosts` file.  You haven't build that VM yet, but if you know what static IP you plan on using (recommended to use `192.168.2.101`) and the hostname (recommended is `metasploitable.home`) then you can add it now.
21. Create user accounts for Nessus.

### Metasploit
21. You need to register to get updates, so run the Metasploit Community application and it will launch the web server and prompt you for all your info.  This *should* get all the updates, but to get them in the future
        sudo msfupdate
22. If you plan on using the Community Edition web application, register a new username.

### Other random things
23. Install Chrome (I like to sync my browser settings)

## Metasploitable
This one is a lot easier to set up.
1. Download the Metasploitable2 VM from the [SourceForge page](http://sourceforge.net/projects/virtualhacking/files/os/metasploitable/).
    - The VM is intended to work on VM Ware, but you can still use the disk image with VirtualBox.
2. Create a new VM and select the `.vmdk` file from the Metasploitable download as the virtual disk.
3. Good settings:
    - 1024 MB RAM
    - Set network adapter internal network **only**.
3. Boot up and login with username/password `msfadmin`.
4. Set a static IP address in the same way as the Kali Linux machine.  I use `192.168.2.101` for this machine.
5. From the Kali Linux machine, ping this machine and make sure it gets a response.
6. From teh Kali Linux machine, open a web browser and go to http://192.168.2.101 and make sure the default Metasploitable web page comes up.   
