from dataclasses import asdict
from typing import Any, Dict, Optional, Union

import pydantic_core
from pydantic import BaseModel

from simba_sdk.config import settings
from simba_sdk.core.requests.client.base import Client
from simba_sdk.core.requests.client.resource import queries as resource_queries
from simba_sdk.core.requests.client.resource import schemas as resource_schemas
from simba_sdk.core.requests.exception import EnsureException


class ResourceClient(Client):
    """
    This client is used as a context manager to interact with one of the SIMBAChain service APIs.
    e.g.
    ```
    my_dids: List[DidResponse] = await credential_client.dids_get_dids()
    ```
    Clients are generated with methods that have a 1:1 relationship with endpoints on the service's API. You can find the models from the api in ./schemas.py
    and query models in ./queries.py
    """

    async def authorise(
        self, token_url: str = settings.TOKEN_URL, headers: Optional[Dict] = None
    ) -> None:
        await super().authorise(token_url, headers)

    async def get_bundle_profiles(
        self,
        query_arguments: resource_queries.GetBundleProfilesQuery,
        domain_name: str,
    ) -> resource_schemas.PageBundleProfile:
        """ """

        # get rid of items where None
        query_params = {
            k: v for k, v in asdict(query_arguments).items() if v is not None
        }

        path_params: Dict[str, Any] = {
            "domain_name": domain_name,
        }
        resp = await self.get(
            f"/v1/domains/{domain_name}/bundles/profiles/",
            params=path_params | query_params,
        )

        try:
            resp_model = resource_schemas.PageBundleProfile.model_validate(resp.json())
        except pydantic_core.ValidationError:
            raise EnsureException(
                f"The response came back in an unexpected format: {resp.text}"
            )
        return resp_model

    async def create_bundle_profile(
        self,
        domain_name: str,
        bundleprofilerequest: resource_schemas.BundleProfileRequest,
    ) -> resource_schemas.BundleProfile:
        """ """

        path_params: Dict[str, Any] = {
            "domain_name": domain_name,
        }
        resp = await self.post(
            f"/v1/domains/{domain_name}/bundles/profiles/",
            data=str(bundleprofilerequest)
            if not issubclass(type(bundleprofilerequest), BaseModel)
            else bundleprofilerequest.model_dump_json(),  # type: ignore
            params=path_params,
        )

        try:
            resp_model = resource_schemas.BundleProfile.model_validate(resp.json())
        except pydantic_core.ValidationError:
            raise EnsureException(
                f"The response came back in an unexpected format: {resp.text}"
            )
        return resp_model

    async def get_bundle_profile(
        self,
        profile_id: str,
        domain_name: str,
    ) -> None:
        """
        Gets a bundle by its database UUID
        """

        path_params: Dict[str, Any] = {
            "profile_id": profile_id,
            "domain_name": domain_name,
        }
        await self.get(
            f"/v1/domains/{domain_name}/bundles/profiles/{profile_id}",
            params=path_params,
        )

        return

    async def update_bundle_profile(
        self,
        profile_id: str,
        domain_name: str,
        updatebundleprofilerequest: resource_schemas.UpdateBundleProfileRequest,
    ) -> resource_schemas.BundleProfile:
        """ """

        path_params: Dict[str, Any] = {
            "profile_id": profile_id,
            "domain_name": domain_name,
        }
        resp = await self.put(
            f"/v1/domains/{domain_name}/bundles/profiles/{profile_id}",
            data=str(updatebundleprofilerequest)
            if not issubclass(type(updatebundleprofilerequest), BaseModel)
            else updatebundleprofilerequest.model_dump_json(),  # type: ignore
            params=path_params,
        )

        try:
            resp_model = resource_schemas.BundleProfile.model_validate(resp.json())
        except pydantic_core.ValidationError:
            raise EnsureException(
                f"The response came back in an unexpected format: {resp.text}"
            )
        return resp_model

    async def delete_bundle_profile(
        self,
        profile_id: str,
        domain_name: str,
    ) -> resource_schemas.BundleProfile:
        """ """

        path_params: Dict[str, Any] = {
            "profile_id": profile_id,
            "domain_name": domain_name,
        }
        resp = await self.delete(
            f"/v1/domains/{domain_name}/bundles/profiles/{profile_id}",
            params=path_params,
        )

        try:
            resp_model = resource_schemas.BundleProfile.model_validate(resp.json())
        except pydantic_core.ValidationError:
            raise EnsureException(
                f"The response came back in an unexpected format: {resp.text}"
            )
        return resp_model

    async def get_bundle_events(
        self,
        query_arguments: resource_queries.GetBundleEventsQuery,
        domain_name: str,
    ) -> resource_schemas.PageBundleEventModel:
        """ """

        # get rid of items where None
        query_params = {
            k: v for k, v in asdict(query_arguments).items() if v is not None
        }

        path_params: Dict[str, Any] = {
            "domain_name": domain_name,
        }
        resp = await self.get(
            f"/v1/domains/{domain_name}/bundles/events/",
            params=path_params | query_params,
        )

        try:
            resp_model = resource_schemas.PageBundleEventModel.model_validate(
                resp.json()
            )
        except pydantic_core.ValidationError:
            raise EnsureException(
                f"The response came back in an unexpected format: {resp.text}"
            )
        return resp_model

    async def get_bundle_event(
        self,
        uid: str,
        event_id: str,
        domain_name: str,
    ) -> resource_schemas.ResourceBundle:
        """
        Gets a bundle by its database UUID
        """

        path_params: Dict[str, Any] = {
            "uid": uid,
            "event_id": event_id,
            "domain_name": domain_name,
        }
        resp = await self.get(
            f"/v1/domains/{domain_name}/bundles/{uid}/events/{event_id}",
            params=path_params,
        )

        try:
            resp_model = resource_schemas.ResourceBundle.model_validate(resp.json())
        except pydantic_core.ValidationError:
            raise EnsureException(
                f"The response came back in an unexpected format: {resp.text}"
            )
        return resp_model

    async def get_bundles(
        self,
        query_arguments: resource_queries.GetBundlesQuery,
        domain_name: str,
    ) -> resource_schemas.PageResourceBundle:
        """ """

        # get rid of items where None
        query_params = {
            k: v for k, v in asdict(query_arguments).items() if v is not None
        }

        path_params: Dict[str, Any] = {
            "domain_name": domain_name,
        }
        resp = await self.get(
            f"/v1/domains/{domain_name}/bundles/", params=path_params | query_params
        )

        try:
            resp_model = resource_schemas.PageResourceBundle.model_validate(resp.json())
        except pydantic_core.ValidationError:
            raise EnsureException(
                f"The response came back in an unexpected format: {resp.text}"
            )
        return resp_model

    async def create_bundle(
        self,
        domain_name: str,
        createresourcebundlerequest: resource_schemas.CreateResourceBundleRequest,
    ) -> resource_schemas.ResourceBundle:
        """ """

        path_params: Dict[str, Any] = {
            "domain_name": domain_name,
        }
        resp = await self.post(
            f"/v1/domains/{domain_name}/bundles/",
            data=str(createresourcebundlerequest)
            if not issubclass(type(createresourcebundlerequest), BaseModel)
            else createresourcebundlerequest.model_dump_json(),  # type: ignore
            params=path_params,
        )

        try:
            resp_model = resource_schemas.ResourceBundle.model_validate(resp.json())
        except pydantic_core.ValidationError:
            raise EnsureException(
                f"The response came back in an unexpected format: {resp.text}"
            )
        return resp_model

    async def get_bundle(
        self,
        uid: str,
        domain_name: str,
    ) -> resource_schemas.ResourceBundle:
        """
        Gets a bundle by its database UUID
        """

        path_params: Dict[str, Any] = {
            "uid": uid,
            "domain_name": domain_name,
        }
        resp = await self.get(
            f"/v1/domains/{domain_name}/bundles/{uid}", params=path_params
        )

        try:
            resp_model = resource_schemas.ResourceBundle.model_validate(resp.json())
        except pydantic_core.ValidationError:
            raise EnsureException(
                f"The response came back in an unexpected format: {resp.text}"
            )
        return resp_model

    async def update_bundle(
        self,
        uid: str,
        domain_name: str,
        updateresourcebundlerequest: resource_schemas.UpdateResourceBundleRequest,
    ) -> resource_schemas.ResourceBundle:
        """ """

        path_params: Dict[str, Any] = {
            "uid": uid,
            "domain_name": domain_name,
        }
        resp = await self.put(
            f"/v1/domains/{domain_name}/bundles/{uid}",
            data=str(updateresourcebundlerequest)
            if not issubclass(type(updateresourcebundlerequest), BaseModel)
            else updateresourcebundlerequest.model_dump_json(),  # type: ignore
            params=path_params,
        )

        try:
            resp_model = resource_schemas.ResourceBundle.model_validate(resp.json())
        except pydantic_core.ValidationError:
            raise EnsureException(
                f"The response came back in an unexpected format: {resp.text}"
            )
        return resp_model

    async def remove_bundle(
        self,
        uid: str,
        domain_name: str,
    ) -> resource_schemas.BundleTask:
        """
                Delete a bundle from the database and storage.
        The bundle must already be in an unpublished state otherwise an error will be raised.
        """

        path_params: Dict[str, Any] = {
            "uid": uid,
            "domain_name": domain_name,
        }
        resp = await self.delete(
            f"/v1/domains/{domain_name}/bundles/{uid}", params=path_params
        )

        try:
            resp_model = resource_schemas.BundleTask.model_validate(resp.json())
        except pydantic_core.ValidationError:
            raise EnsureException(
                f"The response came back in an unexpected format: {resp.text}"
            )
        return resp_model

    async def get_bundle_version(
        self,
        uid: str,
        version: str,
        domain_name: str,
    ) -> resource_schemas.BundleManifest:
        """
        Gets a bundle version.
        """

        path_params: Dict[str, Any] = {
            "uid": uid,
            "version": version,
            "domain_name": domain_name,
        }
        resp = await self.get(
            f"/v1/domains/{domain_name}/bundles/{uid}/versions/{version}",
            params=path_params,
        )

        try:
            resp_model = resource_schemas.BundleManifest.model_validate(resp.json())
        except pydantic_core.ValidationError:
            raise EnsureException(
                f"The response came back in an unexpected format: {resp.text}"
            )
        return resp_model

    async def set_bundle_version(
        self,
        uid: str,
        version: str,
        domain_name: str,
    ) -> resource_schemas.ResourceBundle:
        """
        Sets a bundle draft version.
        """

        path_params: Dict[str, Any] = {
            "uid": uid,
            "version": version,
            "domain_name": domain_name,
        }
        resp = await self.put(
            f"/v1/domains/{domain_name}/bundles/{uid}/versions/{version}",
            params=path_params,
        )

        try:
            resp_model = resource_schemas.ResourceBundle.model_validate(resp.json())
        except pydantic_core.ValidationError:
            raise EnsureException(
                f"The response came back in an unexpected format: {resp.text}"
            )
        return resp_model

    async def remove_bundle_version(
        self,
        uid: str,
        version: str,
        domain_name: str,
    ) -> resource_schemas.BundleTask:
        """
        Removes a bundle version. It must not be a draft or current version.
        """

        path_params: Dict[str, Any] = {
            "uid": uid,
            "version": version,
            "domain_name": domain_name,
        }
        resp = await self.delete(
            f"/v1/domains/{domain_name}/bundles/{uid}/versions/{version}",
            params=path_params,
        )

        try:
            resp_model = resource_schemas.BundleTask.model_validate(resp.json())
        except pydantic_core.ValidationError:
            raise EnsureException(
                f"The response came back in an unexpected format: {resp.text}"
            )
        return resp_model

    async def create_tree_bundle(
        self,
        domain_name: str,
        createtreebundlerequest: resource_schemas.CreateTreeBundleRequest,
    ) -> resource_schemas.BundleTask:
        """ """

        path_params: Dict[str, Any] = {
            "domain_name": domain_name,
        }
        resp = await self.post(
            f"/v1/domains/{domain_name}/bundles/tree/",
            data=str(createtreebundlerequest)
            if not issubclass(type(createtreebundlerequest), BaseModel)
            else createtreebundlerequest.model_dump_json(),  # type: ignore
            params=path_params,
        )

        try:
            resp_model = resource_schemas.BundleTask.model_validate(resp.json())
        except pydantic_core.ValidationError:
            raise EnsureException(
                f"The response came back in an unexpected format: {resp.text}"
            )
        return resp_model

    async def get_tree(
        self,
        uid: str,
        domain_name: str,
    ) -> resource_schemas.MerkleTreeModel:
        """ """

        path_params: Dict[str, Any] = {
            "uid": uid,
            "domain_name": domain_name,
        }
        resp = await self.get(
            f"/v1/domains/{domain_name}/bundles/{uid}/tree/", params=path_params
        )

        try:
            resp_model = resource_schemas.MerkleTreeModel.model_validate(resp.json())
        except pydantic_core.ValidationError:
            raise EnsureException(
                f"The response came back in an unexpected format: {resp.text}"
            )
        return resp_model

    async def update_tree_bundle(
        self,
        uid: str,
        domain_name: str,
        updatetreebundlerequest: resource_schemas.UpdateTreeBundleRequest,
    ) -> resource_schemas.BundleTask:
        """ """

        path_params: Dict[str, Any] = {
            "uid": uid,
            "domain_name": domain_name,
        }
        resp = await self.put(
            f"/v1/domains/{domain_name}/bundles/{uid}/tree/",
            data=str(updatetreebundlerequest)
            if not issubclass(type(updatetreebundlerequest), BaseModel)
            else updatetreebundlerequest.model_dump_json(),  # type: ignore
            params=path_params,
        )

        try:
            resp_model = resource_schemas.BundleTask.model_validate(resp.json())
        except pydantic_core.ValidationError:
            raise EnsureException(
                f"The response came back in an unexpected format: {resp.text}"
            )
        return resp_model

    async def get_tree_proof(
        self,
        uid: str,
        domain_name: str,
        treeproofcreation: resource_schemas.TreeProofCreation,
    ) -> Union[object, list]:
        """ """

        path_params: Dict[str, Any] = {
            "uid": uid,
            "domain_name": domain_name,
        }
        resp = await self.post(
            f"/v1/domains/{domain_name}/bundles/{uid}/tree/proof/",
            data=str(treeproofcreation)
            if not issubclass(type(treeproofcreation), BaseModel)
            else treeproofcreation.model_dump_json(),  # type: ignore
            params=path_params,
        )

        try:
            resp_model = Union[object, list].model_validate(resp.json())
        except pydantic_core.ValidationError:
            raise EnsureException(
                f"The response came back in an unexpected format: {resp.text}"
            )
        return resp_model

    async def tree_validate(
        self,
        uid: str,
        domain_name: str,
        treeproofvalidationinput: resource_schemas.TreeProofValidationInput,
    ) -> resource_schemas.TreeProofValidationOutput:
        """ """

        path_params: Dict[str, Any] = {
            "uid": uid,
            "domain_name": domain_name,
        }
        resp = await self.put(
            f"/v1/domains/{domain_name}/bundles/{uid}/tree/proof/",
            data=str(treeproofvalidationinput)
            if not issubclass(type(treeproofvalidationinput), BaseModel)
            else treeproofvalidationinput.model_dump_json(),  # type: ignore
            params=path_params,
        )

        try:
            resp_model = resource_schemas.TreeProofValidationOutput.model_validate(
                resp.json()
            )
        except pydantic_core.ValidationError:
            raise EnsureException(
                f"The response came back in an unexpected format: {resp.text}"
            )
        return resp_model

    async def add_policy(
        self,
        uid: str,
        domain_name: str,
        policy: resource_schemas.Policy,
    ) -> resource_schemas.Policy:
        """ """

        path_params: Dict[str, Any] = {
            "uid": uid,
            "domain_name": domain_name,
        }
        resp = await self.post(
            f"/v1/domains/{domain_name}/bundles/{uid}/policies/",
            data=str(policy)
            if not issubclass(type(policy), BaseModel)
            else policy.model_dump_json(),  # type: ignore
            params=path_params,
        )

        try:
            resp_model = resource_schemas.Policy.model_validate(resp.json())
        except pydantic_core.ValidationError:
            raise EnsureException(
                f"The response came back in an unexpected format: {resp.text}"
            )
        return resp_model

    async def update_policy(
        self,
        uid: str,
        domain_name: str,
        policy: resource_schemas.Policy,
    ) -> resource_schemas.Policy:
        """ """

        path_params: Dict[str, Any] = {
            "uid": uid,
            "domain_name": domain_name,
        }
        resp = await self.put(
            f"/v1/domains/{domain_name}/bundles/{uid}/policies/",
            data=str(policy)
            if not issubclass(type(policy), BaseModel)
            else policy.model_dump_json(),  # type: ignore
            params=path_params,
        )

        try:
            resp_model = resource_schemas.Policy.model_validate(resp.json())
        except pydantic_core.ValidationError:
            raise EnsureException(
                f"The response came back in an unexpected format: {resp.text}"
            )
        return resp_model

    async def remove_policy(
        self,
        uid: str,
        identifier: str,
        domain_name: str,
    ) -> resource_schemas.Policy:
        """ """

        path_params: Dict[str, Any] = {
            "uid": uid,
            "identifier": identifier,
            "domain_name": domain_name,
        }
        resp = await self.delete(
            f"/v1/domains/{domain_name}/bundles/{uid}/policies/{identifier}",
            params=path_params,
        )

        try:
            resp_model = resource_schemas.Policy.model_validate(resp.json())
        except pydantic_core.ValidationError:
            raise EnsureException(
                f"The response came back in an unexpected format: {resp.text}"
            )
        return resp_model

    async def upload_files(
        self,
        file_url: str,
        uid: str,
        domain_name: str,
    ) -> resource_schemas.BundleTask:
        """ """

        upload_file = {"files": open(file_url, "rb")}

        path_params: Dict[str, Any] = {
            "uid": uid,
            "domain_name": domain_name,
        }
        resp = await self.put(
            f"/v1/domains/{domain_name}/bundles/{uid}/files/upload/",
            upload_file=upload_file,
            params=path_params,
        )

        try:
            resp_model = resource_schemas.BundleTask.model_validate(resp.json())
        except pydantic_core.ValidationError:
            raise EnsureException(
                f"The response came back in an unexpected format: {resp.text}"
            )
        return resp_model

    async def edit_files(
        self,
        uid: str,
        domain_name: str,
        updatebundlefilesrequest: resource_schemas.UpdateBundleFilesRequest,
    ) -> resource_schemas.BundleTask:
        """ """

        path_params: Dict[str, Any] = {
            "uid": uid,
            "domain_name": domain_name,
        }
        resp = await self.put(
            f"/v1/domains/{domain_name}/bundles/{uid}/files/edit/",
            data=str(updatebundlefilesrequest)
            if not issubclass(type(updatebundlefilesrequest), BaseModel)
            else updatebundlefilesrequest.model_dump_json(),  # type: ignore
            params=path_params,
        )

        try:
            resp_model = resource_schemas.BundleTask.model_validate(resp.json())
        except pydantic_core.ValidationError:
            raise EnsureException(
                f"The response came back in an unexpected format: {resp.text}"
            )
        return resp_model

    async def get_task(
        self,
        uid: str,
        task_id: str,
        domain_name: str,
    ) -> resource_schemas.BundleTask:
        """ """

        path_params: Dict[str, Any] = {
            "uid": uid,
            "task_id": task_id,
            "domain_name": domain_name,
        }
        resp = await self.get(
            f"/v1/domains/{domain_name}/bundles/{uid}/tasks/{task_id}",
            params=path_params,
        )

        try:
            resp_model = resource_schemas.BundleTask.model_validate(resp.json())
        except pydantic_core.ValidationError:
            raise EnsureException(
                f"The response came back in an unexpected format: {resp.text}"
            )
        return resp_model

    async def update_task(
        self,
        uid: str,
        task_id: str,
        domain_name: str,
        updatebundletask: resource_schemas.UpdateBundleTask,
    ) -> resource_schemas.BundleTask:
        """ """

        path_params: Dict[str, Any] = {
            "uid": uid,
            "task_id": task_id,
            "domain_name": domain_name,
        }
        resp = await self.put(
            f"/v1/domains/{domain_name}/bundles/{uid}/tasks/{task_id}",
            data=str(updatebundletask)
            if not issubclass(type(updatebundletask), BaseModel)
            else updatebundletask.model_dump_json(),  # type: ignore
            params=path_params,
        )

        try:
            resp_model = resource_schemas.BundleTask.model_validate(resp.json())
        except pydantic_core.ValidationError:
            raise EnsureException(
                f"The response came back in an unexpected format: {resp.text}"
            )
        return resp_model

    async def get_tasks(
        self,
        query_arguments: resource_queries.GetTasksQuery,
        uid: str,
        domain_name: str,
    ) -> resource_schemas.PageBundleTask:
        """ """

        # get rid of items where None
        query_params = {
            k: v for k, v in asdict(query_arguments).items() if v is not None
        }

        path_params: Dict[str, Any] = {
            "uid": uid,
            "domain_name": domain_name,
        }
        resp = await self.get(
            f"/v1/domains/{domain_name}/bundles/{uid}/tasks/",
            params=path_params | query_params,
        )

        try:
            resp_model = resource_schemas.PageBundleTask.model_validate(resp.json())
        except pydantic_core.ValidationError:
            raise EnsureException(
                f"The response came back in an unexpected format: {resp.text}"
            )
        return resp_model

    async def propose_transfer(
        self,
        uid: str,
        domain_name: str,
        proposetransferrequest: resource_schemas.ProposeTransferRequest,
    ) -> resource_schemas.Transfer:
        """ """

        path_params: Dict[str, Any] = {
            "uid": uid,
            "domain_name": domain_name,
        }
        resp = await self.post(
            f"/v1/domains/{domain_name}/bundles/{uid}/transfers/",
            data=str(proposetransferrequest)
            if not issubclass(type(proposetransferrequest), BaseModel)
            else proposetransferrequest.model_dump_json(),  # type: ignore
            params=path_params,
        )

        try:
            resp_model = resource_schemas.Transfer.model_validate(resp.json())
        except pydantic_core.ValidationError:
            raise EnsureException(
                f"The response came back in an unexpected format: {resp.text}"
            )
        return resp_model

    async def get_transfer(
        self,
        query_arguments: resource_queries.GetTransferQuery,
        uid: str,
        transfer_id: str,
        domain_name: str,
    ) -> resource_schemas.Transfer:
        """ """

        # get rid of items where None
        query_params = {
            k: v for k, v in asdict(query_arguments).items() if v is not None
        }

        path_params: Dict[str, Any] = {
            "uid": uid,
            "transfer_id": transfer_id,
            "domain_name": domain_name,
        }
        resp = await self.get(
            f"/v1/domains/{domain_name}/bundles/{uid}/transfers/{transfer_id}",
            params=path_params | query_params,
        )

        try:
            resp_model = resource_schemas.Transfer.model_validate(resp.json())
        except pydantic_core.ValidationError:
            raise EnsureException(
                f"The response came back in an unexpected format: {resp.text}"
            )
        return resp_model

    async def update_transfer(
        self,
        query_arguments: resource_queries.UpdateTransferQuery,
        uid: str,
        transfer_id: str,
        domain_name: str,
        updatetransferrequest: resource_schemas.UpdateTransferRequest,
    ) -> resource_schemas.Transfer:
        """
                Update a transfer. This endpoint takes a role independent
        update payload.
        This payload is converted to a role specific update
        based on the requested role specified in the 'role' query parameter.

        For a proposer, the account is the address to transfer from.
        For a receiver, the account is the address to transfer to.

        Possible states that can be set by a proposer are:

        * OPEN - default initial state
        * SUSPENDED - the proposal cannot be edited until it is opened again
        * CLOSED - the proposal is closed. No further changes/updates can be made.

        Possible states that can be set by a receiver are:

        * ACCEPTED - accept the transfer. If a receiver account has been set or is sent in
            this payload, and the current state is OPEN, then the transfer will be attempted.
        * REJECTED - the proposal is rejected and cannot continue.
        """

        # get rid of items where None
        query_params = {
            k: v for k, v in asdict(query_arguments).items() if v is not None
        }

        path_params: Dict[str, Any] = {
            "uid": uid,
            "transfer_id": transfer_id,
            "domain_name": domain_name,
        }
        resp = await self.put(
            f"/v1/domains/{domain_name}/bundles/{uid}/transfers/{transfer_id}",
            data=str(updatetransferrequest)
            if not issubclass(type(updatetransferrequest), BaseModel)
            else updatetransferrequest.model_dump_json(),  # type: ignore
            params=path_params | query_params,
        )

        try:
            resp_model = resource_schemas.Transfer.model_validate(resp.json())
        except pydantic_core.ValidationError:
            raise EnsureException(
                f"The response came back in an unexpected format: {resp.text}"
            )
        return resp_model

    async def get_transfers(
        self,
        query_arguments: resource_queries.GetTransfersQuery,
        domain_name: str,
    ) -> resource_schemas.PageTransfer:
        """ """

        # get rid of items where None
        query_params = {
            k: v for k, v in asdict(query_arguments).items() if v is not None
        }

        path_params: Dict[str, Any] = {
            "domain_name": domain_name,
        }
        resp = await self.get(
            f"/v1/domains/{domain_name}/bundles/transfers/",
            params=path_params | query_params,
        )

        try:
            resp_model = resource_schemas.PageTransfer.model_validate(resp.json())
        except pydantic_core.ValidationError:
            raise EnsureException(
                f"The response came back in an unexpected format: {resp.text}"
            )
        return resp_model

    async def publish_action(
        self,
        uid: str,
        domain_name: str,
        publicationrequest: resource_schemas.PublicationRequest,
    ) -> resource_schemas.BundleTask:
        """ """

        path_params: Dict[str, Any] = {
            "uid": uid,
            "domain_name": domain_name,
        }
        resp = await self.put(
            f"/v1/domains/{domain_name}/bundles/{uid}/publish/",
            data=str(publicationrequest)
            if not issubclass(type(publicationrequest), BaseModel)
            else publicationrequest.model_dump_json(),  # type: ignore
            params=path_params,
        )

        try:
            resp_model = resource_schemas.BundleTask.model_validate(resp.json())
        except pydantic_core.ValidationError:
            raise EnsureException(
                f"The response came back in an unexpected format: {resp.text}"
            )
        return resp_model

    async def get_storages(
        self,
        query_arguments: resource_queries.GetStoragesQuery,
        domain_name: str,
    ) -> resource_schemas.PageStorageView:
        """ """

        # get rid of items where None
        query_params = {
            k: v for k, v in asdict(query_arguments).items() if v is not None
        }

        path_params: Dict[str, Any] = {
            "domain_name": domain_name,
        }
        resp = await self.get(
            f"/v1/domains/{domain_name}/storages/", params=path_params | query_params
        )

        try:
            resp_model = resource_schemas.PageStorageView.model_validate(resp.json())
        except pydantic_core.ValidationError:
            raise EnsureException(
                f"The response came back in an unexpected format: {resp.text}"
            )
        return resp_model

    async def create_storage(
        self,
        domain_name: str,
        createstoragerequest: resource_schemas.CreateStorageRequest,
    ) -> resource_schemas.Storage:
        """
                Create a Storage object.

        The name must be unique within the domain.

        The Config dictionary contains the storage specific details to connect to the storage
        provider as well as any other information needed for communicating with it.

        The description dictionary describes the fields in the config dictionary.

        The adapter name is the class that will be used to communicate with the storage provider.
        Supported adapters are available at the
        """

        path_params: Dict[str, Any] = {
            "domain_name": domain_name,
        }
        resp = await self.post(
            f"/v1/domains/{domain_name}/storages/",
            data=str(createstoragerequest)
            if not issubclass(type(createstoragerequest), BaseModel)
            else createstoragerequest.model_dump_json(),  # type: ignore
            params=path_params,
        )

        try:
            resp_model = resource_schemas.Storage.model_validate(resp.json())
        except pydantic_core.ValidationError:
            raise EnsureException(
                f"The response came back in an unexpected format: {resp.text}"
            )
        return resp_model

    async def get_storage(
        self,
        name: str,
        domain_name: str,
    ) -> resource_schemas.Storage:
        """ """

        path_params: Dict[str, Any] = {
            "name": name,
            "domain_name": domain_name,
        }
        resp = await self.get(
            f"/v1/domains/{domain_name}/storages/{name}", params=path_params
        )

        try:
            resp_model = resource_schemas.Storage.model_validate(resp.json())
        except pydantic_core.ValidationError:
            raise EnsureException(
                f"The response came back in an unexpected format: {resp.text}"
            )
        return resp_model

    async def update_storage(
        self,
        name: str,
        domain_name: str,
        updatestoragerequest: resource_schemas.UpdateStorageRequest,
    ) -> resource_schemas.Storage:
        """ """

        path_params: Dict[str, Any] = {
            "name": name,
            "domain_name": domain_name,
        }
        resp = await self.put(
            f"/v1/domains/{domain_name}/storages/{name}",
            data=str(updatestoragerequest)
            if not issubclass(type(updatestoragerequest), BaseModel)
            else updatestoragerequest.model_dump_json(),  # type: ignore
            params=path_params,
        )

        try:
            resp_model = resource_schemas.Storage.model_validate(resp.json())
        except pydantic_core.ValidationError:
            raise EnsureException(
                f"The response came back in an unexpected format: {resp.text}"
            )
        return resp_model

    async def get_storage_type_views(
        self,
        query_arguments: resource_queries.GetStorageTypeViewsQuery,
        domain_name: str,
    ) -> resource_schemas.PageStorageTypeView:
        """ """

        # get rid of items where None
        query_params = {
            k: v for k, v in asdict(query_arguments).items() if v is not None
        }

        path_params: Dict[str, Any] = {
            "domain_name": domain_name,
        }
        resp = await self.get(
            f"/v1/domains/{domain_name}/storages/storage_types/",
            params=path_params | query_params,
        )

        try:
            resp_model = resource_schemas.PageStorageTypeView.model_validate(
                resp.json()
            )
        except pydantic_core.ValidationError:
            raise EnsureException(
                f"The response came back in an unexpected format: {resp.text}"
            )
        return resp_model

    async def get_org_bundle_profiles(
        self,
        query_arguments: resource_queries.GetOrgBundleProfilesQuery,
        domain_name: str,
        organisation_name: str,
    ) -> resource_schemas.PageBundleProfile:
        """ """

        # get rid of items where None
        query_params = {
            k: v for k, v in asdict(query_arguments).items() if v is not None
        }

        path_params: Dict[str, Any] = {
            "domain_name": domain_name,
            "organisation_name": organisation_name,
        }
        resp = await self.get(
            f"/v1/domains/{domain_name}/organisations/{organisation_name}/bundles/profiles/",
            params=path_params | query_params,
        )

        try:
            resp_model = resource_schemas.PageBundleProfile.model_validate(resp.json())
        except pydantic_core.ValidationError:
            raise EnsureException(
                f"The response came back in an unexpected format: {resp.text}"
            )
        return resp_model

    async def create_org_bundle_profile(
        self,
        domain_name: str,
        organisation_name: str,
        bundleprofilerequest: resource_schemas.BundleProfileRequest,
    ) -> resource_schemas.BundleProfile:
        """ """

        path_params: Dict[str, Any] = {
            "domain_name": domain_name,
            "organisation_name": organisation_name,
        }
        resp = await self.post(
            f"/v1/domains/{domain_name}/organisations/{organisation_name}/bundles/profiles/",
            data=str(bundleprofilerequest)
            if not issubclass(type(bundleprofilerequest), BaseModel)
            else bundleprofilerequest.model_dump_json(),  # type: ignore
            params=path_params,
        )

        try:
            resp_model = resource_schemas.BundleProfile.model_validate(resp.json())
        except pydantic_core.ValidationError:
            raise EnsureException(
                f"The response came back in an unexpected format: {resp.text}"
            )
        return resp_model

    async def get_org_bundle_profile(
        self,
        profile_id: str,
        domain_name: str,
        organisation_name: str,
    ) -> resource_schemas.BundleProfile:
        """
        Gets a bundle by its database UUID
        """

        path_params: Dict[str, Any] = {
            "profile_id": profile_id,
            "domain_name": domain_name,
            "organisation_name": organisation_name,
        }
        resp = await self.get(
            f"/v1/domains/{domain_name}/organisations/{organisation_name}/bundles/profiles/{profile_id}",
            params=path_params,
        )

        try:
            resp_model = resource_schemas.BundleProfile.model_validate(resp.json())
        except pydantic_core.ValidationError:
            raise EnsureException(
                f"The response came back in an unexpected format: {resp.text}"
            )
        return resp_model

    async def update_org_bundle_profile(
        self,
        profile_id: str,
        domain_name: str,
        organisation_name: str,
        updatebundleprofilerequest: resource_schemas.UpdateBundleProfileRequest,
    ) -> resource_schemas.BundleProfile:
        """ """

        path_params: Dict[str, Any] = {
            "profile_id": profile_id,
            "domain_name": domain_name,
            "organisation_name": organisation_name,
        }
        resp = await self.put(
            f"/v1/domains/{domain_name}/organisations/{organisation_name}/bundles/profiles/{profile_id}",
            data=str(updatebundleprofilerequest)
            if not issubclass(type(updatebundleprofilerequest), BaseModel)
            else updatebundleprofilerequest.model_dump_json(),  # type: ignore
            params=path_params,
        )

        try:
            resp_model = resource_schemas.BundleProfile.model_validate(resp.json())
        except pydantic_core.ValidationError:
            raise EnsureException(
                f"The response came back in an unexpected format: {resp.text}"
            )
        return resp_model

    async def delete_org_bundle_profile(
        self,
        profile_id: str,
        domain_name: str,
        organisation_name: str,
    ) -> resource_schemas.BundleProfile:
        """ """

        path_params: Dict[str, Any] = {
            "profile_id": profile_id,
            "domain_name": domain_name,
            "organisation_name": organisation_name,
        }
        resp = await self.delete(
            f"/v1/domains/{domain_name}/organisations/{organisation_name}/bundles/profiles/{profile_id}",
            params=path_params,
        )

        try:
            resp_model = resource_schemas.BundleProfile.model_validate(resp.json())
        except pydantic_core.ValidationError:
            raise EnsureException(
                f"The response came back in an unexpected format: {resp.text}"
            )
        return resp_model

    async def get_org_bundle_events(
        self,
        query_arguments: resource_queries.GetOrgBundleEventsQuery,
        domain_name: str,
        organisation_name: str,
    ) -> resource_schemas.PageBundleEventModel:
        """ """

        # get rid of items where None
        query_params = {
            k: v for k, v in asdict(query_arguments).items() if v is not None
        }

        path_params: Dict[str, Any] = {
            "domain_name": domain_name,
            "organisation_name": organisation_name,
        }
        resp = await self.get(
            f"/v1/domains/{domain_name}/organisations/{organisation_name}/bundles/events/",
            params=path_params | query_params,
        )

        try:
            resp_model = resource_schemas.PageBundleEventModel.model_validate(
                resp.json()
            )
        except pydantic_core.ValidationError:
            raise EnsureException(
                f"The response came back in an unexpected format: {resp.text}"
            )
        return resp_model

    async def get_org_bundle_event(
        self,
        uid: str,
        event_id: str,
        domain_name: str,
        organisation_name: str,
    ) -> resource_schemas.ResourceBundle:
        """
        Gets a bundle by its database UUID
        """

        path_params: Dict[str, Any] = {
            "uid": uid,
            "event_id": event_id,
            "domain_name": domain_name,
            "organisation_name": organisation_name,
        }
        resp = await self.get(
            f"/v1/domains/{domain_name}/organisations/{organisation_name}/bundles/{uid}/events/{event_id}",
            params=path_params,
        )

        try:
            resp_model = resource_schemas.ResourceBundle.model_validate(resp.json())
        except pydantic_core.ValidationError:
            raise EnsureException(
                f"The response came back in an unexpected format: {resp.text}"
            )
        return resp_model

    async def get_org_bundles(
        self,
        query_arguments: resource_queries.GetOrgBundlesQuery,
        domain_name: str,
        organisation_name: str,
    ) -> resource_schemas.PageResourceBundle:
        """ """

        # get rid of items where None
        query_params = {
            k: v for k, v in asdict(query_arguments).items() if v is not None
        }

        path_params: Dict[str, Any] = {
            "domain_name": domain_name,
            "organisation_name": organisation_name,
        }
        resp = await self.get(
            f"/v1/domains/{domain_name}/organisations/{organisation_name}/bundles/",
            params=path_params | query_params,
        )

        try:
            resp_model = resource_schemas.PageResourceBundle.model_validate(resp.json())
        except pydantic_core.ValidationError:
            raise EnsureException(
                f"The response came back in an unexpected format: {resp.text}"
            )
        return resp_model

    async def create_org_bundle(
        self,
        domain_name: str,
        organisation_name: str,
        createresourcebundlerequest: resource_schemas.CreateResourceBundleRequest,
    ) -> resource_schemas.ResourceBundle:
        """ """

        path_params: Dict[str, Any] = {
            "domain_name": domain_name,
            "organisation_name": organisation_name,
        }
        resp = await self.post(
            f"/v1/domains/{domain_name}/organisations/{organisation_name}/bundles/",
            data=str(createresourcebundlerequest)
            if not issubclass(type(createresourcebundlerequest), BaseModel)
            else createresourcebundlerequest.model_dump_json(),  # type: ignore
            params=path_params,
        )

        try:
            resp_model = resource_schemas.ResourceBundle.model_validate(resp.json())
        except pydantic_core.ValidationError:
            raise EnsureException(
                f"The response came back in an unexpected format: {resp.text}"
            )
        return resp_model

    async def get_org_bundle(
        self,
        uid: str,
        domain_name: str,
        organisation_name: str,
    ) -> resource_schemas.ResourceBundle:
        """
        Gets a bundle by its database UUID
        """

        path_params: Dict[str, Any] = {
            "uid": uid,
            "domain_name": domain_name,
            "organisation_name": organisation_name,
        }
        resp = await self.get(
            f"/v1/domains/{domain_name}/organisations/{organisation_name}/bundles/{uid}",
            params=path_params,
        )

        try:
            resp_model = resource_schemas.ResourceBundle.model_validate(resp.json())
        except pydantic_core.ValidationError:
            raise EnsureException(
                f"The response came back in an unexpected format: {resp.text}"
            )
        return resp_model

    async def update_org_bundle(
        self,
        uid: str,
        domain_name: str,
        organisation_name: str,
        updateresourcebundlerequest: resource_schemas.UpdateResourceBundleRequest,
    ) -> resource_schemas.ResourceBundle:
        """ """

        path_params: Dict[str, Any] = {
            "uid": uid,
            "domain_name": domain_name,
            "organisation_name": organisation_name,
        }
        resp = await self.put(
            f"/v1/domains/{domain_name}/organisations/{organisation_name}/bundles/{uid}",
            data=str(updateresourcebundlerequest)
            if not issubclass(type(updateresourcebundlerequest), BaseModel)
            else updateresourcebundlerequest.model_dump_json(),  # type: ignore
            params=path_params,
        )

        try:
            resp_model = resource_schemas.ResourceBundle.model_validate(resp.json())
        except pydantic_core.ValidationError:
            raise EnsureException(
                f"The response came back in an unexpected format: {resp.text}"
            )
        return resp_model

    async def remove_org_bundle(
        self,
        uid: str,
        domain_name: str,
        organisation_name: str,
    ) -> resource_schemas.BundleTask:
        """
                Delete a bundle from the database and storage.
        The bundle must already be in an unpublished state otherwise an error will be raised.
        """

        path_params: Dict[str, Any] = {
            "uid": uid,
            "domain_name": domain_name,
            "organisation_name": organisation_name,
        }
        resp = await self.delete(
            f"/v1/domains/{domain_name}/organisations/{organisation_name}/bundles/{uid}",
            params=path_params,
        )

        try:
            resp_model = resource_schemas.BundleTask.model_validate(resp.json())
        except pydantic_core.ValidationError:
            raise EnsureException(
                f"The response came back in an unexpected format: {resp.text}"
            )
        return resp_model

    async def create_org_tree_bundle(
        self,
        domain_name: str,
        organisation_name: str,
        createtreebundlerequest: resource_schemas.CreateTreeBundleRequest,
    ) -> resource_schemas.BundleTask:
        """ """

        path_params: Dict[str, Any] = {
            "domain_name": domain_name,
            "organisation_name": organisation_name,
        }
        resp = await self.post(
            f"/v1/domains/{domain_name}/organisations/{organisation_name}/bundles/tree/",
            data=str(createtreebundlerequest)
            if not issubclass(type(createtreebundlerequest), BaseModel)
            else createtreebundlerequest.model_dump_json(),  # type: ignore
            params=path_params,
        )

        try:
            resp_model = resource_schemas.BundleTask.model_validate(resp.json())
        except pydantic_core.ValidationError:
            raise EnsureException(
                f"The response came back in an unexpected format: {resp.text}"
            )
        return resp_model

    async def get_org_tree(
        self,
        uid: str,
        domain_name: str,
        organisation_name: str,
    ) -> resource_schemas.MerkleTreeModel:
        """ """

        path_params: Dict[str, Any] = {
            "uid": uid,
            "domain_name": domain_name,
            "organisation_name": organisation_name,
        }
        resp = await self.get(
            f"/v1/domains/{domain_name}/organisations/{organisation_name}/bundles/{uid}/tree/",
            params=path_params,
        )

        try:
            resp_model = resource_schemas.MerkleTreeModel.model_validate(resp.json())
        except pydantic_core.ValidationError:
            raise EnsureException(
                f"The response came back in an unexpected format: {resp.text}"
            )
        return resp_model

    async def update_org_tree_bundle(
        self,
        uid: str,
        domain_name: str,
        organisation_name: str,
        updatetreebundlerequest: resource_schemas.UpdateTreeBundleRequest,
    ) -> resource_schemas.BundleTask:
        """ """

        path_params: Dict[str, Any] = {
            "uid": uid,
            "domain_name": domain_name,
            "organisation_name": organisation_name,
        }
        resp = await self.put(
            f"/v1/domains/{domain_name}/organisations/{organisation_name}/bundles/{uid}/tree/",
            data=str(updatetreebundlerequest)
            if not issubclass(type(updatetreebundlerequest), BaseModel)
            else updatetreebundlerequest.model_dump_json(),  # type: ignore
            params=path_params,
        )

        try:
            resp_model = resource_schemas.BundleTask.model_validate(resp.json())
        except pydantic_core.ValidationError:
            raise EnsureException(
                f"The response came back in an unexpected format: {resp.text}"
            )
        return resp_model

    async def get_org_tree_proof(
        self,
        uid: str,
        domain_name: str,
        organisation_name: str,
        treeproofcreation: resource_schemas.TreeProofCreation,
    ) -> Union[object, list]:
        """ """

        path_params: Dict[str, Any] = {
            "uid": uid,
            "domain_name": domain_name,
            "organisation_name": organisation_name,
        }
        resp = await self.post(
            f"/v1/domains/{domain_name}/organisations/{organisation_name}/bundles/{uid}/tree/proof/",
            data=str(treeproofcreation)
            if not issubclass(type(treeproofcreation), BaseModel)
            else treeproofcreation.model_dump_json(),  # type: ignore
            params=path_params,
        )

        try:
            resp_model = Union[object, list].model_validate(resp.json())
        except pydantic_core.ValidationError:
            raise EnsureException(
                f"The response came back in an unexpected format: {resp.text}"
            )
        return resp_model

    async def org_tree_validate(
        self,
        uid: str,
        domain_name: str,
        organisation_name: str,
        treeproofvalidationinput: resource_schemas.TreeProofValidationInput,
    ) -> resource_schemas.TreeProofValidationOutput:
        """ """

        path_params: Dict[str, Any] = {
            "uid": uid,
            "domain_name": domain_name,
            "organisation_name": organisation_name,
        }
        resp = await self.put(
            f"/v1/domains/{domain_name}/organisations/{organisation_name}/bundles/{uid}/tree/proof/",
            data=str(treeproofvalidationinput)
            if not issubclass(type(treeproofvalidationinput), BaseModel)
            else treeproofvalidationinput.model_dump_json(),  # type: ignore
            params=path_params,
        )

        try:
            resp_model = resource_schemas.TreeProofValidationOutput.model_validate(
                resp.json()
            )
        except pydantic_core.ValidationError:
            raise EnsureException(
                f"The response came back in an unexpected format: {resp.text}"
            )
        return resp_model

    async def get_org_bundle_version(
        self,
        uid: str,
        version: str,
        domain_name: str,
        organisation_name: str,
    ) -> resource_schemas.BundleManifest:
        """
        Gets a bundle version.
        """

        path_params: Dict[str, Any] = {
            "uid": uid,
            "version": version,
            "domain_name": domain_name,
            "organisation_name": organisation_name,
        }
        resp = await self.get(
            f"/v1/domains/{domain_name}/organisations/{organisation_name}/bundles/{uid}/versions/{version}",
            params=path_params,
        )

        try:
            resp_model = resource_schemas.BundleManifest.model_validate(resp.json())
        except pydantic_core.ValidationError:
            raise EnsureException(
                f"The response came back in an unexpected format: {resp.text}"
            )
        return resp_model

    async def set_org_bundle_version(
        self,
        uid: str,
        version: str,
        domain_name: str,
        organisation_name: str,
    ) -> resource_schemas.ResourceBundle:
        """
        Sets a bundle draft version.
        """

        path_params: Dict[str, Any] = {
            "uid": uid,
            "version": version,
            "domain_name": domain_name,
            "organisation_name": organisation_name,
        }
        resp = await self.put(
            f"/v1/domains/{domain_name}/organisations/{organisation_name}/bundles/{uid}/versions/{version}",
            params=path_params,
        )

        try:
            resp_model = resource_schemas.ResourceBundle.model_validate(resp.json())
        except pydantic_core.ValidationError:
            raise EnsureException(
                f"The response came back in an unexpected format: {resp.text}"
            )
        return resp_model

    async def remove_org_bundle_version(
        self,
        uid: str,
        version: str,
        domain_name: str,
        organisation_name: str,
    ) -> resource_schemas.BundleTask:
        """
        Removes a bundle version. It must not be a draft or current version.
        """

        path_params: Dict[str, Any] = {
            "uid": uid,
            "version": version,
            "domain_name": domain_name,
            "organisation_name": organisation_name,
        }
        resp = await self.delete(
            f"/v1/domains/{domain_name}/organisations/{organisation_name}/bundles/{uid}/versions/{version}",
            params=path_params,
        )

        try:
            resp_model = resource_schemas.BundleTask.model_validate(resp.json())
        except pydantic_core.ValidationError:
            raise EnsureException(
                f"The response came back in an unexpected format: {resp.text}"
            )
        return resp_model

    async def add_org_policy(
        self,
        uid: str,
        domain_name: str,
        organisation_name: str,
        policy: resource_schemas.Policy,
    ) -> resource_schemas.Policy:
        """ """

        path_params: Dict[str, Any] = {
            "uid": uid,
            "domain_name": domain_name,
            "organisation_name": organisation_name,
        }
        resp = await self.post(
            f"/v1/domains/{domain_name}/organisations/{organisation_name}/bundles/{uid}/policies/",
            data=str(policy)
            if not issubclass(type(policy), BaseModel)
            else policy.model_dump_json(),  # type: ignore
            params=path_params,
        )

        try:
            resp_model = resource_schemas.Policy.model_validate(resp.json())
        except pydantic_core.ValidationError:
            raise EnsureException(
                f"The response came back in an unexpected format: {resp.text}"
            )
        return resp_model

    async def update_org_policy(
        self,
        uid: str,
        domain_name: str,
        organisation_name: str,
        policy: resource_schemas.Policy,
    ) -> resource_schemas.Policy:
        """ """

        path_params: Dict[str, Any] = {
            "uid": uid,
            "domain_name": domain_name,
            "organisation_name": organisation_name,
        }
        resp = await self.put(
            f"/v1/domains/{domain_name}/organisations/{organisation_name}/bundles/{uid}/policies/",
            data=str(policy)
            if not issubclass(type(policy), BaseModel)
            else policy.model_dump_json(),  # type: ignore
            params=path_params,
        )

        try:
            resp_model = resource_schemas.Policy.model_validate(resp.json())
        except pydantic_core.ValidationError:
            raise EnsureException(
                f"The response came back in an unexpected format: {resp.text}"
            )
        return resp_model

    async def remove_org_policy(
        self,
        uid: str,
        identifier: str,
        domain_name: str,
        organisation_name: str,
    ) -> resource_schemas.Policy:
        """ """

        path_params: Dict[str, Any] = {
            "uid": uid,
            "identifier": identifier,
            "domain_name": domain_name,
            "organisation_name": organisation_name,
        }
        resp = await self.delete(
            f"/v1/domains/{domain_name}/organisations/{organisation_name}/bundles/{uid}/policies/{identifier}",
            params=path_params,
        )

        try:
            resp_model = resource_schemas.Policy.model_validate(resp.json())
        except pydantic_core.ValidationError:
            raise EnsureException(
                f"The response came back in an unexpected format: {resp.text}"
            )
        return resp_model

    async def upload_org_files(
        self,
        file_url: str,
        uid: str,
        domain_name: str,
        organisation_name: str,
    ) -> resource_schemas.BundleTask:
        """ """

        upload_file = {"files": open(file_url, "rb")}

        path_params: Dict[str, Any] = {
            "uid": uid,
            "domain_name": domain_name,
            "organisation_name": organisation_name,
        }
        resp = await self.put(
            f"/v1/domains/{domain_name}/organisations/{organisation_name}/bundles/{uid}/files/upload/",
            upload_file=upload_file,
            params=path_params,
        )

        try:
            resp_model = resource_schemas.BundleTask.model_validate(resp.json())
        except pydantic_core.ValidationError:
            raise EnsureException(
                f"The response came back in an unexpected format: {resp.text}"
            )
        return resp_model

    async def edit_org_files(
        self,
        uid: str,
        domain_name: str,
        organisation_name: str,
        updatebundlefilesrequest: resource_schemas.UpdateBundleFilesRequest,
    ) -> resource_schemas.BundleTask:
        """ """

        path_params: Dict[str, Any] = {
            "uid": uid,
            "domain_name": domain_name,
            "organisation_name": organisation_name,
        }
        resp = await self.put(
            f"/v1/domains/{domain_name}/organisations/{organisation_name}/bundles/{uid}/files/edit/",
            data=str(updatebundlefilesrequest)
            if not issubclass(type(updatebundlefilesrequest), BaseModel)
            else updatebundlefilesrequest.model_dump_json(),  # type: ignore
            params=path_params,
        )

        try:
            resp_model = resource_schemas.BundleTask.model_validate(resp.json())
        except pydantic_core.ValidationError:
            raise EnsureException(
                f"The response came back in an unexpected format: {resp.text}"
            )
        return resp_model

    async def get_org_task(
        self,
        uid: str,
        task_id: str,
        domain_name: str,
        organisation_name: str,
    ) -> resource_schemas.BundleTask:
        """ """

        path_params: Dict[str, Any] = {
            "uid": uid,
            "task_id": task_id,
            "domain_name": domain_name,
            "organisation_name": organisation_name,
        }
        resp = await self.get(
            f"/v1/domains/{domain_name}/organisations/{organisation_name}/bundles/{uid}/tasks/{task_id}",
            params=path_params,
        )

        try:
            resp_model = resource_schemas.BundleTask.model_validate(resp.json())
        except pydantic_core.ValidationError:
            raise EnsureException(
                f"The response came back in an unexpected format: {resp.text}"
            )
        return resp_model

    async def update_org_task(
        self,
        uid: str,
        task_id: str,
        domain_name: str,
        organisation_name: str,
        updatebundletask: resource_schemas.UpdateBundleTask,
    ) -> resource_schemas.BundleTask:
        """ """

        path_params: Dict[str, Any] = {
            "uid": uid,
            "task_id": task_id,
            "domain_name": domain_name,
            "organisation_name": organisation_name,
        }
        resp = await self.put(
            f"/v1/domains/{domain_name}/organisations/{organisation_name}/bundles/{uid}/tasks/{task_id}",
            data=str(updatebundletask)
            if not issubclass(type(updatebundletask), BaseModel)
            else updatebundletask.model_dump_json(),  # type: ignore
            params=path_params,
        )

        try:
            resp_model = resource_schemas.BundleTask.model_validate(resp.json())
        except pydantic_core.ValidationError:
            raise EnsureException(
                f"The response came back in an unexpected format: {resp.text}"
            )
        return resp_model

    async def get_org_tasks(
        self,
        query_arguments: resource_queries.GetOrgTasksQuery,
        uid: str,
        domain_name: str,
        organisation_name: str,
    ) -> resource_schemas.PageBundleTask:
        """ """

        # get rid of items where None
        query_params = {
            k: v for k, v in asdict(query_arguments).items() if v is not None
        }

        path_params: Dict[str, Any] = {
            "uid": uid,
            "domain_name": domain_name,
            "organisation_name": organisation_name,
        }
        resp = await self.get(
            f"/v1/domains/{domain_name}/organisations/{organisation_name}/bundles/{uid}/tasks/",
            params=path_params | query_params,
        )

        try:
            resp_model = resource_schemas.PageBundleTask.model_validate(resp.json())
        except pydantic_core.ValidationError:
            raise EnsureException(
                f"The response came back in an unexpected format: {resp.text}"
            )
        return resp_model

    async def publish_org_action(
        self,
        uid: str,
        domain_name: str,
        organisation_name: str,
        publicationrequest: resource_schemas.PublicationRequest,
    ) -> resource_schemas.BundleTask:
        """ """

        path_params: Dict[str, Any] = {
            "uid": uid,
            "domain_name": domain_name,
            "organisation_name": organisation_name,
        }
        resp = await self.put(
            f"/v1/domains/{domain_name}/organisations/{organisation_name}/bundles/{uid}/publish/",
            data=str(publicationrequest)
            if not issubclass(type(publicationrequest), BaseModel)
            else publicationrequest.model_dump_json(),  # type: ignore
            params=path_params,
        )

        try:
            resp_model = resource_schemas.BundleTask.model_validate(resp.json())
        except pydantic_core.ValidationError:
            raise EnsureException(
                f"The response came back in an unexpected format: {resp.text}"
            )
        return resp_model

    async def propose_org_transfer(
        self,
        uid: str,
        domain_name: str,
        organisation_name: str,
        proposetransferrequest: resource_schemas.ProposeTransferRequest,
    ) -> resource_schemas.Transfer:
        """ """

        path_params: Dict[str, Any] = {
            "uid": uid,
            "domain_name": domain_name,
            "organisation_name": organisation_name,
        }
        resp = await self.post(
            f"/v1/domains/{domain_name}/organisations/{organisation_name}/bundles/{uid}/transfers/",
            data=str(proposetransferrequest)
            if not issubclass(type(proposetransferrequest), BaseModel)
            else proposetransferrequest.model_dump_json(),  # type: ignore
            params=path_params,
        )

        try:
            resp_model = resource_schemas.Transfer.model_validate(resp.json())
        except pydantic_core.ValidationError:
            raise EnsureException(
                f"The response came back in an unexpected format: {resp.text}"
            )
        return resp_model

    async def get_org_transfer(
        self,
        query_arguments: resource_queries.GetOrgTransferQuery,
        uid: str,
        transfer_id: str,
        domain_name: str,
        organisation_name: str,
    ) -> resource_schemas.Transfer:
        """ """

        # get rid of items where None
        query_params = {
            k: v for k, v in asdict(query_arguments).items() if v is not None
        }

        path_params: Dict[str, Any] = {
            "uid": uid,
            "transfer_id": transfer_id,
            "domain_name": domain_name,
            "organisation_name": organisation_name,
        }
        resp = await self.get(
            f"/v1/domains/{domain_name}/organisations/{organisation_name}/bundles/{uid}/transfers/{transfer_id}",
            params=path_params | query_params,
        )

        try:
            resp_model = resource_schemas.Transfer.model_validate(resp.json())
        except pydantic_core.ValidationError:
            raise EnsureException(
                f"The response came back in an unexpected format: {resp.text}"
            )
        return resp_model

    async def update_org_transfer(
        self,
        query_arguments: resource_queries.UpdateOrgTransferQuery,
        uid: str,
        transfer_id: str,
        domain_name: str,
        organisation_name: str,
        updatetransferrequest: resource_schemas.UpdateTransferRequest,
    ) -> resource_schemas.Transfer:
        """
                Update a transfer. This endpoint takes a role independent
        update payload.
        This payload is converted to a role specific update
        based on the requested role specified in the 'role' query parameter.

        For a proposer, the account is the address to transfer from.
        For a receiver, the account is the address to transfer to.

        Possible states that can be set by a proposer are:

        * OPEN - default initial state
        * SUSPENDED - the proposal cannot be edited until it is opened again
        * CLOSED - the proposal is closed. No further changes/updates can be made.

        Possible states that can be set by a receiver are:

        * ACCEPTED - accept the transfer. If a receiver account has been set or is sent in
            this payload, and the current state is OPEN, then the transfer will be attempted.
        * REJECTED - the proposal is rejected and cannot continue.
        """

        # get rid of items where None
        query_params = {
            k: v for k, v in asdict(query_arguments).items() if v is not None
        }

        path_params: Dict[str, Any] = {
            "uid": uid,
            "transfer_id": transfer_id,
            "domain_name": domain_name,
            "organisation_name": organisation_name,
        }
        resp = await self.put(
            f"/v1/domains/{domain_name}/organisations/{organisation_name}/bundles/{uid}/transfers/{transfer_id}",
            data=str(updatetransferrequest)
            if not issubclass(type(updatetransferrequest), BaseModel)
            else updatetransferrequest.model_dump_json(),  # type: ignore
            params=path_params | query_params,
        )

        try:
            resp_model = resource_schemas.Transfer.model_validate(resp.json())
        except pydantic_core.ValidationError:
            raise EnsureException(
                f"The response came back in an unexpected format: {resp.text}"
            )
        return resp_model

    async def get_org_transfers(
        self,
        query_arguments: resource_queries.GetOrgTransfersQuery,
        domain_name: str,
        organisation_name: str,
    ) -> resource_schemas.PageTransfer:
        """ """

        # get rid of items where None
        query_params = {
            k: v for k, v in asdict(query_arguments).items() if v is not None
        }

        path_params: Dict[str, Any] = {
            "domain_name": domain_name,
            "organisation_name": organisation_name,
        }
        resp = await self.get(
            f"/v1/domains/{domain_name}/organisations/{organisation_name}/bundles/transfers/",
            params=path_params | query_params,
        )

        try:
            resp_model = resource_schemas.PageTransfer.model_validate(resp.json())
        except pydantic_core.ValidationError:
            raise EnsureException(
                f"The response came back in an unexpected format: {resp.text}"
            )
        return resp_model

    async def get_org_storages(
        self,
        query_arguments: resource_queries.GetOrgStoragesQuery,
        domain_name: str,
        organisation_name: str,
    ) -> resource_schemas.PageStorageView:
        """ """

        # get rid of items where None
        query_params = {
            k: v for k, v in asdict(query_arguments).items() if v is not None
        }

        path_params: Dict[str, Any] = {
            "domain_name": domain_name,
            "organisation_name": organisation_name,
        }
        resp = await self.get(
            f"/v1/domains/{domain_name}/organisations/{organisation_name}/storages/",
            params=path_params | query_params,
        )

        try:
            resp_model = resource_schemas.PageStorageView.model_validate(resp.json())
        except pydantic_core.ValidationError:
            raise EnsureException(
                f"The response came back in an unexpected format: {resp.text}"
            )
        return resp_model

    async def create_org_storage(
        self,
        domain_name: str,
        organisation_name: str,
        createstoragerequest: resource_schemas.CreateStorageRequest,
    ) -> resource_schemas.Storage:
        """
                Create a Storage object.

        The name must be unique within the domain.

        The Config dictionary contains the storage specific details to connect to the storage
        provider as well as any other information needed for communicating with it.

        The description dictionary describes the fields in the config dictionary.

        The adapter name is the class that will be used to communicate with the storage provider.
        Supported adapters are available at the
        """

        path_params: Dict[str, Any] = {
            "domain_name": domain_name,
            "organisation_name": organisation_name,
        }
        resp = await self.post(
            f"/v1/domains/{domain_name}/organisations/{organisation_name}/storages/",
            data=str(createstoragerequest)
            if not issubclass(type(createstoragerequest), BaseModel)
            else createstoragerequest.model_dump_json(),  # type: ignore
            params=path_params,
        )

        try:
            resp_model = resource_schemas.Storage.model_validate(resp.json())
        except pydantic_core.ValidationError:
            raise EnsureException(
                f"The response came back in an unexpected format: {resp.text}"
            )
        return resp_model

    async def get_org_storage(
        self,
        name: str,
        domain_name: str,
        organisation_name: str,
    ) -> resource_schemas.Storage:
        """ """

        path_params: Dict[str, Any] = {
            "name": name,
            "domain_name": domain_name,
            "organisation_name": organisation_name,
        }
        resp = await self.get(
            f"/v1/domains/{domain_name}/organisations/{organisation_name}/storages/{name}",
            params=path_params,
        )

        try:
            resp_model = resource_schemas.Storage.model_validate(resp.json())
        except pydantic_core.ValidationError:
            raise EnsureException(
                f"The response came back in an unexpected format: {resp.text}"
            )
        return resp_model

    async def update_org_storage(
        self,
        name: str,
        domain_name: str,
        organisation_name: str,
        updatestoragerequest: resource_schemas.UpdateStorageRequest,
    ) -> resource_schemas.Storage:
        """ """

        path_params: Dict[str, Any] = {
            "name": name,
            "domain_name": domain_name,
            "organisation_name": organisation_name,
        }
        resp = await self.put(
            f"/v1/domains/{domain_name}/organisations/{organisation_name}/storages/{name}",
            data=str(updatestoragerequest)
            if not issubclass(type(updatestoragerequest), BaseModel)
            else updatestoragerequest.model_dump_json(),  # type: ignore
            params=path_params,
        )

        try:
            resp_model = resource_schemas.Storage.model_validate(resp.json())
        except pydantic_core.ValidationError:
            raise EnsureException(
                f"The response came back in an unexpected format: {resp.text}"
            )
        return resp_model

    async def get_schema_data(
        self,
        query_arguments: resource_queries.GetSchemaDataQuery,
        name: str,
        domain_name: str,
    ) -> resource_schemas.InternalSchemaModel:
        """ """

        # get rid of items where None
        query_params = {
            k: v for k, v in asdict(query_arguments).items() if v is not None
        }

        path_params: Dict[str, Any] = {
            "name": name,
            "domain_name": domain_name,
        }
        resp = await self.get(
            f"/v1/domains/{domain_name}/schemas/name/{name}",
            params=path_params | query_params,
        )

        try:
            resp_model = resource_schemas.InternalSchemaModel.model_validate(
                resp.json()
            )
        except pydantic_core.ValidationError:
            raise EnsureException(
                f"The response came back in an unexpected format: {resp.text}"
            )
        return resp_model

    async def upsert_schema_data(
        self,
        name: str,
        domain_name: str,
        schemasetrequest: resource_schemas.SchemaSetRequest,
    ) -> resource_schemas.SchemaEditResponse:
        """ """

        path_params: Dict[str, Any] = {
            "name": name,
            "domain_name": domain_name,
        }
        resp = await self.post(
            f"/v1/domains/{domain_name}/schemas/name/{name}",
            data=str(schemasetrequest)
            if not issubclass(type(schemasetrequest), BaseModel)
            else schemasetrequest.model_dump_json(),  # type: ignore
            params=path_params,
        )

        try:
            resp_model = resource_schemas.SchemaEditResponse.model_validate(resp.json())
        except pydantic_core.ValidationError:
            raise EnsureException(
                f"The response came back in an unexpected format: {resp.text}"
            )
        return resp_model

    async def delete_schema_data(
        self,
        name: str,
        domain_name: str,
    ) -> resource_schemas.SchemaEditResponse:
        """ """

        path_params: Dict[str, Any] = {
            "name": name,
            "domain_name": domain_name,
        }
        resp = await self.delete(
            f"/v1/domains/{domain_name}/schemas/name/{name}", params=path_params
        )

        try:
            resp_model = resource_schemas.SchemaEditResponse.model_validate(resp.json())
        except pydantic_core.ValidationError:
            raise EnsureException(
                f"The response came back in an unexpected format: {resp.text}"
            )
        return resp_model

    async def get_schema_data_by_id(
        self,
        schema_id: str,
        domain_name: str,
    ) -> resource_schemas.InternalSchemaModel:
        """ """

        path_params: Dict[str, Any] = {
            "schema_id": schema_id,
            "domain_name": domain_name,
        }
        resp = await self.get(
            f"/v1/domains/{domain_name}/schemas/{schema_id}", params=path_params
        )

        try:
            resp_model = resource_schemas.InternalSchemaModel.model_validate(
                resp.json()
            )
        except pydantic_core.ValidationError:
            raise EnsureException(
                f"The response came back in an unexpected format: {resp.text}"
            )
        return resp_model

    async def get_version(
        self,
    ) -> str:
        """
        Returns the version of the code running.
        """

        path_params: Dict[str, Any] = {}
        resp = await self.get("/v1/version/", params=path_params)

        resp_model = str(resp.json())  # type: ignore
        return resp_model

    async def suspend_external(
        self,
        suspendexternalprocessmanagement: resource_schemas.SuspendExternalProcessManagement,
    ) -> str:
        """
        Suspends or resumes the external process service.
        """

        path_params: Dict[str, Any] = {}
        resp = await self.put(
            "/v1/external/",
            data=str(suspendexternalprocessmanagement)
            if not issubclass(type(suspendexternalprocessmanagement), BaseModel)
            else suspendexternalprocessmanagement.model_dump_json(),  # type: ignore
            params=path_params,
        )

        resp_model = str(resp.json())  # type: ignore
        return resp_model

    async def get_domains(
        self,
        query_arguments: resource_queries.GetDomainsQuery,
    ) -> resource_schemas.PageDomain:
        """
        Get Domains in the system
        """

        # get rid of items where None
        query_params = {
            k: v for k, v in asdict(query_arguments).items() if v is not None
        }

        path_params: Dict[str, Any] = {}
        resp = await self.get("/v1/domains/", params=path_params | query_params)

        try:
            resp_model = resource_schemas.PageDomain.model_validate(resp.json())
        except pydantic_core.ValidationError:
            raise EnsureException(
                f"The response came back in an unexpected format: {resp.text}"
            )
        return resp_model

    async def create_domain(
        self,
        createdomain: resource_schemas.CreateDomain,
    ) -> resource_schemas.Domain:
        """
                Create a Domain.

        This is deprecated and delegated to the Member Service.
        """

        path_params: Dict[str, Any] = {}
        resp = await self.post(
            "/v1/domains/",
            data=str(createdomain)
            if not issubclass(type(createdomain), BaseModel)
            else createdomain.model_dump_json(),  # type: ignore
            params=path_params,
        )

        try:
            resp_model = resource_schemas.Domain.model_validate(resp.json())
        except pydantic_core.ValidationError:
            raise EnsureException(
                f"The response came back in an unexpected format: {resp.text}"
            )
        return resp_model

    async def get_domain_configuration(
        self,
        domain_name: str,
    ) -> resource_schemas.AdminDomain:
        """ """

        path_params: Dict[str, Any] = {
            "domain_name": domain_name,
        }
        resp = await self.get(
            f"/v1/configuration/domains/{domain_name}", params=path_params
        )

        try:
            resp_model = resource_schemas.AdminDomain.model_validate(resp.json())
        except pydantic_core.ValidationError:
            raise EnsureException(
                f"The response came back in an unexpected format: {resp.text}"
            )
        return resp_model

    async def configure_domain(
        self,
        domain_name: str,
        domainconfigurationrequest: resource_schemas.DomainConfigurationRequest,
    ) -> resource_schemas.AdminDomain:
        """ """

        path_params: Dict[str, Any] = {
            "domain_name": domain_name,
        }
        resp = await self.put(
            f"/v1/configuration/domains/{domain_name}",
            data=str(domainconfigurationrequest)
            if not issubclass(type(domainconfigurationrequest), BaseModel)
            else domainconfigurationrequest.model_dump_json(),  # type: ignore
            params=path_params,
        )

        try:
            resp_model = resource_schemas.AdminDomain.model_validate(resp.json())
        except pydantic_core.ValidationError:
            raise EnsureException(
                f"The response came back in an unexpected format: {resp.text}"
            )
        return resp_model

    async def get_organisations(
        self,
        query_arguments: resource_queries.GetOrganisationsQuery,
    ) -> resource_schemas.PageOrganisation:
        """
        Get Organisations in the system
        """

        # get rid of items where None
        query_params = {
            k: v for k, v in asdict(query_arguments).items() if v is not None
        }

        path_params: Dict[str, Any] = {}
        resp = await self.get("/v1/organisations/", params=path_params | query_params)

        try:
            resp_model = resource_schemas.PageOrganisation.model_validate(resp.json())
        except pydantic_core.ValidationError:
            raise EnsureException(
                f"The response came back in an unexpected format: {resp.text}"
            )
        return resp_model

    async def get_storage_types(
        self,
        query_arguments: resource_queries.GetStorageTypesQuery,
    ) -> resource_schemas.PageStorageType:
        """
                Get StorageTypes in the system. These represent the possible storage backends supported by the
        service. When creating storage objects per domain,
        """

        # get rid of items where None
        query_params = {
            k: v for k, v in asdict(query_arguments).items() if v is not None
        }

        path_params: Dict[str, Any] = {}
        resp = await self.get("/v1/storage_types/", params=path_params | query_params)

        try:
            resp_model = resource_schemas.PageStorageType.model_validate(resp.json())
        except pydantic_core.ValidationError:
            raise EnsureException(
                f"The response came back in an unexpected format: {resp.text}"
            )
        return resp_model

    async def create_storage_type(
        self,
        createstoragetype: resource_schemas.CreateStorageType,
    ) -> resource_schemas.StorageType:
        """
        Create storage type.
        """

        path_params: Dict[str, Any] = {}
        resp = await self.post(
            "/v1/storage_types/",
            data=str(createstoragetype)
            if not issubclass(type(createstoragetype), BaseModel)
            else createstoragetype.model_dump_json(),  # type: ignore
            params=path_params,
        )

        try:
            resp_model = resource_schemas.StorageType.model_validate(resp.json())
        except pydantic_core.ValidationError:
            raise EnsureException(
                f"The response came back in an unexpected format: {resp.text}"
            )
        return resp_model

    async def get_storage_type(
        self,
        name: str,
    ) -> resource_schemas.StorageType:
        """
        Gets a storage type.
        """

        path_params: Dict[str, Any] = {
            "name": name,
        }
        resp = await self.get(f"/v1/storage_types/{name}", params=path_params)

        try:
            resp_model = resource_schemas.StorageType.model_validate(resp.json())
        except pydantic_core.ValidationError:
            raise EnsureException(
                f"The response came back in an unexpected format: {resp.text}"
            )
        return resp_model

    async def update_storage_type(
        self,
        name: str,
        updatestoragetyperequest: resource_schemas.UpdateStorageTypeRequest,
    ) -> resource_schemas.StorageType:
        """
        Update a storage type
        """

        path_params: Dict[str, Any] = {
            "name": name,
        }
        resp = await self.put(
            f"/v1/storage_types/{name}",
            data=str(updatestoragetyperequest)
            if not issubclass(type(updatestoragetyperequest), BaseModel)
            else updatestoragetyperequest.model_dump_json(),  # type: ignore
            params=path_params,
        )

        try:
            resp_model = resource_schemas.StorageType.model_validate(resp.json())
        except pydantic_core.ValidationError:
            raise EnsureException(
                f"The response came back in an unexpected format: {resp.text}"
            )
        return resp_model

    async def get_users(
        self,
        query_arguments: resource_queries.GetUsersQuery,
    ) -> resource_schemas.PageUser:
        """
                Get Users.

        This returns a paged response of Users known to this service.
        """

        # get rid of items where None
        query_params = {
            k: v for k, v in asdict(query_arguments).items() if v is not None
        }

        path_params: Dict[str, Any] = {}
        resp = await self.get("/v1/users/", params=path_params | query_params)

        try:
            resp_model = resource_schemas.PageUser.model_validate(resp.json())
        except pydantic_core.ValidationError:
            raise EnsureException(
                f"The response came back in an unexpected format: {resp.text}"
            )
        return resp_model

    async def request_access(
        self,
        resource_id: str,
        body: Union[resource_schemas.Presentation, None],
    ) -> resource_schemas.ResourceToken:
        """
                Returns a token that can be used to retrieve a bundle.
        The token may take a little time to become active.
        """

        path_params: Dict[str, Any] = {
            "resource_id": resource_id,
        }
        resp = await self.post(
            f"/v1/access/bundles/{resource_id}",
            data=str(body)
            if not issubclass(type(body), BaseModel)
            else body.model_dump_json(),  # type: ignore
            params=path_params,
        )

        try:
            resp_model = resource_schemas.ResourceToken.model_validate(resp.json())
        except pydantic_core.ValidationError:
            raise EnsureException(
                f"The response came back in an unexpected format: {resp.text}"
            )
        return resp_model

    async def get_access(
        self,
        token: str,
    ) -> bytes:
        """ """

        path_params: Dict[str, Any] = {
            "token": token,
        }
        resp = await self.get(f"/v1/access/bundles/{token}", params=path_params)

        resp_model = bytes(resp.content)  # type: ignore
        return resp_model

    async def get_token(
        self,
        token: str,
    ) -> resource_schemas.ResourceToken:
        """ """

        path_params: Dict[str, Any] = {
            "token": token,
        }
        resp = await self.get(f"/v1/access/tokens/{token}", params=path_params)

        try:
            resp_model = resource_schemas.ResourceToken.model_validate(resp.json())
        except pydantic_core.ValidationError:
            raise EnsureException(
                f"The response came back in an unexpected format: {resp.text}"
            )
        return resp_model

    async def browse_bundles(
        self,
        query_arguments: resource_queries.BrowseBundlesQuery,
        domain_name: str,
    ) -> resource_schemas.PagePublicBundle:
        """ """

        # get rid of items where None
        query_params = {
            k: v for k, v in asdict(query_arguments).items() if v is not None
        }

        path_params: Dict[str, Any] = {
            "domain_name": domain_name,
        }
        resp = await self.get(
            f"/v1/access/domains/{domain_name}/bundles/",
            params=path_params | query_params,
        )

        try:
            resp_model = resource_schemas.PagePublicBundle.model_validate(resp.json())
        except pydantic_core.ValidationError:
            raise EnsureException(
                f"The response came back in an unexpected format: {resp.text}"
            )
        return resp_model

    async def request_public_access(
        self,
        resource_id: str,
        body: Union[resource_schemas.Presentation, None],
    ) -> resource_schemas.ResourceToken:
        """
                Returns a token that can be used to retrieve a bundle.
        The token may take a little time to become active.
        """

        path_params: Dict[str, Any] = {
            "resource_id": resource_id,
        }
        resp = await self.post(
            f"/v1/public/bundles/{resource_id}",
            data=str(body)
            if not issubclass(type(body), BaseModel)
            else body.model_dump_json(),  # type: ignore
            params=path_params,
        )

        try:
            resp_model = resource_schemas.ResourceToken.model_validate(resp.json())
        except pydantic_core.ValidationError:
            raise EnsureException(
                f"The response came back in an unexpected format: {resp.text}"
            )
        return resp_model

    async def get_public_access(
        self,
        token: str,
    ) -> None:
        """ """

        path_params: Dict[str, Any] = {
            "token": token,
        }
        await self.get(f"/v1/public/bundles/{token}", params=path_params)

        return

    async def get_public_token(
        self,
        token: str,
    ) -> resource_schemas.ResourceToken:
        """ """

        path_params: Dict[str, Any] = {
            "token": token,
        }
        resp = await self.get(f"/v1/public/tokens/{token}", params=path_params)

        try:
            resp_model = resource_schemas.ResourceToken.model_validate(resp.json())
        except pydantic_core.ValidationError:
            raise EnsureException(
                f"The response came back in an unexpected format: {resp.text}"
            )
        return resp_model

    async def browse_public_bundles(
        self,
        query_arguments: resource_queries.BrowsePublicBundlesQuery,
        domain_name: str,
    ) -> resource_schemas.PagePublicBundle:
        """ """

        # get rid of items where None
        query_params = {
            k: v for k, v in asdict(query_arguments).items() if v is not None
        }

        path_params: Dict[str, Any] = {
            "domain_name": domain_name,
        }
        resp = await self.get(
            f"/v1/public/domains/{domain_name}/bundles/",
            params=path_params | query_params,
        )

        try:
            resp_model = resource_schemas.PagePublicBundle.model_validate(resp.json())
        except pydantic_core.ValidationError:
            raise EnsureException(
                f"The response came back in an unexpected format: {resp.text}"
            )
        return resp_model

    async def get_redactable(
        self,
    ) -> list:
        """
        Returns possible redactable fields of a public bundle.
        """

        path_params: Dict[str, Any] = {}
        resp = await self.get("/v1/public/redactable_fields/", params=path_params)

        resp_model = list(resp.json())  # type: ignore
        return resp_model

    async def get_tree_info(
        self,
    ) -> object:
        """
        Returns the tree types and their supported proof serialization types.
        """

        path_params: Dict[str, Any] = {}
        resp = await self.get("/v1/public/tree_info/", params=path_params)

        try:
            resp_model = object.model_validate(resp.json())
        except pydantic_core.ValidationError:
            raise EnsureException(
                f"The response came back in an unexpected format: {resp.text}"
            )
        return resp_model

    async def health(
        self,
    ) -> object:
        """
        Returns a status response.
        """

        path_params: Dict[str, Any] = {}
        resp = await self.get("/healthz/", params=path_params)

        try:
            resp_model = object.model_validate(resp.json())
        except pydantic_core.ValidationError:
            raise EnsureException(
                f"The response came back in an unexpected format: {resp.text}"
            )
        return resp_model

    async def ping(
        self,
    ) -> resource_schemas.PingResponses:
        """ """

        path_params: Dict[str, Any] = {}
        resp = await self.get("/pingz/", params=path_params)

        try:
            resp_model = resource_schemas.PingResponses.model_validate(resp.json())
        except pydantic_core.ValidationError:
            raise EnsureException(
                f"The response came back in an unexpected format: {resp.text}"
            )
        return resp_model
