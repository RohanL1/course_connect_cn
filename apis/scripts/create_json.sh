#!/bin/bash

if (( "$#" < 1 ))
then
 echo "## HELP##\n./create_json.sh IN_FILE"
 echo "IN_FILE format"
 echo "subject_code|name|credits"
 exit 1
fi

cat ${IN_FILE} | while IFS='|' read code name cred
do 
 for term in 12 13 14 15
  do
   echo "{ \"name\": \"${name}\", \"code\": \"${code}\", \"prof_id\": 4, \"term_id\": ${term},\"credits\" : ${cred}}"
  done
done
