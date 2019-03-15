# coding: utf-8
"""
API Service
"""
import os
import signal
import uvicorn
from sugarapi import apirouter
from sugarapi.endpoints.systems import apirouter as systems_api_router
from multiprocessing import Process


class APIService:
    """
    API service.
    """
    def __init__(self, config):
        self._config = config
        self._process = None

    def _start_service(self) -> None:
        """
        Start service.

        :return: None
        """
        apirouter.include_router(systems_api_router)
        uvicorn.run(apirouter, host="127.0.0.1", port=8000, log_level="info", reload=True,
                    ssl_keyfile=os.path.join(self._config.config_path, "ssl", self._config.crypto.ssl.private),
                    ssl_certfile=os.path.join(self._config.config_path, "ssl", self._config.crypto.ssl.certificate))

    def start(self) -> None:
        """
        Run API service.

        :return: None
        """
        self._process = Process(target=self._start_service)
        self._process.daemon = True
        self._process.start()

    def stop(self) -> None:
        """
        Stop API service.

        :return: None
        """
        os.kill(self._process.pid, signal.SIGTERM)
