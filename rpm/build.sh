#!/bin/bash

##for check
if [ $# -ne 3 ] && [ $# -ne 4 ]; then
	echo "Usage: ./build.sh <*.spec> <version> <qa_version> [package_install_prefix]"
	exit
fi
if [ $# -eq 4 ];then
	./rpm_create -p $4 -v $2 -r $3 $1 -k
else
	./rpm_create -v $2 -r $3 $1 -k
fi
