# kvDB - a distributed key-value storage database (hash table)

Optimized for reading files in range (1Mb - 1Gb).

## API

- GET <key>
    - with ranges
- PUT, DELETE <key>

## Instructions (master server)

```bash
./master.py -p 3000 /tmp/cachedb
```

## Instructions (volume server)

```bash
./volume.py -p 3001 /tmp/volume1/ localhost:3000
./volume.py -p 3002 /tmp/volume2/ localhost:3000
```