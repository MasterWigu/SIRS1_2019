#!/usr/bin/env bash

apt-get update

#enable forwarding
sysctl -w net.ipv4.ip_forward=1


#enable NAT
iptables -P FORWARD ACCEPT
iptables -F FORWARD
iptables -t nat -F
iptables -t nat -A POSTROUTING  -o enp0s10 -j MASQUERADE

ip route delete default via 10.0.2.2 

iptables -P FORWARD DROP 
iptables -A FORWARD -p icmp -j ACCEPT
iptables -A FORWARD -d 192.168.50.10/24 -p tcp --dport 443 -j ACCEPT
iptables -A FORWARD -s 192.168.50.10/24 -p tcp --sport 443 -j ACCEPT
iptables -A FORWARD -s 192.168.50.10/24 -p tcp --sport 4347 -j ACCEPT
iptables -A FORWARD -d 192.168.50.10/24 -p tcp --dport 4347 -j ACCEPT 
#allow internet to client machines
iptables -A FORWARD -s 192.168.52.0/24  -j ACCEPT
iptables -A FORWARD -d 192.168.52.0/24  -j ACCEPT
iptables-save