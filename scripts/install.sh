#!/bin/bash

if [ $# -eq 0 ]; then
    >&2 echo "No arguments supplied"
    >&2 echo "Possible arguments are: kernel, boot, dependencies, dhcp"
    exit
fi

if grep -q kernel <(echo $@); then
    if [ ! -f /etc/modules ]; then
        >2& printf "Couldn't Find kernal module file\nManualy add dwc2 to modules"
    else
        if grep -v -q "dwc2" /etc/modules; then
            >2& printf "dwc2 already in kernel modules"
        else
            echo "dwc2" | tee -a /etc/modules
        fi
        if grep -v -q "g_ether" /etc/modules; then
            >2& printf "g_ether already in kernel modules"
        else
            echo "g_ether" | tee -a /etc/modules
            echo "installed kernel module"
        fi
    fi
fi

if grep -q boot <(echo $@); then
    if [ ! -f /boot/config.txt ]; then
        >&2 printf "Boot config file does not exist\nNot installing boot"
    elif grep -v -q -P "(#\s*dtoverlay\s*=\s*\".*\"|dtoverlay\s*=\s*\"\s*\")" /boot/config.txt; then
        >&2 printf "already dtoverlay in boot config\nManualy add \"dwc2\" to that list"
    else
        echo "dtoverlay=dwc2" | tee -a /boot/config.txt
        echo "installed boot options"
    fi
fi

if grep -q dependencies <(echo $@); then
    apt install python3 python3-pip isc-dhcp-server
    pip3 install flask
fi

if grep -q dhcp <(echo $@); then
    if [ -f /etc/dhcp/dhcpd.conf ]; then
        printf "subnet 10.50.40.0 netmask 255.255.255.0{\n\trange 10.50.40.10 10.50.40.20\n}" >> /etc/dhcp/dhcpd.conf
        echo "Installed dhcp config"
    else
        >&2 printf "Couldn't find isc-dhcp-server configuration, are you sure it's installed?"
    fi
    if [ -f /etc/dhcpcd.conf ]; then
        printf "interface usb0\nstatic ip_address=10.50.40.1" >> /etc/dhcpcd.conf
        echo "Installed network interface config"
    else
        >&2 printf "Couldn't set static ip.\nPlease set ip of interface usb0 to '10.50.40.1'"
    fi
fi
echo
