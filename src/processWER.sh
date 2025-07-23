
#!/bin/sh
#*-----------------------------------------------------------------------*
#* processWER                                                            *
#* Process all REQ files (.req) on the current directory and explore     *
#* the disambiguation thru chatGPT (OpenAI) using the API SKD            *
#*-----------------------------------------------------------------------*

#*---- Retrieve execution environment
clear
CURR=$(pwd)
PWD=$(dirname $0)

export DISPLAY=:0.0
export OPENAI_API_KEY={place your OPENAI_API_KEY here}

#*--- Execution environment

SCRIPT_PATH=$(dirname "$0")
if [ "$SCRIPT_PATH" = "." ]; then
   SCRIPT_PATH=$(pwd)
fi

SCRIPT_NAME="$(basename "$(test -L "$0" && readlink "$0" || echo "$0")")"
ME=$(echo $SCRIPT_NAME | cut -f 1 -d ".")
logFile=$ME".log"
tmpFile=$ME".tmp"
lstFile="WERchat.lst"
csvFile="WERchat.txt"

rm -r $logFile 2>&1 >/dev/null
rm -r $lstFile 2>&1 >/dev/null
rm -r $csvFile 2>&1 >/dev/null

echo "Corrida $SCRIPT_NAME at $(date)" | tee -a $logFile > $lstFile
echo '"Script","RunTimeStamp","CPU","File","InputSize","OutputSize","Findings","Model","TokenIn","TokenOut","TokenTotal"' 2>&1 > $csvFile

#*--- Initialize
QNET=0

#*--- Extract files and process, would process the file from WSJT-X plus any other placed in the directory with .adi extension
FILES=$(ls ./*.req)

for f in $FILES
do
  touch $tmpFile
  REQ_NAME="$(basename "$(test -L "$0" && readlink "$f" || echo "$f")")"
  REQ_E=$(echo $REQ_NAME | cut -f 1 -d ".")
  datFile='./'$REQ_E'.dat'
  echo "$ME: Processing file ($f) ($REQ_NAME) ($REQ_E)" 2>&1 | tee -a $tmpFile
  python3.11 WERchat.py $f | tee -a $tmpFile > $datFile 
  echo "***********************************************************************************************" | tee -a $logFile

  cat $tmpFile >> $logFile
  rm -r $tmpFile 2>&1 >/dev/null

  QFILES=$((QFILES+1))
done

echo "***********************************************************************************************" | tee -a $logFile >> WERchat.lst
echo "End of processing $(date) files($QFILES)" | tee -a $logFile  >> $lstFile
#*-----------------------------------------------[End of Script]-----------------------------------------------------

