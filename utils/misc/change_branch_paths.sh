#!/bin/bash

#grep -R "githubusercontent.com"  --include \*.json -l

if [ "$#" -lt 2 ] ; then
    echo "Replace search-pattern with replace-pattern in all the json files in the given sub-directory"
    echo "Usage: $0 <search-pattern> <replace-pattern>"
    exit 1
fi

var1=$(echo "$1" | sed 's/\//\\\//g')
var2=$(echo "$2" | sed 's/\//\\\//g')
while read line ;
  do echo $line ;
  sed -i -e  "s/$var1/$var2/g" $line
done < <(grep -R "githubusercontent.com"  --include \*.json -l)

