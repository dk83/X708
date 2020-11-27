#!/bin/bash
Log="/var/log/X708.log";
gpio export 5 in;
gpio export 12 out;
gpio -g mode 5 in;
gpio -g mode 12 out;
gpio -g mode 13 out;
gpio -g write 12 1;

echo "- Reboot in 3s..."; sleep 3s;
#Simulate Power Button Press 2s -> Reboot USV & Raspbian
gpio -g write 13 1 && sleep 2s && gpio -g write 13 0;
wall "|--->>>   REBOOT NOW   <<<---|";
sudo sh -c "echo '$(date +%H:%M) |--->>>   REBOOT NOW   <<<---|' >> $Log";
sudo poweroff --reboot;
