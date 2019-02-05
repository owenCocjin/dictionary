#!/bin/bash
dirs=("/usr/local/bin")
for i in ${dirs[@]}; do
	if [[ -d "$i" ]]; then
		cp ./dictionary $i
		echo "Copying script to $i..."
	fi
done
echo "Done!"
