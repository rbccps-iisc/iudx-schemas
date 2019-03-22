#!/bin/bash

#grep -R "githubusercontent.com"  --include \*.json -l

var1=$(echo "$1" | sed 's/\//\\\//g')
var2=$(echo "$2" | sed 's/\//\\\//g')
while read line ;
  do echo $line ;
  sed -i -e  "s/$var1/$var2/g" $line
done < <(grep -R "githubusercontent.com"  --include \*.json -l)

