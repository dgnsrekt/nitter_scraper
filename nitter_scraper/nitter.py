from contextlib import contextmanager
from ipaddress import IPv4Address
from tempfile import _TemporaryFileWrapper as TemporaryFile
from tempfile import NamedTemporaryFile
import time
from typing import ClassVar, Optional

import docker
from docker.client import DockerClient
from docker.models.containers import Container
from jinja2 import Environment, FileSystemLoader
from loguru import logger
from pydantic import BaseModel as Base

from nitter_scraper.paths import PROJECT_ROOT, TEMPLATES_DIRECTORY  # noqa: I202, I100
from nitter_scraper.profile import get_profile  # noqa: I202, I100
from nitter_scraper.tweets import get_tweets  # noqa: I202, I100


class DockerBase(Base):
    """Provides helper methods for connecting to the docker client."""

    client: ClassVar[DockerClient] = None

    @classmethod
    def _get_client(cls):
        if cls.client is None:
            cls.client = docker.from_env()

        cls.client.ping()
        logger.info("Docker connection successful.")

        return cls.client


class Nitter(DockerBase):
    """Nitter Docker container object

    Args:
        host (IPv4Address): The host address the docker container will bind too.
        port (int): The port the docker container will listen to.

    Attributes:
        tempfile (TemporaryFile): A TemporaryFile file generated from a template.
        container (Container): Local representation of a container object.
            Holds the started instance of a docker container.
        address (str): The full address of the docker container.
        ports (dict[int, int]): Binds the listening port to the nitter docker container's
            internal port 8080.
        config_filepath (str): Path name to the generated tempfile.
        volumes (dict[str, dict[str, str]]): used to configure a bind volume.


    """

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

    def get_profile(self, username: str, not_found_ok: bool = False):
        """Scrapes nitter for the target users profile information.

        This is a modified version of nitter_scraper.profile.get_profile().
        This version automatically uses the address of the docker container as the primary
        address to scrape profile data.

        Args:
            username: The target profiles username.
            not_found_ok: If not_found_ok is false (the default), a ValueError is raised if
                the target profile doesn't exist. If not_found_ok is true, None will be returned
                instead.

        Returns:
            Profile object if successfully scraped, otherwise None.

        Raises:
            ValueError: If the target profile does not exist and the not_found_ok argument is
                false.
        """
        return get_profile(username=username, not_found_ok=not_found_ok, address=self.address)

    def get_tweets(self, username: str, pages: int = 25, break_on_tweet_id: Optional[int] = None):
        """Gets the target users tweets

        This is a modified version of nitter_scraper.tweets.get_tweets().
        This version automatically uses the address of the docker container as the primary
        address to scrape profile data.

        Args:
            username: Targeted users username.
            pages: Max number of pages to lookback starting from the latest tweet.
            break_on_tweet_id: Gives the ability to break out of a loop if a tweets id is found.
            address: The address to scrape from. The default is https://nitter.net which should
                be used as a fallback address.

        Yields:
            Tweet Objects

        """

        return get_tweets(
            username=username,
            pages=pages,
            break_on_tweet_id=break_on_tweet_id,
            address=self.address,
        )

    def start(self):
        """Starts the docker the container"""
        self._create_configfile()
        client = self._get_client()

        self.container = client.containers.run(
            image="zedeus/nitter:2c6cabb4abe79166ce9973d8652fb213c1b0c5a2",
            auto_remove=True,
            ports=self.ports,
            detach=True,
            volumes=self.volumes,
        )
        time.sleep(1)
        logger.info(f"Running container {self.container.name} {self.container.short_id}.")

    def stop(self):
        """Stops the docker the container"""
        logger.info(f"Stopping container {self.container.name} {self.container.short_id}.")
        if self.container:
            self.container.stop(timeout=5)
            logger.info(f"Container {self.container.name} {self.container.short_id} Destroyed.")


@contextmanager
def NitterScraper(host: str = "0.0.0.0", port: int = 8080):
    """The NitterScraper context manager.

    Takes care of configuring, starting, and stopping a docker instance of nitter.

    Args:
        host: The host address the docker container will bind too.
        port: The port the docker container will listen to.

    Yields:
        Nitter: An object representing a started nitter docker container.
    """
    nitter = Nitter(host=host, port=port)
    nitter.start()

    try:
        yield nitter

    finally:
        nitter.stop()
