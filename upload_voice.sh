#!/bin/bash

ROBOT_IP="theq.lan"                 # IP or hostname of your robot
LOCAL_SERVER="192.168.1.15:8000"    # IP and port of the computer running this script
LANGUAGE_CODE="VA"


while getopts "f:v:" opt; do
    case ${opt} in
        f )
            file_path=${OPTARG}
            ;;
        v )
            volume=${OPTARG}
            ;;
  \? )
    echo "Invalid Option: -$OPTARG" 1>&2
    exit 1
    ;;
 esac
done

if [ ! -f "$file_path" ]; then
    echo "Error: File not found at '$file_path'"
    exit 1
fi

FILENAME=$(basename "$file_path")

HASH=$(md5sum "$file_path" | awk '{ print $1 }')

DOWNLOAD_URL="http://${LOCAL_SERVER}/${FILENAME}"
JSON_PAYLOAD=$(printf '{"action":"download","url":"%s","hash":"%s","language":"%s"}' "$DOWNLOAD_URL" "$HASH" "$LANGUAGE_CODE")


echo "▶️  Preparing to send voice pack..."
echo "-----------------------------------"
echo "  File:      $FILENAME"
echo "  MD5 Hash:  $HASH"
echo "  Payload:   $JSON_PAYLOAD"
echo "-----------------------------------"
echo ""

curl -X PUT \
     -H "Content-Type: application/json" \
     -d "$JSON_PAYLOAD" \
     "http://${ROBOT_IP}/api/v2/robot/capabilities/VoicePackManagementCapability"

if [ "$volume" != "" ]; then
    curl -X PUT \
         -H "Content-Type: application/json" \
         -d '{"action":"set_volume","value": '$volume'}' \
         "http://${ROBOT_IP}/api/v2/robot/capabilities/SpeakerVolumeControlCapability"
fi

echo -e "\n✅ Request sent."
