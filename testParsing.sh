#!/usr/bin/bash

for i in `ls cdslTests`; do
	echo $i
	./parseCDSL.py cdslTests/$i;
	echo "----------------"
	echo ""
done;


