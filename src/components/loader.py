"""
Loader component
"""

from collections.abc import Mapping
from dataclasses import dataclass
import json
from typing import Any
from src.environment import SECRET_PASSWORD
from src.utils import path_from_root
from src.utils import detect_indentation, add_indentation
from src.utils import random_name
from src.exceptions import LoaderException
from .logger import logger


@dataclass
class LoaderConfig:
    code: str


class Loader:
    """
    The responsibility of the loader is to
      - Parse the input JSON
      - Validate the input JSON
      - Prepare the unique module names for the user specified algorithm
      - Prepare the code specified by the user (add function definition, ...)
      - Create the module which holds the user specified algorithm
    """

    def _validate_cfg(self, raw_config: Mapping[str, object]) -> LoaderConfig:
        try:
            if "code" not in raw_config:
                raise LoaderException("Code is missing")
            if not isinstance(raw_config["code"], str):
                raise LoaderException("Code is invalid - must be a string")
            if not raw_config["code"]:
                raise LoaderException("Code is empty")
            config = LoaderConfig(code=raw_config["code"])
            return config
        except Exception as e:
            logger.error("Config validation failed")
            raise e

    def _parse_cfg(self, raw_config: Mapping[str, object]) -> LoaderConfig:
        """
        Parses the input config JSON

        raises:
         - LoaderException: if the JSON cannot be parsed
        """
        try:
            config = self._validate_cfg(raw_config)
            logger.info("Parsing cfg: success")

            return config

        except LoaderException as error:
            logger.error("Parsing cfg: error")
            raise error

        except json.JSONDecodeError:
            logger.error("Parsing cfg: error")
            raise LoaderException("Error parsing cfg")

    def generate_name(self):
        """
        Generates the unique name of the module. If running in admin mode (by
        providing correct secret in the config JSON, an uid can be specified.
        Otherwise a random 32 bytes [0-9a-f] will be generated and prefixed with
        an underscore (_) and used as the unique name.
        """
        # if self._admin_access and "uid" in self._cfg:
        #     self.unique_id = self._cfg["uid"]
        # else:
        self.unique_id = "_{}".format(random_name())

        self.module_name = "src.{}.{}".format("__algs", self.unique_id)
        self.module_path = "{}.py".format(path_from_root("__algs", self.unique_id))

        return self

    def prepare_code(self):
        """
        Prepares the user specified code to be run be the runner component.
        Wraps the code inside of a unique method which receives these arguments:
         - engine: the engine component
         - print: the overloaded print function which dumps the output to a list
           stored in the engine

        raises:
         - LoaderException: if the indentation of the code is inconsistent
        """
        try:
            code = self._cfg.code
            indentation = detect_indentation(code)

            # If there is no indentation (no if, for, while blocks), use 2
            if indentation == 0:
                indentation = 2

            code += '\nprint("That\'s all, folks!")'

            self._code = "def {}(engine, print):\n{}".format(
                self.unique_id, add_indentation(code, indentation)
            )

            return self

        except IndentationError:
            raise LoaderException("Indentation error")

    def create_module(self):
        """
        Creates the module which holds the user specified code

        raises:
         - LoaderException: if it is impossible to write to the designated file
        """
        try:
            with open(self.module_path, "w", encoding="utf8") as f:
                f.write(self._code)

            logger.info("Creating module: success", {"module": self.module_name})

            return self

        except OSError:
            logger.error("Creating module: error", {"module": self.module_name})
            raise LoaderException()

    def load(self, raw_config: Mapping[str, Any]):
        """
        Prepares the module which can be run by the runner component from the user
        provided JSON config
        """
        self._cfg = self._parse_cfg(raw_config)
        self.generate_name()
        self.prepare_code()
        self.create_module()

        return self

    def __init__(self):
        """
        Creates a new instance of Loader

        parameters:
         - cfg (str): the JSON config input
        """
        self.unique_id = None
        self.module_name = None
        self.module_path = None

        self._cfg = None
        self._code = None

        self._admin_access = False
