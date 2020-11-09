#!/bin/bash
#
Log="/var/log/X708.log"
gpio export 5 in;
gpio -g mode 5 in;
gpio export 12 out;
gpio -g mode 12 out && gpio -g write 12 1;

wall "Shutdown & USV Power OFF in 15s"; sleep 15s
gpio -g mode 13 out && gpio -g write 13 1;
# Prepare USV for Power Off
wall "|--->>>   POWER OFF NOW   <<<---|";
sleep 6s; # Simulate Power Button Press 6s -> Shutdown Raspbian and Power Off
sudo sh -c "echo '$(date +%H:%M) |--->>>   POWER OFF   <<<---|' >> $Log";
gpio -g write 13 0; sudo poweroff --poweroff;
