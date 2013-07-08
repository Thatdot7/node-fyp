Smart Power Board
=================================================

By Moses Yi-Jie Wan (aka Thatdot7)

The "node-fyp" repository is a web server, written for the Raspberry Pis, which can remotely control the states of a 4-plug power board. It is designed to be a Final Year Project for Electrical Engineering. Because this project allows the Raspberry Pis to interact with AC mains power, caution is advised when creating the circuitory.

The current implementation is rather static, but I am improving it to be a lot more customizable as I progress through my Final Year Project. Though, there are a few features that are up and running.

This program doesn't not guarantee safety around AC Mains Power. **YOU HAVE BEEN WARNED**.

Features include:-
- [x] Manual Control of each power-plug
- [x] Scheduling and Timing Policies for each plug
- [x] Plugs cans have a label
- [x] Wifi connection settings can be changed within the interface
- [ ] Ability to connect to new networks
- [ ] Range Extension settings in the interface
 
Getting Started
------------------------------------------- 
- Clone the repository
- Connect the powerpoint controllers to pins 3,5,7,11
- Open up /etc/rc.local (sudo nano /etc/rc.local)
- Add the following lines just before "exit 0"
  - `python %clone_location%/node-fyp/server.py&`
  - `python %clone_location%/node-fyp/test_broadcast_receive.py&`
  - `%clone_location%` is the path where you clone the repository. Please write the **full path name**.

Once this is all done, you should be able to enter the IP address of your Raspberry Pi then enjoy the web interface.

Requirements
-------------------------------------------
Python libraries required:-
- Tornado Web Server
- python-crontab
- python-dateutil
- python-configobj

Linux packages required:-
- at
- cron
- wpa_supplicant / wpa_cli

Acknowledgements
-------------------------------------------
- Dr Jonathan Li, Supervisor for this project
- Brendan Wreford, for bouncing ideas
- Ricky Wong Yung Fei, for bouncing ideas and teaching me Linux skills
- Martin, for basically creating the prototype
- All the software developments that made the packages and libraries used in the project
- Raspberry Pi Team
