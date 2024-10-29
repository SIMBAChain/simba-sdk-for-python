from dataclasses import asdict
from typing import Any, Dict, Optional, Union

import pydantic_core
from pydantic import BaseModel

from simba_sdk.config import settings
from simba_sdk.core.requests.client.base import Client
from simba_sdk.core.requests.client.members import queries as members_queries
from simba_sdk.core.requests.client.members import schemas as members_schemas
from simba_sdk.core.requests.exception import EnsureException


class MembersClient(Client):
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

    async def onboarding(
        self,
    ) -> None:
        """ """

        path_params: Dict[str, Any] = {}
        await self.get("/onboarding/invites/", params=path_params)

        return

    async def invite_complete(
        self,
    ) -> None:
        """ """

        path_params: Dict[str, Any] = {}
        await self.get("/onboarding/invite_complete/", params=path_params)

        return

    async def get_client_credentials(
        self,
        query_arguments: members_queries.GetClientCredentialsQuery,
        organisation_name: str,
    ) -> members_schemas.PageClientCredential:
        """ """

        # get rid of items where None
        query_params = {
            k: v for k, v in asdict(query_arguments).items() if v is not None
        }

        path_params: Dict[str, Any] = {
            "organisation_name": organisation_name,
        }
        resp = await self.get(
            f"/organisations/{organisation_name}/client_credentials/",
            params=path_params | query_params,
        )

        try:
            resp_model = members_schemas.PageClientCredential.model_validate(
                resp.json()
            )
        except pydantic_core.ValidationError:
            raise EnsureException(
                f"The response came back in an unexpected format: {resp.text}"
            )
        return resp_model

    async def create_client_credential(
        self,
        organisation_name: str,
        createclientcredentialinput: members_schemas.CreateClientCredentialInput,
    ) -> members_schemas.FreshClientCredential:
        """ """

        path_params: Dict[str, Any] = {
            "organisation_name": organisation_name,
        }
        resp = await self.post(
            f"/organisations/{organisation_name}/client_credentials/",
            data=str(createclientcredentialinput)
            if not issubclass(type(createclientcredentialinput), BaseModel)
            else createclientcredentialinput.model_dump_json(),  # type: ignore
            params=path_params,
        )

        try:
            resp_model = members_schemas.FreshClientCredential.model_validate(
                resp.json()
            )
        except pydantic_core.ValidationError:
            raise EnsureException(
                f"The response came back in an unexpected format: {resp.text}"
            )
        return resp_model

    async def get_client_credential(
        self,
        organisation_name: str,
        client_id: str,
    ) -> members_schemas.ClientCredential:
        """ """

        path_params: Dict[str, Any] = {
            "organisation_name": organisation_name,
            "client_id": client_id,
        }
        resp = await self.get(
            f"/organisations/{organisation_name}/client_credentials/{client_id}",
            params=path_params,
        )

        try:
            resp_model = members_schemas.ClientCredential.model_validate(resp.json())
        except pydantic_core.ValidationError:
            raise EnsureException(
                f"The response came back in an unexpected format: {resp.text}"
            )
        return resp_model

    async def update_client_credential(
        self,
        organisation_name: str,
        client_id: str,
        updateclientcredentialinput: members_schemas.UpdateClientCredentialInput,
    ) -> str:
        """ """

        path_params: Dict[str, Any] = {
            "organisation_name": organisation_name,
            "client_id": client_id,
        }
        resp = await self.put(
            f"/organisations/{organisation_name}/client_credentials/{client_id}",
            data=str(updateclientcredentialinput)
            if not issubclass(type(updateclientcredentialinput), BaseModel)
            else updateclientcredentialinput.model_dump_json(),  # type: ignore
            params=path_params,
        )

        resp_model = str(resp.json())  # type: ignore
        return resp_model

    async def revoke_client_credential(
        self,
        organisation_name: str,
        client_id: str,
    ) -> None:
        """ """

        path_params: Dict[str, Any] = {
            "organisation_name": organisation_name,
            "client_id": client_id,
        }
        await self.delete(
            f"/organisations/{organisation_name}/client_credentials/{client_id}",
            params=path_params,
        )

        return

    async def update_client_credential_roles(
        self,
        organisation_name: str,
        client_id: str,
        updateidentityrolesinput: members_schemas.UpdateIdentityRolesInput,
    ) -> str:
        """ """

        path_params: Dict[str, Any] = {
            "organisation_name": organisation_name,
            "client_id": client_id,
        }
        resp = await self.put(
            f"/organisations/{organisation_name}/client_credentials/{client_id}/roles/",
            data=str(updateidentityrolesinput)
            if not issubclass(type(updateidentityrolesinput), BaseModel)
            else updateidentityrolesinput.model_dump_json(),  # type: ignore
            params=path_params,
        )

        resp_model = str(resp.json())  # type: ignore
        return resp_model

    async def add_organisation_client_credential_roles(
        self,
        organisation_name: str,
        client_id: str,
        addidentityrolesinput: members_schemas.AddIdentityRolesInput,
    ) -> str:
        """ """

        path_params: Dict[str, Any] = {
            "organisation_name": organisation_name,
            "client_id": client_id,
        }
        resp = await self.post(
            f"/organisations/{organisation_name}/client_credentials/{client_id}/roles/add/",
            data=str(addidentityrolesinput)
            if not issubclass(type(addidentityrolesinput), BaseModel)
            else addidentityrolesinput.model_dump_json(),  # type: ignore
            params=path_params,
        )

        resp_model = str(resp.json())  # type: ignore
        return resp_model

    async def remove_organisation_client_credential_roles(
        self,
        organisation_name: str,
        client_id: str,
    ) -> str:
        """ """

        path_params: Dict[str, Any] = {
            "organisation_name": organisation_name,
            "client_id": client_id,
        }
        resp = await self.delete(
            f"/organisations/{organisation_name}/client_credentials/{client_id}/roles/remove/",
            params=path_params,
        )

        resp_model = str(resp.json())  # type: ignore
        return resp_model

    async def get_user_client_credentials(
        self,
        query_arguments: members_queries.GetUserClientCredentialsQuery,
        user_account_id: Union[str, None] = None,
    ) -> members_schemas.PageClientCredential:
        """ """

        # get rid of items where None
        query_params = {
            k: v for k, v in asdict(query_arguments).items() if v is not None
        }

        path_params: Dict[str, Any] = {
            "user_account_id": user_account_id,
        }
        resp = await self.get(
            f"/user_accounts/{user_account_id}/client_credentials/",
            params=path_params | query_params,
        )

        try:
            resp_model = members_schemas.PageClientCredential.model_validate(
                resp.json()
            )
        except pydantic_core.ValidationError:
            raise EnsureException(
                f"The response came back in an unexpected format: {resp.text}"
            )
        return resp_model

    async def create_impersonate_user_client_credentials(
        self,
        user_account_id: str,
        createclientcredentialinput: members_schemas.CreateClientCredentialInput,
    ) -> members_schemas.FreshClientCredential:
        """ """

        path_params: Dict[str, Any] = {
            "user_account_id": user_account_id,
        }
        resp = await self.post(
            f"/user_accounts/{user_account_id}/client_credentials/",
            data=str(createclientcredentialinput)
            if not issubclass(type(createclientcredentialinput), BaseModel)
            else createclientcredentialinput.model_dump_json(),  # type: ignore
            params=path_params,
        )

        try:
            resp_model = members_schemas.FreshClientCredential.model_validate(
                resp.json()
            )
        except pydantic_core.ValidationError:
            raise EnsureException(
                f"The response came back in an unexpected format: {resp.text}"
            )
        return resp_model

    async def get_user_client_credential(
        self,
        user_account_id: str,
        client_id: str,
    ) -> members_schemas.ClientCredential:
        """ """

        path_params: Dict[str, Any] = {
            "user_account_id": user_account_id,
            "client_id": client_id,
        }
        resp = await self.get(
            f"/user_accounts/{user_account_id}/client_credentials/{client_id}",
            params=path_params,
        )

        try:
            resp_model = members_schemas.ClientCredential.model_validate(resp.json())
        except pydantic_core.ValidationError:
            raise EnsureException(
                f"The response came back in an unexpected format: {resp.text}"
            )
        return resp_model

    async def update_user_client_credential(
        self,
        user_account_id: str,
        client_id: str,
        updateclientcredentialinput: members_schemas.UpdateClientCredentialInput,
    ) -> str:
        """ """

        path_params: Dict[str, Any] = {
            "user_account_id": user_account_id,
            "client_id": client_id,
        }
        resp = await self.put(
            f"/user_accounts/{user_account_id}/client_credentials/{client_id}",
            data=str(updateclientcredentialinput)
            if not issubclass(type(updateclientcredentialinput), BaseModel)
            else updateclientcredentialinput.model_dump_json(),  # type: ignore
            params=path_params,
        )

        resp_model = str(resp.json())  # type: ignore
        return resp_model

    async def revoke_user_client_credential(
        self,
        user_account_id: str,
        client_id: str,
    ) -> None:
        """ """

        path_params: Dict[str, Any] = {
            "user_account_id": user_account_id,
            "client_id": client_id,
        }
        await self.delete(
            f"/user_accounts/{user_account_id}/client_credentials/{client_id}",
            params=path_params,
        )

        return

    async def get_organisations(
        self,
        query_arguments: members_queries.GetOrganisationsQuery,
    ) -> members_schemas.PageOrganisation:
        """ """

        # get rid of items where None
        query_params = {
            k: v for k, v in asdict(query_arguments).items() if v is not None
        }

        path_params: Dict[str, Any] = {}
        resp = await self.get("/organisations/", params=path_params | query_params)

        try:
            resp_model = members_schemas.PageOrganisation.model_validate(resp.json())
        except pydantic_core.ValidationError:
            raise EnsureException(
                f"The response came back in an unexpected format: {resp.text}"
            )
        return resp_model

    async def create_organisation(
        self,
        createorganisationinput: members_schemas.CreateOrganisationInput,
    ) -> str:
        """ """

        path_params: Dict[str, Any] = {}
        resp = await self.post(
            "/organisations/",
            data=str(createorganisationinput)
            if not issubclass(type(createorganisationinput), BaseModel)
            else createorganisationinput.model_dump_json(),  # type: ignore
            params=path_params,
        )

        resp_model = str(resp.json())  # type: ignore
        return resp_model

    async def get_organisation_by_id(
        self,
        organisation_id: str,
    ) -> members_schemas.Organisation:
        """ """

        path_params: Dict[str, Any] = {
            "organisation_id": organisation_id,
        }
        resp = await self.get(f"/organisations/{organisation_id}", params=path_params)

        try:
            resp_model = members_schemas.Organisation.model_validate(resp.json())
        except pydantic_core.ValidationError:
            raise EnsureException(
                f"The response came back in an unexpected format: {resp.text}"
            )
        return resp_model

    async def update_organisation(
        self,
        organisation_id: str,
        updateorganisationinput: members_schemas.UpdateOrganisationInput,
    ) -> str:
        """ """

        path_params: Dict[str, Any] = {
            "organisation_id": organisation_id,
        }
        resp = await self.put(
            f"/organisations/{organisation_id}",
            data=str(updateorganisationinput)
            if not issubclass(type(updateorganisationinput), BaseModel)
            else updateorganisationinput.model_dump_json(),  # type: ignore
            params=path_params,
        )

        resp_model = str(resp.json())  # type: ignore
        return resp_model

    async def remove_user_from_organisation(
        self,
        user_id: str,
        organisation_id: str,
    ) -> None:
        """ """

        path_params: Dict[str, Any] = {
            "user_id": user_id,
            "organisation_id": organisation_id,
        }
        await self.delete(
            f"/organisations/{organisation_id}/users/{user_id}", params=path_params
        )

        return

    async def check_organisation_name(
        self,
        organisationname: members_schemas.OrganisationName,
    ) -> None:
        """ """

        path_params: Dict[str, Any] = {}
        await self.post(
            "/organisation-input-checks/",
            data=str(organisationname)
            if not issubclass(type(organisationname), BaseModel)
            else organisationname.model_dump_json(),  # type: ignore
            params=path_params,
        )

        return

    async def get_domains(
        self,
        query_arguments: members_queries.GetDomainsQuery,
    ) -> members_schemas.PageDomain:
        """ """

        # get rid of items where None
        query_params = {
            k: v for k, v in asdict(query_arguments).items() if v is not None
        }

        path_params: Dict[str, Any] = {}
        resp = await self.get("/domains/", params=path_params | query_params)

        try:
            resp_model = members_schemas.PageDomain.model_validate(resp.json())
        except pydantic_core.ValidationError:
            raise EnsureException(
                f"The response came back in an unexpected format: {resp.text}"
            )
        return resp_model

    async def create_domain(
        self,
        createdomaininput: members_schemas.CreateDomainInput,
    ) -> str:
        """ """

        path_params: Dict[str, Any] = {}
        resp = await self.post(
            "/domains/",
            data=str(createdomaininput)
            if not issubclass(type(createdomaininput), BaseModel)
            else createdomaininput.model_dump_json(),  # type: ignore
            params=path_params,
        )

        resp_model = str(resp.json())  # type: ignore
        return resp_model

    async def get_domain_by_id(
        self,
        domain_id: str,
    ) -> members_schemas.Domain:
        """ """

        path_params: Dict[str, Any] = {
            "domain_id": domain_id,
        }
        resp = await self.get(f"/domains/{domain_id}", params=path_params)

        try:
            resp_model = members_schemas.Domain.model_validate(resp.json())
        except pydantic_core.ValidationError:
            raise EnsureException(
                f"The response came back in an unexpected format: {resp.text}"
            )
        return resp_model

    async def update_domain(
        self,
        domain_id: str,
        updatedomaininput: members_schemas.UpdateDomainInput,
    ) -> str:
        """ """

        path_params: Dict[str, Any] = {
            "domain_id": domain_id,
        }
        resp = await self.put(
            f"/domains/{domain_id}",
            data=str(updatedomaininput)
            if not issubclass(type(updatedomaininput), BaseModel)
            else updatedomaininput.model_dump_json(),  # type: ignore
            params=path_params,
        )

        resp_model = str(resp.json())  # type: ignore
        return resp_model

    async def add_domain_organisation(
        self,
        domain_name: str,
        adddomainorganisationinput: members_schemas.AddDomainOrganisationInput,
    ) -> str:
        """ """

        path_params: Dict[str, Any] = {
            "domain_name": domain_name,
        }
        resp = await self.post(
            f"/domains/{domain_name}/organisations/",
            data=str(adddomainorganisationinput)
            if not issubclass(type(adddomainorganisationinput), BaseModel)
            else adddomainorganisationinput.model_dump_json(),  # type: ignore
            params=path_params,
        )

        resp_model = str(resp.json())  # type: ignore
        return resp_model

    async def remove_domain_organisation(
        self,
        domain_name: str,
    ) -> str:
        """ """

        path_params: Dict[str, Any] = {
            "domain_name": domain_name,
        }
        resp = await self.delete(
            f"/domains/{domain_name}/organisations/", params=path_params
        )

        resp_model = str(resp.json())  # type: ignore
        return resp_model

    async def republish_events(
        self,
        republisheventsinput: members_schemas.RepublishEventsInput,
    ) -> None:
        """ """

        path_params: Dict[str, Any] = {}
        await self.post(
            "/republish_events/",
            data=str(republisheventsinput)
            if not issubclass(type(republisheventsinput), BaseModel)
            else republisheventsinput.model_dump_json(),  # type: ignore
            params=path_params,
        )

        return

    async def check_domain_name(
        self,
        organisationname: members_schemas.OrganisationName,
    ) -> None:
        """ """

        path_params: Dict[str, Any] = {}
        await self.post(
            "/domain-input-checks/",
            data=str(organisationname)
            if not issubclass(type(organisationname), BaseModel)
            else organisationname.model_dump_json(),  # type: ignore
            params=path_params,
        )

        return

    async def get_permissions(
        self,
        query_arguments: members_queries.GetPermissionsQuery,
    ) -> members_schemas.PagePermission:
        """ """

        # get rid of items where None
        query_params = {
            k: v for k, v in asdict(query_arguments).items() if v is not None
        }

        path_params: Dict[str, Any] = {}
        resp = await self.get("/permissions/", params=path_params | query_params)

        try:
            resp_model = members_schemas.PagePermission.model_validate(resp.json())
        except pydantic_core.ValidationError:
            raise EnsureException(
                f"The response came back in an unexpected format: {resp.text}"
            )
        return resp_model

    async def create_permission(
        self,
        createpermissioninput: members_schemas.CreatePermissionInput,
    ) -> str:
        """ """

        path_params: Dict[str, Any] = {}
        resp = await self.post(
            "/permissions/",
            data=str(createpermissioninput)
            if not issubclass(type(createpermissioninput), BaseModel)
            else createpermissioninput.model_dump_json(),  # type: ignore
            params=path_params,
        )

        resp_model = str(resp.json())  # type: ignore
        return resp_model

    async def get_permission(
        self,
        permission_id: str,
    ) -> members_schemas.Permission:
        """ """

        path_params: Dict[str, Any] = {
            "permission_id": permission_id,
        }
        resp = await self.get(f"/permissions/{permission_id}", params=path_params)

        try:
            resp_model = members_schemas.Permission.model_validate(resp.json())
        except pydantic_core.ValidationError:
            raise EnsureException(
                f"The response came back in an unexpected format: {resp.text}"
            )
        return resp_model

    async def update_permission(
        self,
        permission_id: str,
        updatepermissioninput: members_schemas.UpdatePermissionInput,
    ) -> str:
        """ """

        path_params: Dict[str, Any] = {
            "permission_id": permission_id,
        }
        resp = await self.put(
            f"/permissions/{permission_id}",
            data=str(updatepermissioninput)
            if not issubclass(type(updatepermissioninput), BaseModel)
            else updatepermissioninput.model_dump_json(),  # type: ignore
            params=path_params,
        )

        resp_model = str(resp.json())  # type: ignore
        return resp_model

    async def get_identities_permissions(
        self,
        query_arguments: members_queries.GetIdentitiesPermissionsQuery,
    ) -> members_schemas.GetIdentityPermissions:
        """ """

        # get rid of items where None
        query_params = {
            k: v for k, v in asdict(query_arguments).items() if v is not None
        }

        path_params: Dict[str, Any] = {}
        resp = await self.get(
            "/identity_permissions/", params=path_params | query_params
        )

        try:
            resp_model = members_schemas.GetIdentityPermissions.model_validate(
                resp.json()
            )
        except pydantic_core.ValidationError:
            raise EnsureException(
                f"The response came back in an unexpected format: {resp.text}"
            )
        return resp_model

    async def get_user_permissions(
        self,
        query_arguments: members_queries.GetUserPermissionsQuery,
    ) -> members_schemas.GetIdentityPermissions:
        """ """

        # get rid of items where None
        query_params = {
            k: v for k, v in asdict(query_arguments).items() if v is not None
        }

        path_params: Dict[str, Any] = {}
        resp = await self.get("/users_permissions/", params=path_params | query_params)

        try:
            resp_model = members_schemas.GetIdentityPermissions.model_validate(
                resp.json()
            )
        except pydantic_core.ValidationError:
            raise EnsureException(
                f"The response came back in an unexpected format: {resp.text}"
            )
        return resp_model

    async def get_client_creds_permissions(
        self,
        query_arguments: members_queries.GetClientCredsPermissionsQuery,
    ) -> members_schemas.GetIdentityPermissions:
        """ """

        # get rid of items where None
        query_params = {
            k: v for k, v in asdict(query_arguments).items() if v is not None
        }

        path_params: Dict[str, Any] = {}
        resp = await self.get(
            "/clientcredentials_permissions/", params=path_params | query_params
        )

        try:
            resp_model = members_schemas.GetIdentityPermissions.model_validate(
                resp.json()
            )
        except pydantic_core.ValidationError:
            raise EnsureException(
                f"The response came back in an unexpected format: {resp.text}"
            )
        return resp_model

    async def sync_permission(
        self,
        syncservicepermissions: members_schemas.SyncServicePermissions,
    ) -> None:
        """ """

        path_params: Dict[str, Any] = {}
        await self.post(
            "/sync_permissions/",
            data=str(syncservicepermissions)
            if not issubclass(type(syncservicepermissions), BaseModel)
            else syncservicepermissions.model_dump_json(),  # type: ignore
            params=path_params,
        )

        return

    async def get_roles(
        self,
        query_arguments: members_queries.GetRolesQuery,
    ) -> members_schemas.PageRoleWithFlags:
        """ """

        # get rid of items where None
        query_params = {
            k: v for k, v in asdict(query_arguments).items() if v is not None
        }

        path_params: Dict[str, Any] = {}
        resp = await self.get("/roles/", params=path_params | query_params)

        try:
            resp_model = members_schemas.PageRoleWithFlags.model_validate(resp.json())
        except pydantic_core.ValidationError:
            raise EnsureException(
                f"The response came back in an unexpected format: {resp.text}"
            )
        return resp_model

    async def get_role(
        self,
        role_id: str,
    ) -> members_schemas.Role:
        """ """

        path_params: Dict[str, Any] = {
            "role_id": role_id,
        }
        resp = await self.get(f"/roles/{role_id}", params=path_params)

        try:
            resp_model = members_schemas.Role.model_validate(resp.json())
        except pydantic_core.ValidationError:
            raise EnsureException(
                f"The response came back in an unexpected format: {resp.text}"
            )
        return resp_model

    async def get_templates(
        self,
        query_arguments: members_queries.GetTemplatesQuery,
    ) -> members_schemas.PageTemplate:
        """ """

        # get rid of items where None
        query_params = {
            k: v for k, v in asdict(query_arguments).items() if v is not None
        }

        path_params: Dict[str, Any] = {}
        resp = await self.get("/templates/", params=path_params | query_params)

        try:
            resp_model = members_schemas.PageTemplate.model_validate(resp.json())
        except pydantic_core.ValidationError:
            raise EnsureException(
                f"The response came back in an unexpected format: {resp.text}"
            )
        return resp_model

    async def create_template(
        self,
        createtemplateinput: members_schemas.CreateTemplateInput,
    ) -> str:
        """ """

        path_params: Dict[str, Any] = {}
        resp = await self.post(
            "/templates/",
            data=str(createtemplateinput)
            if not issubclass(type(createtemplateinput), BaseModel)
            else createtemplateinput.model_dump_json(),  # type: ignore
            params=path_params,
        )

        resp_model = str(resp.json())  # type: ignore
        return resp_model

    async def get_template(
        self,
        template_id: str,
    ) -> members_schemas.Template:
        """ """

        path_params: Dict[str, Any] = {
            "template_id": template_id,
        }
        resp = await self.get(f"/templates/{template_id}", params=path_params)

        try:
            resp_model = members_schemas.Template.model_validate(resp.json())
        except pydantic_core.ValidationError:
            raise EnsureException(
                f"The response came back in an unexpected format: {resp.text}"
            )
        return resp_model

    async def update_template(
        self,
        template_id: str,
        updatetemplateinput: members_schemas.UpdateTemplateInput,
    ) -> str:
        """ """

        path_params: Dict[str, Any] = {
            "template_id": template_id,
        }
        resp = await self.put(
            f"/templates/{template_id}",
            data=str(updatetemplateinput)
            if not issubclass(type(updatetemplateinput), BaseModel)
            else updatetemplateinput.model_dump_json(),  # type: ignore
            params=path_params,
        )

        resp_model = str(resp.json())  # type: ignore
        return resp_model

    async def get_user_accounts(
        self,
        query_arguments: members_queries.GetUserAccountsQuery,
    ) -> members_schemas.PageUserAccountWithoutOrganisations:
        """ """

        # get rid of items where None
        query_params = {
            k: v for k, v in asdict(query_arguments).items() if v is not None
        }

        path_params: Dict[str, Any] = {}
        resp = await self.get("/user_accounts/", params=path_params | query_params)

        try:
            resp_model = (
                members_schemas.PageUserAccountWithoutOrganisations.model_validate(
                    resp.json()
                )
            )
        except pydantic_core.ValidationError:
            raise EnsureException(
                f"The response came back in an unexpected format: {resp.text}"
            )
        return resp_model

    async def get_user_account(
        self,
        user_account_id: str,
    ) -> members_schemas.UserAccount:
        """ """

        path_params: Dict[str, Any] = {
            "user_account_id": user_account_id,
        }
        resp = await self.get(f"/user_accounts/{user_account_id}", params=path_params)

        try:
            resp_model = members_schemas.UserAccount.model_validate(resp.json())
        except pydantic_core.ValidationError:
            raise EnsureException(
                f"The response came back in an unexpected format: {resp.text}"
            )
        return resp_model

    async def update_account(
        self,
        user_account_id: str,
        updateuseraccountinput: members_schemas.UpdateUserAccountInput,
    ) -> str:
        """ """

        path_params: Dict[str, Any] = {
            "user_account_id": user_account_id,
        }
        resp = await self.put(
            f"/user_accounts/{user_account_id}",
            data=str(updateuseraccountinput)
            if not issubclass(type(updateuseraccountinput), BaseModel)
            else updateuseraccountinput.model_dump_json(),  # type: ignore
            params=path_params,
        )

        resp_model = str(resp.json())  # type: ignore
        return resp_model

    async def delete_account(
        self,
        user_account_id: str,
    ) -> str:
        """ """

        path_params: Dict[str, Any] = {
            "user_account_id": user_account_id,
        }
        resp = await self.delete(
            f"/user_accounts/{user_account_id}", params=path_params
        )

        resp_model = str(resp.json())  # type: ignore
        return resp_model

    async def whoami(
        self,
    ) -> members_schemas.UserAccount:
        """ """

        path_params: Dict[str, Any] = {}
        resp = await self.get("/user_accounts/whoami/", params=path_params)

        try:
            resp_model = members_schemas.UserAccount.model_validate(resp.json())
        except pydantic_core.ValidationError:
            raise EnsureException(
                f"The response came back in an unexpected format: {resp.text}"
            )
        return resp_model

    async def get_user_profile(
        self,
        user_account_id: str,
        profile_id: str,
    ) -> members_schemas.UserProfile:
        """ """

        path_params: Dict[str, Any] = {
            "user_account_id": user_account_id,
            "profile_id": profile_id,
        }
        resp = await self.get(
            f"/user_accounts/{user_account_id}/user_profiles/{profile_id}",
            params=path_params,
        )

        try:
            resp_model = members_schemas.UserProfile.model_validate(resp.json())
        except pydantic_core.ValidationError:
            raise EnsureException(
                f"The response came back in an unexpected format: {resp.text}"
            )
        return resp_model

    async def update_profile(
        self,
        user_account_id: str,
        profile_id: str,
        updateuserprofileinput: members_schemas.UpdateUserProfileInput,
    ) -> str:
        """ """

        path_params: Dict[str, Any] = {
            "user_account_id": user_account_id,
            "profile_id": profile_id,
        }
        resp = await self.put(
            f"/user_accounts/{user_account_id}/user_profiles/{profile_id}",
            data=str(updateuserprofileinput)
            if not issubclass(type(updateuserprofileinput), BaseModel)
            else updateuserprofileinput.model_dump_json(),  # type: ignore
            params=path_params,
        )

        resp_model = str(resp.json())  # type: ignore
        return resp_model

    async def get_bulk_users_import_requests(
        self,
        query_arguments: members_queries.GetBulkUsersImportRequestsQuery,
    ) -> members_schemas.PageBulkUsersImportRequest:
        """ """

        # get rid of items where None
        query_params = {
            k: v for k, v in asdict(query_arguments).items() if v is not None
        }

        path_params: Dict[str, Any] = {}
        resp = await self.get(
            "/bulk-users-import-requests/", params=path_params | query_params
        )

        try:
            resp_model = members_schemas.PageBulkUsersImportRequest.model_validate(
                resp.json()
            )
        except pydantic_core.ValidationError:
            raise EnsureException(
                f"The response came back in an unexpected format: {resp.text}"
            )
        return resp_model

    async def create_bulk_users_import_request(
        self,
        file_url: str,
    ) -> str:
        """
                ## Uploads a CSV file with organisation/domain, user(s) and roles information
        The endpoint uploads a CSV file, parses it, and saves the data. It is processed asynchronously.

        Args:
        - `bulk_import_file`: A csv file of a specific format to add users to orgs, assign roles, remove roles and set
        default organisation for the user(s)


        Each row specifies the organisation/domains to which the user(s) with the respective role(s) should be added to
        and/or the roles to remove from a user that already belongs to the organisation/domain.

        The user can be a new or existing user.

        Each row in the CSV file should follow the following format:
        **org name, user email;first name;last name|another user;;, roles to add, roles to remove, is_default_org, system_type**
        i.e.:
        org-a,user-1@org.com;user-fn1;user-ln1|user-2@org.com;user-fn2;user-ln2,RoleToAdd1|RoleToAdd2…, RoleToRemove1|RoleToRemove2, True, build

        The CSV follows the following rules:
        - A valid CSV file
        - The file should be less than 1Mb
        - If headers are present the following: org_name, users, add_roles, remove_roles, is_default_org, system_type
        - At least the first two columns are required.
        - Any columns after the first six are ignored.
        - Columns and the rules:
            - **Ist column**: Organisation/domain name.  The organisation or domain to which the user should be added.
                - This is required
                - The organisation or domain should exist, the bulk import does not create organisations or domains
            - **2nd column**: list of users to add to the organisation or domain.
                - At least one user is required
                - There can be multiple users, each separated by a |
                - The structure of a user should be: user's email; user’s first name; user’s last name
                    i.e donald_duck@scass.py;Donald;duck
                - The user email is required and should be a valid email.
                - The first name and last name are optional for existing users i.e.
                    - with no first name and last name: donald_duck@scass.py;; or just donald_duck@scass.py
                    - with just first name: donald_duck@scass.py;Donald; or donald_duck@scass.py;donald
                    - with just the last name donald_duck@scass.py;;duck
                - An example of multiple users: i.e. donald_duck@scass.py;Donald;Duck|daisy_duck@scass.py;daisy;duck
                - A new user should have a first name and last name if the same user is provided multiple times in the bulk import user request, then the last non-null value of the first and last name is used
                - Similarly for existing users, the last non-null entry of the  first name and/or last name is updated if provided
            - **3rd column**: roles to add to the users for the organisation/domain
                - This column is optional
                - A list of role names separated by |. i.e  Admin|GlobalAdmin|...
                - The role should belong to the organisation or domain
                - All global roles are ignored
            - **4th column**: The third column: roles to remove to the users for the organisation/domain
                - This column is optional
                - A list of role names separated by |. i.e  Admin|GlobalAdmin|...
                - The role should belong to the user for the organisation or domain
                - All global roles are ignored
            - **5th column**: sets the organisation/domain as the default organisation/domain for the users.
                - This is optional, the values can be true or false.
            - **6th column**: The system type - Specifies the system the users belong to. values: 'build' or 'ensure'
        """

        upload_file = {"files": open(file_url, "rb")}

        path_params: Dict[str, Any] = {}
        resp = await self.post(
            "/bulk-users-import-requests/", upload_file=upload_file, params=path_params
        )

        resp_model = str(resp.json())  # type: ignore
        return resp_model

    async def get_bulk_users_import_request(
        self,
        bulk_users_import_request_id: str,
    ) -> members_schemas.BulkUsersImportRequest:
        """ """

        path_params: Dict[str, Any] = {
            "bulk_users_import_request_id": bulk_users_import_request_id,
        }
        resp = await self.get(
            f"/bulk-users-import-requests/{bulk_users_import_request_id}",
            params=path_params,
        )

        try:
            resp_model = members_schemas.BulkUsersImportRequest.model_validate(
                resp.json()
            )
        except pydantic_core.ValidationError:
            raise EnsureException(
                f"The response came back in an unexpected format: {resp.text}"
            )
        return resp_model

    async def update_organisation_user_account_roles(
        self,
        organisation_name: str,
        user_account_id: str,
        updateidentityrolesinput: members_schemas.UpdateIdentityRolesInput,
    ) -> str:
        """ """

        path_params: Dict[str, Any] = {
            "organisation_name": organisation_name,
            "user_account_id": user_account_id,
        }
        resp = await self.put(
            f"/organisations/{organisation_name}/users/{user_account_id}/roles/",
            data=str(updateidentityrolesinput)
            if not issubclass(type(updateidentityrolesinput), BaseModel)
            else updateidentityrolesinput.model_dump_json(),  # type: ignore
            params=path_params,
        )

        resp_model = str(resp.json())  # type: ignore
        return resp_model

    async def add_organisation_user_account_roles(
        self,
        organisation_name: str,
        user_account_id: str,
        addidentityrolesinput: members_schemas.AddIdentityRolesInput,
    ) -> str:
        """ """

        path_params: Dict[str, Any] = {
            "organisation_name": organisation_name,
            "user_account_id": user_account_id,
        }
        resp = await self.post(
            f"/organisations/{organisation_name}/users/{user_account_id}/roles/add/",
            data=str(addidentityrolesinput)
            if not issubclass(type(addidentityrolesinput), BaseModel)
            else addidentityrolesinput.model_dump_json(),  # type: ignore
            params=path_params,
        )

        resp_model = str(resp.json())  # type: ignore
        return resp_model

    async def remove_organisation_user_account_roles(
        self,
        organisation_name: str,
        user_account_id: str,
    ) -> str:
        """ """

        path_params: Dict[str, Any] = {
            "organisation_name": organisation_name,
            "user_account_id": user_account_id,
        }
        resp = await self.delete(
            f"/organisations/{organisation_name}/users/{user_account_id}/roles/remove/",
            params=path_params,
        )

        resp_model = str(resp.json())  # type: ignore
        return resp_model

    async def get_organisation_users(
        self,
        query_arguments: members_queries.GetOrganisationUsersQuery,
        organisation_name: str,
    ) -> members_schemas.PageUserAccountWithoutOrganisations:
        """ """

        # get rid of items where None
        query_params = {
            k: v for k, v in asdict(query_arguments).items() if v is not None
        }

        path_params: Dict[str, Any] = {
            "organisation_name": organisation_name,
        }
        resp = await self.get(
            f"/organisations/{organisation_name}/users/",
            params=path_params | query_params,
        )

        try:
            resp_model = (
                members_schemas.PageUserAccountWithoutOrganisations.model_validate(
                    resp.json()
                )
            )
        except pydantic_core.ValidationError:
            raise EnsureException(
                f"The response came back in an unexpected format: {resp.text}"
            )
        return resp_model

    async def admin_add_user_to_org_domain(
        self,
        organisation_name: str,
        adminaddusertoorgdomain: members_schemas.AdminAddUserToOrgDomain,
    ) -> str:
        """
                ## Adds a user to an organisation or domain with the roles specified
        An admin endpoint to add a new or existing user to an org/domain, bypassing the invite process. A user can be
        added to sub organisations of a domain at the same time with the respective roles.

        Args:
        - `organisation name`: Name of the organisation/domain


         For an organisation or domain for existing user
        ```
           {
              "system_type": "build or ensure",
              "to_email": "email_of_user@scaas.py",
              "role_ids": ["f4e41abf-09ef-43f7-94c0-33ba51238828", "a4e41abf-09ef-43f7-94c0-33ba51238827"],
              "role_names": ["_Admin", "_OtherRole"],
              "is_default_org": True,
            }
        ```
         For an organisation or domain for existing user
        ```
           {
              "system_type": "build or ensure",
              "to_email": "email_of_user@scaas.py",
              "role_ids": ["f4e41abf-09ef-43f7-94c0-33ba51238828", "a4e41abf-09ef-43f7-94c0-33ba51238827"],
              "role_names": ["_Admin", "_OtherRole"],
              "user_info": {
                 "first_name": "user first name",
                 "last_name": "user last name"
               },
              "is_default_org": true
            }
        ```
        For a domain with sub organisations
        ```
           {
          "system_type": "build or ensure",
          "to_email": "email_of_user@scaas.py",
          "role_ids": ["f4e41abf-09ef-43f7-94c0-33ba51238828", "a4e41abf-09ef-43f7-94c0-33ba51238827"],
          "role_names": ["_Admin", "_OtherRole"],
          "sub_organisations": [
              {
                "organisation_name": "Name of the organisation  that belongs to the domain",
                "role_ids": ["list of role ids to assign to the user for the organisation"],
                "role_names": ["list of role names to assign to the user for the organisation"]
              },
             ]
          "user_info": {
             "first_name": "user first name",
             "last_name": "user last name"
           },
          "is_default_org": true
         }
        ```

        Returns:
           - id -UUID of the user.
        """

        path_params: Dict[str, Any] = {
            "organisation_name": organisation_name,
        }
        resp = await self.post(
            f"/organisations/{organisation_name}/users/",
            data=str(adminaddusertoorgdomain)
            if not issubclass(type(adminaddusertoorgdomain), BaseModel)
            else adminaddusertoorgdomain.model_dump_json(),  # type: ignore
            params=path_params,
        )

        resp_model = str(resp.json())  # type: ignore
        return resp_model

    async def get_organisation_user(
        self,
        user_account_id: str,
        organisation_name: str,
    ) -> members_schemas.OrgScopedUserAccount:
        """ """

        path_params: Dict[str, Any] = {
            "user_account_id": user_account_id,
            "organisation_name": organisation_name,
        }
        resp = await self.get(
            f"/organisations/{organisation_name}/users/{user_account_id}",
            params=path_params,
        )

        try:
            resp_model = members_schemas.OrgScopedUserAccount.model_validate(
                resp.json()
            )
        except pydantic_core.ValidationError:
            raise EnsureException(
                f"The response came back in an unexpected format: {resp.text}"
            )
        return resp_model

    async def get_user_invites(
        self,
        query_arguments: members_queries.GetUserInvitesQuery,
    ) -> members_schemas.PageInvite:
        """ """

        # get rid of items where None
        query_params = {
            k: v for k, v in asdict(query_arguments).items() if v is not None
        }

        path_params: Dict[str, Any] = {}
        resp = await self.get("/invites/", params=path_params | query_params)

        try:
            resp_model = members_schemas.PageInvite.model_validate(resp.json())
        except pydantic_core.ValidationError:
            raise EnsureException(
                f"The response came back in an unexpected format: {resp.text}"
            )
        return resp_model

    async def get_invite_info(
        self,
        invite_id: str,
    ) -> members_schemas.InviteInfo:
        """ """

        path_params: Dict[str, Any] = {
            "invite_id": invite_id,
        }
        resp = await self.get(f"/invites/{invite_id}", params=path_params)

        try:
            resp_model = members_schemas.InviteInfo.model_validate(resp.json())
        except pydantic_core.ValidationError:
            raise EnsureException(
                f"The response came back in an unexpected format: {resp.text}"
            )
        return resp_model

    async def get_organisation_invites(
        self,
        query_arguments: members_queries.GetOrganisationInvitesQuery,
        organisation_name: str,
    ) -> members_schemas.PageInvite:
        """ """

        # get rid of items where None
        query_params = {
            k: v for k, v in asdict(query_arguments).items() if v is not None
        }

        path_params: Dict[str, Any] = {
            "organisation_name": organisation_name,
        }
        resp = await self.get(
            f"/organisations/{organisation_name}/invites/",
            params=path_params | query_params,
        )

        try:
            resp_model = members_schemas.PageInvite.model_validate(resp.json())
        except pydantic_core.ValidationError:
            raise EnsureException(
                f"The response came back in an unexpected format: {resp.text}"
            )
        return resp_model

    async def create_organisation_invite(
        self,
        organisation_name: str,
        createbulkinviteinput: members_schemas.CreateBulkInviteInput,
    ) -> list:
        """
                ## Creates organisation invites
         This endpoint creates the invites for an organisation/domain. Multiple invites can be sent to multiple users at
         the same time. While inviting a user to an organisation/domain, the roles the user should be assigned can also be
         specified. If no roles are specified, then the _default role will be assigned.
         This endpoint can also be used to invite a user(s) to a domain and it's organisations that belong to the domain
         at the same time with its respective roles.


         Args:
         - `organisation name`: Name of the organisation/domain


         Example:
         Body Payload:
         - **system_type**: Specifies if the system the user is created for, used for UI and themes
         - **invites**: List of invites to create
             - **to_email**: Email of the user to invite.
             - **role_ids**: Ids of roles to assign to user for an organisation/domain.
             - **role_names**: Names of roles to assign to user for an organisation/domain.
             - **sub_organisations**: List of organisations of the domain to automatically invite along with domain.
                 - **organisation_name**: Name of organisation that already belongs to the domain.
                 - **role_ids**: Ids of roles to assign to user for an organisation.
                 - **role_names**: Names of roles to assign to user for an organisation.

         For an organisation or domain
         ```
        {
           "system_type": "build or ensure",
           "invites": [
                 {
                   "to_email": "email_of_user@scaas.py",
                   "role_ids": ["f4e41abf-09ef-43f7-94c0-33ba51238828", "a4e41abf-09ef-43f7-94c0-33ba51238827"],
                   "role_names": ["_Admin", "_OtherRole"],

                 },
                 {
                   "to_email": "email_of_user2@scaas.py",
                 },
             ]
         }
         ```
         For a domain with sub organisations
         ```
         {
           "system_type": "build or ensure",
           "invites": [
                 {
                   "to_email": "email_of_user@scaas.py",
                   "role_ids": ["f4e41abf-09ef-43f7-94c0-33ba51238828", "a4e41abf-09ef-43f7-94c0-33ba51238827"],
                   "role_names": ["_Admin", "_OtherDomainRole"],
                   "sub_organisations": [
                       {
                             organisation_name: "Name of the organisation  that belongs to the domain",
                             role_ids = ["b4e41abf-09ef-43f7-94c0-33ba51238827"],
                             role_names: ["OrgRole1", "OrgRole2"]
                       }
                   ]
                 }
             ]
         }
         ```

         Returns:
         - List of ids (UUIDs) of the newly created invites.
        """

        path_params: Dict[str, Any] = {
            "organisation_name": organisation_name,
        }
        resp = await self.post(
            f"/organisations/{organisation_name}/invites/",
            data=str(createbulkinviteinput)
            if not issubclass(type(createbulkinviteinput), BaseModel)
            else createbulkinviteinput.model_dump_json(),  # type: ignore
            params=path_params,
        )

        resp_model = list(resp.json())  # type: ignore
        return resp_model

    async def resend_user_invite(
        self,
        invite_id: str,
        organisation_name: str,
    ) -> str:
        """ """

        path_params: Dict[str, Any] = {
            "invite_id": invite_id,
            "organisation_name": organisation_name,
        }
        resp = await self.patch(
            f"/organisations/{organisation_name}/invites/{invite_id}/resend/",
            params=path_params,
        )

        resp_model = str(resp.json())  # type: ignore
        return resp_model

    async def get_organisation_invite(
        self,
        invite_id: str,
        organisation_name: str,
    ) -> members_schemas.Invite:
        """ """

        path_params: Dict[str, Any] = {
            "invite_id": invite_id,
            "organisation_name": organisation_name,
        }
        resp = await self.get(
            f"/organisations/{organisation_name}/invites/{invite_id}",
            params=path_params,
        )

        try:
            resp_model = members_schemas.Invite.model_validate(resp.json())
        except pydantic_core.ValidationError:
            raise EnsureException(
                f"The response came back in an unexpected format: {resp.text}"
            )
        return resp_model

    async def revoke_organisation_invite(
        self,
        invite_id: str,
        organisation_name: str,
    ) -> None:
        """ """

        path_params: Dict[str, Any] = {
            "invite_id": invite_id,
            "organisation_name": organisation_name,
        }
        await self.delete(
            f"/organisations/{organisation_name}/invites/{invite_id}",
            params=path_params,
        )

        return

    async def accept_invite_for_existing_user(
        self,
        invite_id: str,
    ) -> str:
        """ """

        path_params: Dict[str, Any] = {
            "invite_id": invite_id,
        }
        resp = await self.put(
            f"/invites/{invite_id}/accept-existing/", params=path_params
        )

        resp_model = str(resp.json())  # type: ignore
        return resp_model

    async def accept_new_user_invite(
        self,
        invite_id: str,
        userinputbase: members_schemas.UserInputBase,
    ) -> str:
        """ """

        path_params: Dict[str, Any] = {
            "invite_id": invite_id,
        }
        resp = await self.put(
            f"/invites/{invite_id}/accept-new/",
            data=str(userinputbase)
            if not issubclass(type(userinputbase), BaseModel)
            else userinputbase.model_dump_json(),  # type: ignore
            params=path_params,
        )

        resp_model = str(resp.json())  # type: ignore
        return resp_model

    async def get_version(
        self,
    ) -> members_schemas.Version:
        """ """

        path_params: Dict[str, Any] = {}
        resp = await self.get("/version/", params=path_params)

        try:
            resp_model = members_schemas.Version.model_validate(resp.json())
        except pydantic_core.ValidationError:
            raise EnsureException(
                f"The response came back in an unexpected format: {resp.text}"
            )
        return resp_model
