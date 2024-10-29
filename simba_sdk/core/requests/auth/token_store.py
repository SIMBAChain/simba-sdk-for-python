import json
import logging
import os.path
import pathlib
import time
from abc import ABC, abstractmethod
from typing import Dict, Optional, Union


class BaseTokenStore(ABC):
    """Defines a contract for obtaining a token for a given session"""

    @abstractmethod
    def is_stored_token(self, identifier: str) -> bool:
        """Checks if the defined token exists"""

    @abstractmethod
    def is_expired_token(self, identifier: str) -> bool:
        """Checks if the defined token has expired"""

    @abstractmethod
    def set_token(self, identifier: str, token: str, expires: int) -> None:
        """Stores the token in the specified store type"""

    @abstractmethod
    def get_token(self, identifier: str) -> Optional[str]:
        """Fetches the stored token"""


class InMemoryTokenStore(BaseTokenStore):
    token_store: Dict[str, Dict[str, Union[str, int]]] = {}

    def __init__(self, buffer: int = 60):
        self.buffer = buffer

    def is_stored_token(self, identifier: str) -> bool:
        if identifier not in self.token_store.keys():
            return False
        else:
            return True

    def is_expired_token(self, identifier: str) -> bool:
        expiry = self.token_store[identifier]["expires"]
        if not isinstance(expiry, int):
            raise TypeError(f"Token {identifier} does not have a valid expiry")
        current_time = int(time.time())
        logging.debug("token store expiry:       {}".format(expiry))
        logging.debug("token store current_time: {}".format(current_time))
        logging.debug("token store buffer:       {}".format(self.buffer))
        if current_time < expiry - self.buffer:
            return False
        else:
            return True

    def set_token(self, identifier: str, token: str, expires: int) -> None:
        self.token_store[identifier] = {"token": token, "expires": expires}

    def get_token(self, identifier: str) -> Optional[str]:
        token = self.token_store.get(identifier)
        if token is None:
            return None
        token_val = token.get("token")
        if not isinstance(token_val, str):
            raise TypeError(f"Token {identifier} does not have a valid token")
        return token_val


class FileTokenStore(BaseTokenStore):
    def __init__(self, dirpath: str, buffer: int = 60):
        self.buffer = buffer
        if not os.path.exists(dirpath):
            raise EnvironmentError
        self._dirpath = dirpath
        tokens = os.listdir(dirpath)
        logging.debug("checking for expired tokens")
        for token_path in tokens:
            if self.is_expired_token(token_path.split(".json")[0]):
                logging.debug("expired token, removing: {}".format(token_path))
                os.remove(
                    os.path.join(dirpath, token_path)
                )  # this can be made optional to just "archive"

    def is_expired_token(self, identifier: str) -> bool:
        filepath = pathlib.Path(self._dirpath, f"{identifier}.json")
        with open(filepath, "r") as f:
            store = json.loads(f.read())

        expiry = store["expires"]
        current_time = int(time.time())
        logging.debug("token store expiry:       {}".format(expiry))
        logging.debug("token store current_time: {}".format(current_time))
        logging.debug("token store buffer:       {}".format(self.buffer))
        if current_time < expiry - self.buffer:
            return False
        else:
            return True

    def is_stored_token(self, identifier: str) -> bool:
        filepath = pathlib.Path(self._dirpath, f"{identifier}.json")
        if not os.path.isfile(filepath):
            return False
        else:
            return True

    def set_token(self, identifier: str, token: str, expires: int) -> None:
        filepath = pathlib.Path(self._dirpath, f"{identifier}.json")
        with open(filepath, "w") as f:
            f.write(json.dumps({"token": token, "expires": expires}))

    def get_token(self, identifier: str) -> str:
        filepath = pathlib.Path(self._dirpath, f"{identifier}.json")
        with open(filepath) as f:
            token: str = json.loads(f.read())["token"]
            return token
