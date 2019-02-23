#!/bin/bash

#Set curUser
curUser=$( logname )

#Checks if running as root. Asks user to run as root if not already
if [[ "$( whoami )" != 'root' ]]; then
	echo "Run as root (I have to remove files in /usr/local/bin)!"
	exit 1
fi

#Remove main file
rm -f /usr/local/bin/dictionary 2>/dev/null
if [[ -f "/usr/local/bin/dictionary" ]]; then
	echo "\e[31m[\e[34m|\e[31mX]\e[0m Failed to remove main dictionary program!
	(You can try manually removing /usr/local/bin/dictionary and re-running uninstaller)"
	exit 1
fi

#Remove .dictionary directory & subfiles
rm -rf /home/$curUser/.dictionary 2>/dev/null
if [[ -d "/home/$curUser/.dictionary" ]]; then
	echo "\e[31m[\e[34m|\e[31mX]\e[0m Failed to remove .dictionary!
	(You can try manually removing /home/$curUser/.dictionary and re-running uninstaller)"
	exit 1
fi

#Remove /tmp/dictionary
rm -rf /tmp/dictionary 2>/dev/null
if [[ -d "/tmp/dictionary" ]]; then
	echo -e "\e[31m[\e[34m|\e[31mX]\e[0m Failed to remove temp directory! This shouldn't be an issues as files \
	in /tmp are normally deleted automatically.
	(You can try manually removing /tmp/dictionary and re-running uninstaller)"
fi

#Remove /etc/dictionary
rm -rf /etc/dictionary
if [[ -d "/etc/dictionary" ]]; then
	echo "\e[31m[\e[34m|\e[31mX]\e[0m Failed to remove temp directory!
	(You can try manually removing /etc/dictionary and re-running uninstaller)"
fi

echo "Everything's gone! Thanks for using my dictionary!"
