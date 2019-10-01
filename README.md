# cifs

[![Build Status](https://travis-ci.org/sesam-community/cifs.svg?branch=master)](https://travis-ci.org/sesam-community/cifs)

Sesam microservice to read files from cifs file share.

## System set up

```json
{
  "_id": "<my-system-id>",
  "type": "system:microservice",
  "docker": {
    "environment": {
      "host": "<hostip>",
      "hostname": "<name returned by hostname command on host>",
      "password": "<password>",
      "share": "<share name>",
      "username": "<username>"
    },
    "image": "sesamcommunity/cifs",
    "port": 5000
  }
}

```
## Pipe example
Example when reading a csv file:
```json
{
  "_id": "<my-pipe-id>",
  "type": "pipe",
  "source": {
    "type": "csv",
    "system": "<my-system-id>",
    "auto_dialect": true,
    "delimiter": ";",
    "dialect": "excel",
    "encoding": "utf-8",
    "has_header": true,
    "preserve_empty_strings": false,
    "primary_key": "DOC_NO",
    "url": "/path/to/file.csv"
  },
  "transform": {
    "type": "dtl",
    "rules": {
      "default": [
        ["copy", "*"],
        ["add", "rdf:type",
          ["ni", "cool:Document"]
        ]
      ]
    }
  },
  "add_namespaces": true
}
```