#!/bin/bash

#Get the word html
curl -L https://www.merriam-webster.com/dictionary/$( cat dict_pipe ) > dict_file 2>/dev/null

if [[ "$?" == '6' ]]; then
	error "curl could not resolve host (Check internet connection)"
elif [[ "$?" == '0' ]]; then
	error
else
	:
fi

#Cut out only the relevent tag
#sR==Starting row, eR=Ending row
#sR will waways be 318, but it is decided dynamically just in case the dictionary
#webside changes (This will potentially prevent the scritp from breaking)
sR=$( grep -n 'class="hword"' dict_file | awk -F':' 'NR==1 { print $1 }' )
awk -v sR="$sR" 'NR>sR {print > "d"}' dict_file

#Writes the stripped webpage into dict_file
cat d | /home/$USER/.dictionary/dictionary_py/removeTags > dict_file
partOfSpeach=$( awk -F'[^a-zA-Z]' 'NR==1 {print $1}' dict_file )
pronunciation=$( grep -e 'ˈ' dict_file | head -n 1 | sed 's/ˈ//')    #Assume pronunciation starts with a \

#Removes leading '\' for proper output
if [[ "${pronunciation:0:1}" != '\' ]];then
	pronunciation='\ '$pronunciation
fi
echo -n > ./d    #Wipe d file to store definitions. This will make them easier to save
grep '^:' dict_file | awk -F': ' 'NR<=5 {print toupper(substr($2,1,1)) substr($2,2) >> "d"}'
