# kvDB - a distributed key-value storage database (hash table)

Optimized for reading files in range (1Mb - 1Gb).

## Description

This project includes a very simple and short implementation of a distributed key-value store.
It contains two types of servers:

- Master servers
	- Keep track of all the metadata of all the keys put in the store 
- Volume servers 
	- Responsible for storing the key-value pairs

## API

- GET <key>
	- with ranges
- PUT, DELETE <key>

## Instructions (master server)

```bash
./master.py /tmp/cachedb
```

## Instructions (volume server)

```bash
./volume /tmp/volume1/ localhost:3000
PORT=3002 ./volume.py /tmp/volume2/ localhost:3000
```

## Usage

```bash
# Instead of "examplekey", put the key. Instead of "examplevalue" put the desired value
curl -X PUT -d examplevalue localhost:3000/examplekey
curl localhost:3000/examplekey
curl -X DELETE localhost:3000/examplekey
```
