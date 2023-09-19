#!/usr/bin/env bash
set -e
ssh -o StrictHostKeyChecking=no -t $HOST_USER@$UAT_DAILY_REMOTE_HOST "cd $DIR; $UAT_DAILY_SCRIPT_PATH"
