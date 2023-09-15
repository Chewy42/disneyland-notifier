#!/bin/bash

if [ -f ".tokens.sh" ];
then
    . .tokens.sh
else
    export API_PASS=$(echo $RANDOM | sha256sum | base64 | head -c 32)
    echo "export API_PASS=$API_PASS" > .tokens.sh
fi

export DOCKER_PLATFORM="linux/amd64"