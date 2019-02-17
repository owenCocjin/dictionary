#!/bin/bash

#Set curUser
curUser=$( logname )

#Copy main script to /usr/local/bin (Normally part of the path)
if [[ -d "/usr/local/bin" ]]; then
	echo "Copying script to /usr/local/bin..."
	cp ./dictionary /usr/local/bin
	if [[ "$?" != '0' ]]; then
		echo -e "\e[31m[\e[34m|\e[31mX]\e[0m Failed to copy to /usr/local/bin!"
	fi
else
	echo -e "\e[31m[\e[34m|\e[31mX]\e[0m /usr/local/bin not found!"
	exit 1
fi

#Create .dictionary folder in home
echo "Creating .dictionary folder..."
if [[ -d "/home/$curUser/.dictionary" ]]; then
	echo -e "\e[92m[\e[34m|\e[92mX]\e[0m file already exists, over-write(y/n)?: "
	read rec
	if [[ "$rec" == 'y' ]] || [[ "$rec" == 'yes' ]]; then
		rm -rf /home/$curUser/.dictionary
		mkdir /home/$curUser/.dictionary
	else
		echo -e "\tLeaving .dictionary alone!"
	fi
else
	mkdir /home/$curUser/.dictionary
fi

if [[ -d "/home/$curUser/.dictionary" ]]; then
	#Copy dictionary_py to .dictionary
	echo "Copying dictionary_py to /home/$curUser/.dictionary..."
	cp -r ./dictionary_py /home/$curUser/.dictionary
	if [[ "$?" != '0' ]]; then
		echo -e "\t\e[92m[\e[34m|\e[92mX]\e[0m Copying of dictionary_py failed!"
	fi
else
	#Checks id .dictionary exists/was created
	echo -e "\e[31m[\e[34m|\e[31mX]\e[0m /home/$curUser/.dictionary not found!"
	exit 1
fi

echo "Done!"
