# coding: utf-8
"""
API Service
"""
import os
import signal
import uvicorn
from sugarapi import apirouter, MasterRef
from sugarapi.endpoints.systems import apirouter as systems_api_router
from sugarapi.endpoints.jobs import apirouter as jobs_api_router
from multiprocessing import Process, Pipe


class APIService:
    """
    API service.
    """
    def __init__(self, config):
        self._config = config
        self._process = None
        self._running = True
        self._channel = MasterRef(Pipe()).receiver

    def queue_loop(self, target):
        while self._running:
            call_target = self._channel.recv()
            if call_target is not None:
                obj = call_target(target)
                if obj is not None:
                    self._channel.send(obj)
                else:
                    raise Exception("No such attribute: '{}'".format(call_target))

    def _start_service(self) -> None:
        """
        Start service.

        :return: None
        """
        apirouter.include_router(systems_api_router)
        apirouter.include_router(jobs_api_router)
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
        self._running = False
        MasterRef().sender.send(None)
        os.kill(self._process.pid, signal.SIGTERM)
