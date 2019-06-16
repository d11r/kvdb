# kvDB - a distributed key-value storage database (hash table)

Optimized for reading files in range (1Mb - 1Gb).

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