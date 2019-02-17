#!/bin/bash

#Set curUser
curUser=$( logname )

#Checks if running as root. Asks user to run as root if not already
if [[ "$( whoami )" != 'root' ]]; then
	echo "Run as root (I have to write to /usr/local/bin/)!"
	exit 1
fi

#Copy main script to /usr/local/bin (Normally part of the path)
if [[ -d "/usr/local/bin" ]]; then
	echo "Copying script to /usr/local/bin/..."
	cp ./dictionary /usr/local/bin
	if [[ "$?" != '0' ]]; then
		echo -e "\e[31m[\e[34m|\e[31mX]\e[0m Failed to copy to /usr/local/bin/!"
		exit 1
	fi
else
	echo -e "\e[31m[\e[34m|\e[31mX]\e[0m /usr/local/bin not found!"
	exit 1
fi

#Create .dictionary folder in home
echo "Creating .dictionary folder..."
if [[ -d "/home/$curUser/.dictionary" ]]; then
	echo -en "\e[92m[\e[34m|\e[92mX]\e[0m Folder already exists, over-write(y/n)?: "
	read rec
	if [[ "$rec" == 'y' ]] || [[ "$rec" == 'yes' ]]; then
		rm -rf /home/$curUser/.dictionary
		mkdir /home/$curUser/.dictionary
	else
		echo -e "\tLeaving .dictionary alone!"
	fi
else
	cp -r ./.dictionary /home/$curUser/
fi

#Copy dictionary_py to .dictionary
if [[ -d "/home/$curUser/.dictionary" ]]; then
	#Copy dictionary_py to .dictionary
	echo "Copying dictionary_py to /home/$curUser/.dictionary/"
	cp -r ./dictionary_py /home/$curUser/.dictionary
	if [[ "$?" != '0' ]]; then
		echo -e "\t\e[92m[\e[34m|\e[92mX]\e[0m Copying of dictionary_py failed!"
		exit 1
	fi

	#Copy word save file to .dictionary
	echo "Copying saved_words to /home/$curUser/.dictionary/"
	cp ./saved_words.txt /home/$curUser/.dictionary/
	chown $curUser:$curUser /home/$curUser/.dictionary/saved_words.txt
	if [[ "$?" != '0' ]]; then
		echo -e "\t\e[92m[\e[34m|\e[92mX]\e[0m Creation/Editting of saved_words.txt failed!"
		exit 1
	fi

else
	#Checks if .dictionary exists/was created
	echo -e "\e[31m[\e[34m|\e[31mX]\e[0m /home/$curUser/.dictionary not found!"
	exit 1
fi


echo "Done!"
