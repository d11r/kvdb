#!/bin/bash
trap "trap - SIGTERM && kill -- -$$" SIGINT SIGTERM EXIT

chmod +x /tmp/bringup.sh &
chmod +x /tmp/test.py &

PORT=3001 ./volume /tmp/volume1/ &
PORT=3002 ./volume /tmp/volume2/ &

./master localhost:3001,localhost:3002 /tmp/cachedb/
