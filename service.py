import csv
import os

import json
import logging
import socket

from flask import Flask, Response, request, abort
from waitress import serve
from smb.SMBConnection import SMBConnection

APP = Flask(__name__)

logging.basicConfig(level='INFO')

fieldnames = os.environ.get("fieldnames",
                            "maalepunkt,netteigarmaalarid,installasjonsid,namn,husnr,adresse,poststad,postnr,telefonnr,telefonnrjob,mobilnummer1,epost").split(
    ",")


@APP.route("/<file_name>", methods=['GET'])
def process_request(file_name):
    logging.info("Processing request..")

    # get URL params
    delimiter = request.args.get('delimiter')
    headers = request.args.get('headers')

    # defaulting to comma separated files if no delimiters are supplied in URL
    if delimiter is None:
        delimiter = ','

    if headers is not None:
        fieldnames = headers.split(delimiter)

    logging.info("csv file: %s" % file_name)
    logging.info("csv headers: %s" % ','.join(fieldnames))
    logging.info("csv delimiter: '%s'" % delimiter)

    if file_name == "use_current_date_filename":
        import datetime
        today = datetime.date.today()
        file_name = "customer_{}.lst".format(today.strftime("%d-%m-%y"))

    conn = SMBConnection(os.environ.get("username"), os.environ.get("password"), socket.gethostname(),
                         os.environ.get("hostname"), is_direct_tcp=True, use_ntlm_v2=True)
    conn.connect(os.environ.get("host"), 445)
    logging.info("Connected to SMB host ...")

    logging.info("List shares...")
    share_list = conn.listShares()
    for share in share_list:
        logging.info('Shared device: %s (type:0x%02x comments:%s)' % (share.name, share.type, share.comments))

    try:
        with open('local_file', 'wb') as fp:
            conn.retrieveFile(os.environ.get("share"), file_name, fp)
            logging.info("Completed file downloading...", )
        with open('local_file', 'r', encoding='utf-8', errors='ignore') as fp:
            return Response(json.dumps(list(csv.DictReader(fp, fieldnames=fieldnames, delimiter=delimiter))),
                            content_type="application/json")
    except Exception as e:
        logging.info(e)
        logging.info("List files founded on share")
        file_list = conn.listPath(os.environ.get("share"), "/")
        for f in file_list:
            logging.info('file: %s (FileSize:%d bytes, isDirectory:%s)' % (f.filename, f.file_size, f.isDirectory))
    finally:
        conn.close()
        os.remove("local_file")
    abort(500)


if __name__ == "__main__":
    logging.info("Starting service...")
    serve(APP, host='0.0.0.0', port=8080)
