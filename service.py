import io
import os
import sys

import socket

from flask import Flask, abort, send_file
from waitress import serve
from smb.SMBConnection import SMBConnection
from sesamutils import VariablesConfig, sesam_logger
APP = Flask(__name__)

logger = sesam_logger("cifs-reader")

required_env_vars = ["username", "password", "hostname", "host", "share"]
config = VariablesConfig(required_env_vars)
if not config.validate():
    sys.exit(1)


def create_connection():
    return SMBConnection(config.username, config.password, socket.gethostname(),
                          config.hostname, is_direct_tcp=True, use_ntlm_v2=True)


@APP.route("/<path:path>", methods=['GET'])
def process_request(path):
    logger.info(f"Processing request for path '{path}'.")

    conn = create_connection()
    if not conn.connect(config.host, 445):
        logger.error("Failed to authenticate with the provided credentials")
        conn.close()
        return "Invalid credentials provided for fileshare", 500

    logger.info("Successfully connected to SMB host.")

    logger.info("Listing available shares:")
    share_list = conn.listShares()
    for share in share_list:
        logger.info(f"Share: {share.name}  {share.type}    {share.comments}")

    path_parts = path.split("/")
    file_name = path_parts[len(path_parts)-1]

    try:
        with open('local_file', 'wb') as fp:
            conn.retrieveFile(config.share, path, fp)
            logger.info("Completed file downloading...", )
        return send_file('local_file', attachment_filename=file_name)
    except Exception as e:
        logger.error(f"Failed to get file from fileshare. Error: {e}")
        logger.debug("Files found on share:")
        file_list = conn.listPath(os.environ.get("share"), "/")
        for f in file_list:
            logger.debug('file: %s (FileSize:%d bytes, isDirectory:%s)' % (f.filename, f.file_size, f.isDirectory))
    finally:
        conn.close()
        os.remove("local_file")
    abort(500)


if __name__ == "__main__":
    logger.info("Starting service...")

    # Test connection at startup
    conn = create_connection()
    if not conn.connect(config.host, 445):
        logger.error("Failed to authenticate with the provided credentials")
    conn.close()

    serve(APP, host='0.0.0.0', port=8080)


# TODO: cherrypy https://github.com/sesam-io/python-datasink-template/blob/master/service/datasink-service.py