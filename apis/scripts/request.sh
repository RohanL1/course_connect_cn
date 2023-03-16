#!/bin/bash

if (( "$#" < 3 ))
then
 echo "## HELP##\n./request.sh URL METHOD JSON_FILE"
 exit 1
fi

URL=$1
METHOD=$2
JSON_FILE=$3

while read ln
do
 echo "curl -X \"${METHOD}\" \"${URL}\" -H \"Content-Type: application/json\" -d  \"${ln}\""
 curl -X "${METHOD}" "${URL}" -H "Content-Type: application/json" -d  "${ln}"
done < ${JSON_FILE}

