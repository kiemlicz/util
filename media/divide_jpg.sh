#!/bin/bash

#divides the input jpeg of size 3840x1080 into two 1920x1080

if [ -z $1 ]
then
	echo "Input image required"
	exit 1
fi

IMAGE=$1

convert -extract 1920x1200+0+0 $IMAGE l.jpg
convert -extract 1920x1200+1920+0 $IMAGE r.jpg
