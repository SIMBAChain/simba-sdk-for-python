from dataclasses import dataclass
from typing import Union

from simba_sdk.core.requests.client.resource import schemas as resource_schemas


@dataclass
class GetBundleProfilesQuery:
    page: int
    size: int
    order_by: Union[str, None] = None
    name: Union[str, None] = None
    storage_name: Union[str, None] = None


@dataclass
class GetBundleEventsQuery:
    page: int
    size: int
    order_by: Union[str, None] = None
    type: Union[str, None] = None
    transaction: Union[str, None] = None
    trigger: Union[str, None] = None
    bundle_id: Union[str, None] = None
    created_at__lt: Union[str, None] = None
    created_at__gt: Union[str, None] = None


@dataclass
class GetBundlesQuery:
    page: int
    size: int
    order_by: Union[str, None] = None
    name: Union[str, None] = None
    container: Union[str, None] = None
    tags__in: Union[str, None] = None
    hash: Union[str, None] = None
    storage_id: Union[str, None] = None
    owner_id: Union[str, None] = None
    owner__email: Union[str, None] = None
    owner__simba_id: Union[str, None] = None
    owner__name: Union[str, None] = None


@dataclass
class GetTasksQuery:
    page: int
    size: int
    order_by: Union[str, None] = None
    type: Union[str, None] = None
    status: Union[str, None] = None


@dataclass
class GetTransferQuery:
    role: str


@dataclass
class UpdateTransferQuery:
    role: str


@dataclass
class GetTransfersQuery:
    role: str
    page: int
    size: int
    order_by: Union[str, None] = None
    completed: Union[bool, None] = None
    state: Union[str, None] = None


@dataclass
class GetStoragesQuery:
    page: int
    size: int
    order_by: Union[str, None] = None
    name: Union[str, None] = None
    enabled: Union[bool, None] = None


@dataclass
class GetStorageTypeViewsQuery:
    page: int
    size: int
    order_by: Union[str, None] = None
    name: Union[str, None] = None
    adapter: Union[str, None] = None


@dataclass
class GetOrgBundleProfilesQuery:
    page: int
    size: int
    order_by: Union[str, None] = None
    name: Union[str, None] = None
    storage_name: Union[str, None] = None


@dataclass
class GetOrgBundleEventsQuery:
    page: int
    size: int
    order_by: Union[str, None] = None
    type: Union[str, None] = None
    transaction: Union[str, None] = None
    trigger: Union[str, None] = None
    bundle_id: Union[str, None] = None
    created_at__lt: Union[str, None] = None
    created_at__gt: Union[str, None] = None


@dataclass
class GetOrgBundlesQuery:
    page: int
    size: int
    order_by: Union[str, None] = None
    name: Union[str, None] = None
    container: Union[str, None] = None
    tags__in: Union[str, None] = None
    hash: Union[str, None] = None
    storage_id: Union[str, None] = None
    owner_id: Union[str, None] = None
    owner__email: Union[str, None] = None
    owner__simba_id: Union[str, None] = None
    owner__name: Union[str, None] = None


@dataclass
class GetOrgTasksQuery:
    page: int
    size: int
    order_by: Union[str, None] = None
    type: Union[str, None] = None
    status: Union[str, None] = None


@dataclass
class GetOrgTransferQuery:
    role: str


@dataclass
class UpdateOrgTransferQuery:
    role: str


@dataclass
class GetOrgTransfersQuery:
    role: str
    page: int
    size: int
    order_by: Union[str, None] = None
    completed: Union[bool, None] = None
    state: Union[str, None] = None


@dataclass
class GetOrgStoragesQuery:
    page: int
    size: int
    order_by: Union[str, None] = None
    name: Union[str, None] = None
    enabled: Union[bool, None] = None


@dataclass
class GetSchemaDataQuery:
    data_type: resource_schemas.SchemaDataType


@dataclass
class GetDomainsQuery:
    page: int
    size: int
    order_by: Union[str, None] = None
    name: Union[str, None] = None


@dataclass
class GetOrganisationsQuery:
    page: int
    size: int
    order_by: Union[str, None] = None
    name: Union[str, None] = None


@dataclass
class GetStorageTypesQuery:
    page: int
    size: int
    order_by: Union[str, None] = None
    name: Union[str, None] = None
    adapter: Union[str, None] = None


@dataclass
class GetUsersQuery:
    page: int
    size: int
    order_by: Union[str, None] = None
    name: Union[str, None] = None
    simba_id: Union[str, None] = None
    email: Union[str, None] = None


@dataclass
class BrowseBundlesQuery:
    page: int
    size: int
    order_by: Union[str, None] = None
    tags__in: Union[str, None] = None


@dataclass
class BrowsePublicBundlesQuery:
    page: int
    size: int
    order_by: Union[str, None] = None
    tags__in: Union[str, None] = None
