from ipaddress import IPv4Address
from typing import ClassVar, Optional, List
from pathlib import Path

import docker
from docker.errors import APIError
from docker.client import DockerClient
from docker.models.containers import Container
from pydantic import BaseModel as Base

from tempfile import NamedTemporaryFile
from tempfile import _TemporaryFileWrapper as TemporaryFile

from jinja2 import Environment, FileSystemLoader

from contextlib import contextmanager, ExitStack

from nitter_scraper.paths import TEMPLATES_DIRECTORY, PROJECT_ROOT

from loguru import logger

import time


class DockerBase(Base):
    client: ClassVar[DockerClient] = None

    @classmethod
    def get_client(cls):
        if cls.client is None:
            cls.client = docker.from_env()
            cls.client.ping()
            logger.info(f"Docker connection successful.")

        return cls.client


class Nitter(DockerBase):
    host: IPv4Address
    port: int

    tempfile: TemporaryFile = None
    container: Optional[Container]

    class Config:
        arbitrary_types_allowed = True

    @property
    def address(self):
        return f"http://{self.host}:{self.port}"

    @property
    def config_filepath(self):
        if self.tempfile:
            return self.tempfile.name

    @property
    def ports(self):
        return {8080: self.port}

    @property
    def volumes(self):
        volumes = {"bind": "/src/nitter.conf", "mode": "ro"}
        return {self.config_filepath: volumes}

    def _render_config(self):
        env = Environment(loader=FileSystemLoader(TEMPLATES_DIRECTORY))
        template = env.get_template("nitter.conf")
        return template.render(self.dict())

    def _create_configfile(self):
        config = self._render_config()
        self.tempfile = NamedTemporaryFile(dir=PROJECT_ROOT)
        self.tempfile.write(config.encode())
        self.tempfile.seek(0)

    def start(self):
        self._create_configfile()
        client = self.get_client()

        self.container = client.containers.run(
            image="zedeus/nitter:latest",
            auto_remove=True,
            ports=self.ports,
            detach=True,
            volumes=self.volumes,
        )
        time.sleep(1)
        logger.info(f"Running container {self.container.name} {self.container.short_id}.")

    def stop(self):
        logger.info(f"Stopping container {self.container.name} {self.container.short_id}.")
        if self.container:
            self.container.stop(timeout=5)
            logger.info(f"Container {self.container.name} {self.container.short_id} Destroyed.")


@contextmanager
def NitterDockerContainer(host: str = "0.0.0.0", port: int = 8080):
    nitter = Nitter(host=host, port=port)
    nitter.start()

    try:
        yield nitter

    finally:
        nitter.stop()
