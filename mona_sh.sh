#!/bin/bash
while : 
do
  cat ~/Workspaces/mona_data_latest.txt
  i=60
  while [ $i -gt 0 ] 
  do
    i=$(($i - 1))
    echo -ne "`date +%H:%M:%S` Refresh after $i s\r"
    sleep 1;
  done
done
