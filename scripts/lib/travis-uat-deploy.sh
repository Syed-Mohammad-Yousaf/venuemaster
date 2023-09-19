#!/usr/bin/env bash
set -e
ssh -o StrictHostKeyChecking=no -t $HOST_USER@34.207.76.167 "cd $DIR; $UAT_SCRIPT_PATH"
