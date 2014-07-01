Host List
==========
This is a list of machines available in the security lab.

## Hosts elgible for attack

### Metasploitable Hosts
        
    192.168.3.100
    192.168.3.101

Metasploitable is a purposefully insecure Linux distribution.  It has many obvious security holes that can be easily exploited.
These hosts are open for attack.

## Hosts not elgible for attack

### Snort IDS

    192.168.3.200

Snort is an intrusion detection system that monitors the internal network.  It is being used to make sure the network stays online
and to collect some data about the attacks.  It is not open for attack.

### Debian Desktop

    192.168.3.201

This is a standalone Debian host used for various purposes, mostly for transfering files to the internal network and performing admin
tasks.  It usually isn't online, but try not to attack it. 

### External Non-Participant Hosts

    192.168.4.x

There are several hosts on the external network that are considered non-participants and are being used to simulate 3rd party resouces.
In general, do not attack hosts on the `192.168.4.0/24` subnet.
