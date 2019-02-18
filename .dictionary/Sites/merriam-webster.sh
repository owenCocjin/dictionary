#!/bin/bash

#Get the word html
curl -L https://www.merriam-webster.com/dictionary/$( cat dict_pipe ) > dict_file 2>/dev/null
if [[ "$?" == '6' ]]; then
	echo "curl could not resolve host (Check internet connection)"
elif [[ "$?" == '0' ]]; then
	echo "ugh"
else
	:
fi

#Cut out only the relevent tag
#sR==Starting row
#sR will always be 318, but it is decided dynamically just in case the dictionary
#webside changes (This will potentially prevent the script from breaking)
sR=$( grep -n 'class="hword"' dict_file | awk -F':' 'NR==1 { print $1 }' )
awk -v sR="$sR" 'NR>sR {print > "d"}' dict_file

#Stripping html tags and identifying needed variables
head -n 500 d | /home/$USER/.dictionary/dictionary_py/removeTags > dict_file
partOfSpeach=$( awk -F'[^a-zA-Z]' 'NR==1 {print $1}' dict_file )
pronunciation='\ '$( grep -e 'ˈ' dict_file | head -n 1 | sed 's/[|\ ]*//')    #Assume pronunciation starts with a \

#Create string and send to dict_pipe
toSend=${pronunciation}:${partOfSpeach}
echo "$toSend" > dict_pipe &
echo -n > d
grep '^:' dict_file | awk -F': ' 'NR<=5 {print toupper(substr($2,1,1)) substr($2,2) >> "d"}'
