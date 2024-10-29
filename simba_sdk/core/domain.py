from typing import Any, Dict, List, Optional
from uuid import UUID

from kiota_abstractions.serialization import Parsable
from pydantic import BaseModel, EmailStr
from typing_extensions import Self


def recursive_deserialise(obj: Any) -> Any:
    if isinstance(obj, dict):
        for key, value in obj.items():
            obj[key] = recursive_deserialise(value)
    elif isinstance(obj, list):
        for i in range(len(obj)):
            obj[i] = recursive_deserialise(obj[i])
    elif isinstance(obj, Parsable):
        obj = obj.__dict__
        recursive_deserialise(obj)
    elif isinstance(obj, DomainModel):
        obj = obj.model_dump()
    return obj


class DomainModel(BaseModel):
    """
    Domain model for storing simplified versions of various SIMBA models.
    Provides a method for converting from Kiota serialisers.
    """

    @classmethod
    def model_validate_kiota(cls, serialiser: Parsable) -> Self:
        """
        Convert a kiota serialiser obj (Parsable) into a pydantic DomainModel.
        args:
            cls: The DomainModel class. Used for accessing fields and validation.
            serialiser: The Parsable object to convert.
        returns:
            An instance of the DomainModel class with fields populated by the kiota serialisers data.
        """
        data = {}
        for field_name, field_info in cls.model_fields.items():
            if hasattr(serialiser, field_name):
                data[field_name] = recursive_deserialise(
                    getattr(serialiser, field_name)
                )
            elif field_info.is_required():
                raise ValueError(f"Field '{field_name}' is required.")
        return cls.model_validate(data)


class Organisation(DomainModel):
    id: UUID
    display_name: str
    name: str
    is_domain: bool


class UserProfile(DomainModel):
    first_name: str
    last_name: str


class User(DomainModel):
    id: UUID
    default_organisation: Organisation
    email: EmailStr
    organisations: Optional[List[Organisation]] = None
    profile: Optional[Dict[str, UserProfile]]


class Account(DomainModel):
    alias: str
    nickname: str
    network: str
    owner: Dict[str, str]
