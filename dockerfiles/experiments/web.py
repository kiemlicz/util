import logging
import flask
import time
import signal
import sys
import socket
from flask import Flask
from flask_api import status
from os import environ

from kubernetes import client, config

log = logging.getLogger()
log.addHandler(logging.StreamHandler())
log.setLevel(logging.INFO)

app = Flask(__name__)
try:
    config.load_incluster_config()
    v1 = client.CoreV1Api()
except Exception as e:
    log.exception("K8s config not loaded")


@app.route('/')
def hello():
    return f"Hello World!: {flask.request.remote_addr}, handler: {socket.gethostname()}"

@app.route('/health')
def health():
    log.info(f"health check from: {flask.request.remote_addr}")
    return "OK"

@app.route('/broken')
def sick():
    return "BAD", status.HTTP_404_NOT_FOUND

@app.route('/slow/<leng>')
def broken(leng):
    time.sleep(int(leng))
    return "slow", status.HTTP_200_OK

@app.route('/pods')
def k8sapi():
    # with open("/var/run/secrets/kubernetes.io/serviceaccount/namespace", 'r') as f:
    #     ns = f.readline()
    #     log.info(f"Reading PODs in ns: {ns}")
    return [i for i in v1.list_pod_for_all_namespaces(watch=False).items]


def sigterm_handler(signum, frame):
    log.info("SIGTERM received, stopping")
    sys.exit()

if __name__ == '__main__':
    if environ.get('FLASK_SETTINGS') is not None:
        log.info("Found flask config")
        app.config.from_envvar('FLASK_SETTINGS')
        log.info(f"config: {app.config}")

    signal.signal(signal.SIGTERM, sigterm_handler)
    app.run(host="0.0.0.0")
