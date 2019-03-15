# coding: utf-8
"""
API Service
"""
import os
import uvicorn
from sugarapi import apirouter
from sugarapi.endpoints import systems


def api_service(config):
    """
    Run API service.
    """
    uvicorn.run(apirouter, host="127.0.0.1", port=8000, log_level="info", reload=True)


if __name__ == "__main__":
    r = "/home/bo/work/sugar/sugar/etc/sugar/ssl"
    uvicorn.run(apirouter, host="127.0.0.1", port=8000, log_level="info", reload=True,
                ssl_keyfile=os.path.join(r, "key.pem"),
                ssl_certfile=os.path.join(r, "cert.pem"))
