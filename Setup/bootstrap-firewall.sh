#!/usr/bin/env bash

apt-get update
apt-get -y install fwbuilder

#enable forwarding
sysctl net.ipv4.ip_forward=1

#enable NAT
#iptables -P FORWARD ACCEPT
#iptables -F FORWARD
#iptables -t nat -F
#iptables -t nat -A POSTROUTING  -o ens9 -j MASQUERADE