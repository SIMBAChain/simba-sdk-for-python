import os
from typing import Dict, Type

from pydantic import ValidationError
from pydantic_settings import BaseSettings

from simba_sdk.core.requests.exception import EnsureException
from simba_sdk.core.requests.middleware.manager import BaseMiddleware
from simba_sdk.core.requests.middleware.trailing_slash import (
    UrlAppendTrailingSlashHandler,
)

SDK_ROOT: str = "/".join(os.path.realpath(__file__).split("/")[:-2])
MIDDLEWARE: Dict[str, Type[BaseMiddleware]] = {
    "trailing_slash": UrlAppendTrailingSlashHandler
}


class Settings(BaseSettings):
    """
    CLIENT_ID: str - Client ID from Client Credentials
    CLIENT_SECRET: str - Client Secret from Client Credentials
    MIDDLEWARE: Dict[str, Type[BaseMiddleware]] - Middlewares to apply to any requests being sent. UrlAppendTrailingSlashHandler by default.
    MEMBERS_URL: str - The url to the members service.
    TOKEN_URL: str - The url you can get an oauth token from. Likely ends in /oauth/token/.
    CREDENTIAL_URL: str - The url to the credential service.
    RESOURCE_URL: str - The url to the resource service.
    SDK_ROOT: str - The root directory of the SDK, defaults to the folder this file is in.
    """

    CLIENT_ID: str
    CLIENT_SECRET: str
    MEMBERS_URL: str
    TOKEN_URL: str
    CREDENTIAL_URL: str
    RESOURCE_URL: str


def load_settings(**kwargs: str) -> Settings:
    return Settings()


try:
    settings = load_settings()
except ValidationError:
    raise EnsureException(message="Missing environment variables")
