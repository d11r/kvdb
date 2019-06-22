#!/bin/bash
docker build -t kvdb -f Dockerfile .
docker run --hostname localhost -p 3000:3000 -p 3001:3001 -p 3002:3002 --name kvdb --rm kvdb bash -c "cd /tmp && test/bringup.sh"