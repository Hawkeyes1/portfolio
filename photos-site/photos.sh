#!/bin/bash

# change jpgs to JPGs, create 20% and 5% versions of all files.

for file in `ls big | grep jpg`; do mv big/$file `echo big/$file | sed 's/\(.*\.\)jpg/\1JPG/'`; done

for file in `ls signatures`; 
	do
	if [ ! -f big/$file ]
	then
	rm signatures/$file
	fi
done


for file in `ls big | grep JPG`; 
	do 
	if [ -f signatures/$file ] 
	then
	echo "Bypassing" $file
	else
	echo convert big/$file -resize 20% small/$file && convert big/$file -resize 20% small/$file; 
	echo convert small/$file -resize 25% tiny/$file && convert small/$file -resize 25% tiny/$file; 
	touch signatures/$file
	fi
done





# create the html page

echo "<h1>James' Photos.</h1><p>Click for medium versions, to download at varying sizes change small/ or tiny/ to big/.  Otherwise you can get everything in a zip file with <a href=\"tiny.zip\">tiny.zip</a>, <a href=\"small.zip\">small.zip</a>, or <a href=\"big.zip\">big.zip</a>.  Method for this page: camera files go in big/, and then <a href=\"photos.sh.txt\">photos.sh</a> is used to do stuff.</p>" > photos.html
for file in `ls big | grep JPG`; do
	echo "<a href=\"small/$file\"><img src=\"tiny/$file\"></a><hr>" >> photos.html ; done

#
# create zipfiles and copy this script, set permissions

cp photos.sh photos.sh.txt
zip -0ruv tiny.zip tiny/
zip -0ruv small.zip small/
zip -0ruv big.zip big/
chmod -R 755 .
