#!/bin/bash
if [ -d $1 ]; then
	cd $1
	find . -name main.out -exec ls -ltha \{\} \; -exec tail -1 \{\} \;
	cd ..
else
	echo "$1 is not a directory"
fi
