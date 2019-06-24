# kvDB - a distributed key-value storage database (hash table)

[![Build Status](https://travis-ci.com/strudra/kvdb.svg?branch=master)](https://travis-ci.com/strudra/kvdb)

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
- POST, DELETE <key>

## Instructions (master server)

```bash
./master localhost:3001,localhost:3002 /tmp/cachedb/
```

## Instructions (volume server)

```bash
./volume /tmp/volume1/
PORT=3002 ./volume /tmp/volume2/
```

## Usage

```bash
# Instead of "examplekey", post the key. Instead of "examplevalue" put the desired value
curl -L -X POST -d examplevalue localhost:3000/examplekey
curl -L -X GET localhost:3000/examplekey
curl -L -X DELETE localhost:3000/examplekey
```
