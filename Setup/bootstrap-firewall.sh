#!/usr/bin/env bash

apt-get update
apt-get -y install fwbuilder

#enable forwarding
sysctl -w net.ipv4.ip_forward=1


#enable NAT
iptables -P FORWARD ACCEPT
iptables -F FORWARD
iptables -t nat -F
iptables -t nat -A POSTROUTING  -o enp0s10 -j MASQUERADE

ip route delete default via 10.0.2.2 