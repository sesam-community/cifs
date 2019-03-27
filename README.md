# sesam-cifs-cvs-reader
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
