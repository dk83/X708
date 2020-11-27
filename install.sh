##!/bin/bash
#
Init="/etc/init.d";
Bin="/usr/local/sbin";
# Link Protection.py
File="Protection"
sudo ln -s "${PWD}/${File}.init"  "${Init}/${File}"
sudo ln -s "${PWD}/${File}.py"    "/etc/${File}"
sudo ln -s "${PWD}/${File}.py"    "${Bin}/${File}"
sudo update-rc.d "${File}" defaults

# Link PowerOff.sh && Reboot.sh
sudo ln -s "${PWD}/PowerOff.sh" "${Bin}/PowerOff"
sudo ln -s "${PWD}/Reboot.sh"   "${Bin}/Reboot"
sudo ln -s "${PWD}/Battery.py"   "${Bin}/Battery"

# Prepare Logging
Log="/var/log/Do/Protection.py";
sudo sh -c "echo ' ' > $Log";
