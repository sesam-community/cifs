# sesam-cifs-cvs-reader

[![Build Status](https://travis-ci.org/sesam-community/sesam-cifs-cvs-reader.svg?branch=master)](https://travis-ci.org/sesam-community/sesam-cifs-cvs-reader)

Simple sesam source that fetch CVS file from CIFS share

## System set up

```json
{
  "_id": "<id>",
  "type": "system:microservice",
  "docker": {
    "environment": {
      "host": "<hostip>",
      "hostname": "<name returned by hostname command on host>",
      "password": "<password>",
      "share": "<share name>",
      "username": "<username>"
    },
    "image": "ohuenno/python-cifs-test",
    "port": 8080
  },
  "verify_ssl": true
}

```
## Pipe set up
```json
{
  "_id": "<id>",
  "type": "pipe",
  "source": {
    "type": "json",
    "system": "<system id>",
    "url": "/use_current_date_filename"
  },
  "transform": {
    "type": "dtl",
    "rules": {
      "default": [
        ["add", "_id",
          ["string",
            ["concat", "_S.maalepunkt", "-", "_S.netteigarmaalarid", "-", "_S.installasjonsid"]
          ]
        ],
        ["copy", "*"]
      ]
    }
  },
  "pump": {
    "cron_expression": "0 7 * * ?"
  }
}

```

## Pipe set up with headers as URL parameters
```json
{
  "_id": "<id>",
  "type": "pipe",
  "source": {
    "type": "json",
    "system": "<system id>",
    "url": "/some-file.csv?headers=header1,header2,header3"
  },
  "transform": {
    "type": "dtl",
    "rules": {
      "default": [
        ["add", "_id",
          ["string",
            ["concat", "_S.header1", "-", "_S.header2", "-", "_S.header3"]
          ]
        ],
        ["copy", "*"]
      ]
    }
  },
  "pump": {
    "cron_expression": "0 7 * * ?"
  }
}

```
