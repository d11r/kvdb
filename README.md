# kvDB - a distributed key-value storage database

[![Build Status](https://travis-ci.com/strudra/kvdb.svg?branch=master)](https://travis-ci.com/strudra/kvdb)

Optimized for reading files in range (1Mb - 1Gb). 
The idea is to have one master server and multiple volume servers.
Requests are forwarded from master to volumes depending on certain criteria.
Volume servers then store the necessary information in the key-value store LevelDB (by Google).
Supports inserts, deletes and gets.

## Description

This project includes a very simple and short implementation of a distributed key-value store.
It contains two types of servers:

- Master servers
	- Keep track of all the metadata of all the keys put in the store 
- Volume servers 
	- Responsible for storing the key-value pairs
	
## Implementation (technology stack)

Tools that were used are the following:

- Python3 for overall scripting
- uWSGI for handling requests
- LevelDB by Google for storing key-value pairs on the disk

## Instructions

To contribute to the project, or just play with it, 
clone the repository and install all the requirements from `requirements.txt`.
Then execute the following scripts to get the uWSGI server up and running.
Also, you can use docker using the `docker.sh` script to execute all the necessary commands.

### Master server

```bash
./master localhost:3001,localhost:3002 /tmp/cachedb/
```

### Instructions (volume server)

```bash
./volume /tmp/volume1/
PORT=3002 ./volume /tmp/volume2/
```

## API

- GET, DELETE `<key>`, returns the value or raises an error
- POST `<key>` `<value>`, returns the value or raises an error

For the detailed docs, see `test/test.py`. 

## Usage

```bash
# Instead of "examplekey", post the key. Instead of "examplevalue" put the desired value
curl -L -X POST -d examplevalue localhost:3000/examplekey
curl -L -X GET localhost:3000/examplekey
curl -L -X DELETE localhost:3000/examplekey
```

## Next Steps

- Use a key-value store that supports multi-processing and multi-threading.
- Select volume servers `intelligently`.