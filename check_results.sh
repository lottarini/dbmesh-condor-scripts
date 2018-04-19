#!/bin/bash
if [ "$#" -eq 1 ] && [ -d $1 ]; then
	find $1 -name main.out -exec ls -ltha \{\} \; -exec tail -1 \{\} \; -exec echo "" \;
else
	echo "pass a valid directory path"
fi
