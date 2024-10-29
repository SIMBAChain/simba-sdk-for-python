from typing import IO, Any, Callable, Optional, Union

import simba_sdk.core.requests.client.credential.queries as credential_queries
import simba_sdk.core.requests.client.credential.schemas as credential_schemas
import simba_sdk.core.requests.client.members.queries as members_queries
import simba_sdk.core.requests.client.members.schemas as members_schemas
import simba_sdk.core.requests.client.resource.queries as resource_queries
import simba_sdk.core.requests.client.resource.schemas as resource_schemas
from simba_sdk import config
from simba_sdk.config import settings
from simba_sdk.core.requests.auth.token_store import InMemoryTokenStore
from simba_sdk.core.requests.client.credential.client import CredentialClient
from simba_sdk.core.requests.client.members.client import MembersClient
from simba_sdk.core.requests.client.resource.client import ResourceClient
from simba_sdk.core.requests.exception import EnsureException, RequestException


def authorised(method: Callable) -> Callable:
    async def auth_and_call(self, *args: int, **kwargs: str) -> Any:
        await self.authorise()
        return await method(self, *args, **kwargs)

    return auth_and_call


class EnsureClient:
    def __init__(self) -> None:
        self._authorised = False
        # api profile
        self._user: Optional[members_schemas.UserAccount] = None
        self._domain: Optional[members_schemas.Domain] = None
        self._account: Optional[credential_schemas.BlocksAccount] = None

        self._token_store = InMemoryTokenStore()
        # build middleware
        self._middleware = []
        for middleware in config.MIDDLEWARE.values():
            self._middleware.append(middleware())
        # build clients
        self.members_client = MembersClient(
            settings.MEMBERS_URL, token_store=self._token_store
        )
        self.credential_client = CredentialClient(
            settings.CREDENTIAL_URL, token_store=self._token_store
        )
        self.resource_client = ResourceClient(
            settings.RESOURCE_URL, token_store=self._token_store
        )

    async def authorise(self) -> None:
        try:
            if not self._authorised or self._token_store.is_expired_token(
                settings.CLIENT_ID
            ):
                await self.members_client.authorise()
                self._authorised = True
        except RequestException as ex:
            raise RequestException(
                ex.status_code,
                f"Couldn't authorise client, please check your client credentials (in config.py) are correct. {ex}",
            )

        if type(self._user) is not members_schemas.UserAccount:
            self._user = await self.members_client.whoami()

    @property
    def user(self) -> members_schemas.UserAccount:
        if type(self._user) is not members_schemas.UserAccount:
            raise EnsureException(
                "The user profile is not available until you authorise, to do so please call `EnsureClient.authorise`."
            )
        return self._user

    @user.setter
    def user(self, _: Any) -> None:
        raise EnsureException(
            message="Your user profile is determined by the client credentials in config.py, to change accounts please update these credentials."
        )

    @authorised
    async def set_domain(self, domain_name: str) -> members_schemas.Domain:
        if isinstance(domain_name, str):
            domains = await self.members_client.get_domains(
                members_queries.GetDomainsQuery(
                    page=1, size=1, name=domain_name, user__id=self.user.id
                )
            )

            if len(domains.items) == 0:
                raise EnsureException(
                    "You are not currently a member of any domains on this environment."
                )
            self._domain = domains.items[0]
        return self._domain

    @property
    def domain(self) -> members_schemas.Domain:
        if type(self._domain) is not members_schemas.Domain:
            raise EnsureException(
                "Your domain information hasn't been validated, please do so via `EnsureClient.set_domain`."
            )
        return self._domain

    @domain.setter
    def domain(self, _: Any) -> None:
        raise EnsureException(
            "Please use `EnsureClient.set_domain` to set your domain."
        )

    @authorised
    async def set_account(self, network: str, alias: str) -> None:
        query_obj = credential_queries.ListCustodialAccountsQuery(
            page=1, size=1, domain=self.domain.name
        )
        accounts_response = await self.credential_client.list_custodial_accounts(
            query_arguments=query_obj
        )
        for account in accounts_response.results:
            if account.network == network and account.alias == alias:
                self._account = account
                return
        else:
            raise EnsureException(
                "Could not find an account matching these fields on the Credential Service."
            )

    @authorised
    async def get_default_account(self) -> credential_schemas.BlocksAccount:
        query_obj = credential_queries.ListCustodialAccountsQuery(
            page=1, size=1, domain=self.domain.name
        )
        accounts_response = await self.credential_client.list_custodial_accounts(
            query_arguments=query_obj
        )
        accounts = accounts_response.results
        if len(accounts_response.results) == 0:
            raise EnsureException(
                "You do not currently have any accounts on this environment."
            )
        default_account = sorted(accounts, key=lambda x: x.created_on)[0]
        return default_account

    @property
    def account(self) -> credential_schemas.BlocksAccount:
        if type(self._account) is not credential_schemas.BlocksAccount:
            raise EnsureException(
                "An account has not been set, please set one via `EnsureClient.set_account`."
            )
        return self._account

    @authorised
    async def create_bundle(
        self,
        createresourcebundlerequest: resource_schemas.CreateResourceBundleRequest,
    ) -> resource_schemas.ResourceBundle:
        """ """
        resp = await self.resource_client.create_bundle(
            domain_name=self.domain.name,
            createresourcebundlerequest=createresourcebundlerequest,
        )
        return resp

    @authorised
    async def get_bundle(
        self,
        uid: str,
    ) -> resource_schemas.ResourceBundle:
        """
        Gets a bundle by its database UUID
        """
        resp = await self.resource_client.get_bundle(
            uid=uid,
            domain_name=self.domain.name,
        )
        return resp

    @authorised
    async def add_policy(
        self,
        uid: str,
        policy: resource_schemas.Policy,
    ) -> resource_schemas.Policy:
        """ """
        resp = await self.resource_client.add_policy(
            uid=uid,
            domain_name=self.domain.name,
            policy=policy,
        )
        return resp

    @authorised
    async def upload_files(
        self,
        file_url: str,
        uid: str,
    ) -> resource_schemas.BundleTask:
        """ """
        resp = await self.resource_client.upload_files(
            uid=uid, domain_name=self.domain.name, file_url=file_url
        )
        return resp

    @authorised
    async def resource_get_task(
        self,
        uid: str,
        task_id: str,
    ) -> resource_schemas.BundleTask:
        """ """
        resp = await self.resource_client.get_task(
            uid=uid,
            task_id=task_id,
            domain_name=self.domain.name,
        )
        return resp

    @authorised
    async def publish_action(
        self,
        uid: str,
        publicationrequest: resource_schemas.PublicationRequest,
    ) -> resource_schemas.BundleTask:
        """ """
        resp = await self.resource_client.publish_action(
            uid=uid,
            domain_name=self.domain.name,
            publicationrequest=publicationrequest,
        )
        return resp

    @authorised
    async def get_storages(
        self,
        query_arguments: resource_queries.GetStoragesQuery,
    ) -> resource_schemas.PageStorageView:
        """ """
        resp = await self.resource_client.get_storages(
            domain_name=self.domain.name,
            query_arguments=query_arguments,
        )
        return resp

    @authorised
    async def request_access(
        self,
        resource_id: str,
        body: Union[resource_schemas.Presentation, None],
    ) -> resource_schemas.ResourceToken:
        """
                    Returns a token that can be used to retrieve a bundle.
        The token may take a little time to become active.
        """
        resp = await self.resource_client.request_access(
            resource_id=resource_id,
            body=body,
        )
        return resp

    @authorised
    async def get_access(
        self,
        output_stream: IO,
        token: str,
    ) -> None:
        """ """
        resp = await self.resource_client.get_access(
            token=token,
        )
        output_stream.write(resp)

    @authorised
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
        resp = await self.members_client.admin_add_user_to_org_domain(
            organisation_name=organisation_name,
            adminaddusertoorgdomain=adminaddusertoorgdomain,
        )
        return resp

    @authorised
    async def create_custodial_account(
        self,
        createaccounthttp: credential_schemas.CreateAccountHttp,
    ) -> credential_schemas.BlocksAccount:
        """
                    ## Create a SIMBA Blocks account owned by the logged-in is user.
        The `domain` and optional `trust_profile` are used to identify the blockchain on which the account will be created.

        Args:
        - `domain`: Domain name to be used to look up the blockchain.

        - `trust_profile`: Optional TrustProfile name to be used to look up the blockchain..

        - `nickname`: A name for your new account.

        - `alias`: Optional, an alternate name by which this account will be known.


        Example:

        ```
        {
          "domain": "dog_domain",
          "nickname": "Cred-Svc-Wallet"
          "alias": "george-wallet-alias",
        }
        ```

        Returns:
        - `models.BlocksAccount`: A blocks account object.
        """
        resp = await self.credential_client.create_custodial_account(
            createaccounthttp=createaccounthttp,
        )
        return resp

    @authorised
    async def list_trust_profiles(
        self,
        query_arguments: credential_queries.ListTrustProfilesQuery,
    ) -> credential_schemas.PageTrustProfile:
        """
                    ## List TrustProfiles
        This endpoint retrieves a list of TrustProfiles scoped by Domain.

        Args:
        - `domain`: The Domain name.

        - `trustprofile_filter`: Filtering parameters, encapsulated by the TrustProfileFilter.

        Returns:
        - `Page[models.TrustProfile]`: A page of TrustProfile objects defined for the specified Domain.

        ### Filters:
        For a detailed description and usage examples of the `TrustProfileFilter` parameters, please refer to the
        `TrustProfileFilter` model defined in the OpenAPI schema section of this documentation.


        - `__ilike`: Used for case-insensitive pattern matching. For example, `alias__ilike` would be used to search for
        aliases that match a specified pattern, ignoring case.

        - `__in`: Used to filter data that matches any value in a provided list. For example, `tags__in` filters for records
        where the tags attribute matches any value in the given list.

        - `__lte`: "less than or equal to". For example, `created_at__lte` would filter for records created at or before a
        specified date.

        - `__gte`: "greater than or equal to". For example, `created_at__gte` would filter for records created at or after a
        specified date.
        """
        resp = await self.credential_client.list_trust_profiles(
            domain_name=self.domain.name,
            query_arguments=query_arguments,
        )
        return resp

    @authorised
    async def get_schema_registry(
        self,
    ) -> credential_schemas.DomainRegistry:
        """
                    Get the claim schema registry for a particular domain.

        Args:
        - `domain`: the name of the domain

        - `schema_reg`: injected dependency

        Returns: `DomainRegistry`
        """
        resp = await self.credential_client.get_schema_registry(
            domain_name=self.domain.name,
        )
        return resp

    @authorised
    async def list_dids(
        self,
        query_arguments: credential_queries.ListDidsQuery,
    ) -> credential_schemas.PageDIDResponseModel:
        """
                    ## List DIDs

        Args:
        - `request`: The request object.

        - `domain`: You can scope the request by domain.

        - `simba_id`: List the DIDs of a specific user. Can be used to see your own DIDs.

        - `output_format`: "SIMPLE" | "DETAILED".

        - `include_stats`: bool, True=show usage counts, False (default).

        - `diddoc_filter`: Filtering parameters, encapsulated by the DIDFilter.

        Returns:
        - `Page[models.DID]`: A page of DID objects that belong to the current user.

        ### Filters:
        For a detailed description and usage examples of the `DIDFilter` parameters, please refer to the `DIDFilter` model
        defined in the OpenAPI schema section of this documentation.

        - `__search`: Used for case-insensitive pattern matching on multiple fields using an `OR` clause. For `DID.metadata`
        the search fields are:

            - `["nickname", "public_name", "tags", "permission", "trust_profile"]`.

            - Note: Specifying `metadata__nickname__ilike` restricts the query to the owners DIDs only.


        - `__ilike`: Used for case-insensitive pattern matching. For example, `alias__ilike` would be used to search for
        aliases that match a specified pattern, ignoring case.

        - `__in`: Used to filter data that matches any value in a provided list. For example, `tags__in` filters for records
        where the tags attribute matches any value in the given list.

        - `__lte`: "less than or equal to". For example, `created_at__lte` would filter for records created at or before a
        specified date.

        - `__gte`: "greater than or equal to". For example, `created_at__gte` would filter for records created at or after a
        specified date.

        - `order_by`: a list of prefixed attributes on which to sort, for example  `metadata.created_at, metadata.name`
        """
        resp = await self.credential_client.list_dids(
            domain_name=self.domain.name,
            query_arguments=query_arguments,
        )
        return resp

    @authorised
    async def create_did(
        self,
        createdidhttp: credential_schemas.CreateDidHttp,
    ) -> str:
        """
                    ## Create DID
        This endpoint creates a `DID` for the logged-in user. See `DID` in the OpenAPI schema section of this
        documentation.

        Args:
        - `domain`: Domain name where the TrustProfile is to be created.

        - `did_http`: The input model `CreateDidHttp`

        Returns:
        - `DocumentId`: The MongoDB ObjectID of the newly created Document.<br><br>


        ### CreateDIDHttp detail:
        - **trust_profile**: TrustProfile name, determines the type of DID created and controls subsequent DID operations on
        DIDS, VCs and VPs. Available types: SMB1-STD, SMB1-NFT
          - Example: `"SMB1-STD"`

        - **account**: PubKeyAccountInfo object containing `public_key`, `alias` and `org` (optional). `org` should be defined for an org scoped account.

          - The `alias` field, if omitted, will create a client-side-signing DID. if `alias` is defined, then a server-side-signing DID is created

          - Example of input for server-side-signing DID:
            ```
            {
              "public_key": "0xd4039eB67CBB36429Ad9DD30187B94f6A5122215",
              "alias": "george-wallet-alias"
            }
            ```

          - Example of input for client-side-signing DID:
            ```
            {
              "public_key": "0xd4039eB67CBB36429Ad9DD30187B94f6A5122215",
            }
            ```

        - **permission**: Defines the DID's capabilities. An ISSUER DID can be used to create VCs. A HOLDER DID can be used as the credentialSubject in a VC.
          - Example: `"HOLDER" | "ISSUER"`

        - **alias**: Allows a user to own multiple DIDs within the same Domain. The _**alias**_ of a _**DID**_ owned by the logged in user.
          - Example: `"joe@bloggs.com" | "my-work-did"`

        - **nickname**:  Owner's familiar DID name. Must be case-insensitive unique for this user.
          - Example: `"Molly dog cert"`

        - **public_name**: The public name of the entity represented by this DID. Must be case-insensitive unique for this user.
          - Example: `"Certificate of Pedigree""`

        - **seed**: A user-defined seed to enhance DID uniqueness. Allows multiple DIDs per user+alias within this domain. Could be a document ID or part-number.
          - Example: `document_id | part-number`

        - **tags** (Optional): Keywords for easy searching or identification of the DID.
          - Example: `["dog", "cat"]`

        - **did_doc_creation_params**: Optional for GitHub DIDs and not required for creating an SMB1 DID with the STD
        registry, unless specifying a controller. Required for all other DID methods and registry smart contract combinations.
          - Note: A **controller** refers to an existing **DID.id** that authorizes changes to this new DID/DIDDocument.


        See examples below:
          - Examples:

            ### Optional GitHub did_doc_creation_params

            ```
            {
                "controller": "did:web:SIMBAChain.github.io:context:diddoc:5fb976f5697fe769a054f516377491c1eadd0f3e51bb58f26990035afa474465",
                "aka": "did is also known as",
                "key_name": "public key name to use. Default = #1"
            }
            ```

            ### Optional SMB1-STD did_doc_creation_params

            ```
            {
                "controller": "did:smb1:1337:0xfc98c982ca22ea0141c3452325c372ff728e9ccd:39517405560208510513658073967297468008711112795722749167466577185994559263742"
            }
            ```

            ### Required SMB1-NFT DID did_doc_creation_params
            ```
            {
                "collection": "0x2e3e124bc2Cc43Bc3A8FA8D87322057eD3bB4a5f",
                "token_id": 1234
            }
            ```

            ### Required SMB1-MSC Multi-sig  did_doc_creation_params

            ```
            {
                "signers": [
                    "0xd4039eB67CBB36429Ad9DD30187B94f6A5122215",
                    "0x7633Fe8542c2218B5A25777477F63D395aA5aFB4",
                    "0xd5cC383881D6d9A7dc1891A0235E11D03Cb992d3"
                ],
                "threshold": 2
            }
            ```

        ## Full payload examples
        Below are full payload examples. You must set the following fields (see above descriptions of the fields):

        - `"trust_profile":` ...

        - `"account.public_key":` ...

        - `"account.alias":` ...

        - `"alias":` ...

        - `"seed:` ...

            - Update or delete `tags`.

        ### Example GitHub DID
        ```
        {
          "trust_profile": "SIMBAWEB",
          "account": {
            "alias": "george-wallet-alias",
            "public_key": "0xd9dE3dC135f5264Ff159B662442dd8A589AC6040"
          },
          "permission": "ISSUER",
          "alias": "emloyee.123@simbachain.com",
          "nickname": "Me",
          "public_name": "Head HR Simbachain",
          "seed": "fwoipxcnmw",
          "tags": [
            "HR", "operations", "planning"
          ]
        }
        ```

        ### Example SMB1 Standard DID
        ```
        {
          "trust_profile": "SMB1-STD",
          "account": {
            "alias": "george-wallet-alias",
            "public_key": "0xd9dE3dC135f5264Ff159B662442dd8A589AC6040"
          },
          "permission": "ISSUER",
          "alias": "emloyee.123@simbachain.com",
          "nickname": "Me",
          "public_name": "Head HR Simbachain",
          "seed": "fwoipxcnmw",
          "tags": [
            "HR", "operations", "planning"
          ]
        }
        ```

        ### Example SMB1-NFT Standard DID
        ```
        {
          "trust_profile": "SMB1-NFT",
          "account": {
            "alias": "george-wallet-alias",
            "public_key": "0xd9dE3dC135f5264Ff159B662442dd8A589AC6040"
          },
          "permission": "HOLDER",
          "alias": "emloyee.123@simbachain.com",
          "nickname": "ops work",
          "public_name": "Operations Plan",
          "seed": "doc#678921456",
          "tags": [
            "Work", "operations", "planning"
          ]
          "did_doc_creation_params": {
            "collection": "0x2e3e124bc2Cc43Bc3A8FA8D87322057eD3bB4a5f",
            "token_id": 1234
          }
        }
        ```

        ### Example SMB1-MSC DID
        ```
        {
          "trust_profile": "SMB1-MSC",
          "account": {
            "alias": "george-wallet-alias",
            "public_key": "0xd9dE3dC135f5264Ff159B662442dd8A589AC6040"
          },
          "permission": "HOLDER",
          "alias": "emloyee.123@simbachain.com",
          "nickname": "ops work",
          "public_name": "Operations Plan",
          "seed": "doc#678921456",
          "tags": [
            "Work", "operations", "planning"
          ]
          "did_doc_creation_params": {
              "signers": [
                  "0xd4039eB67CBB36429Ad9DD30187B94f6A5122215",
                  "0x7633Fe8542c2218B5A25777477F63D395aA5aFB4",
                  "0xd5cC383881D6d9A7dc1891A0235E11D03Cb992d3"
              ],
              "threshold": 2
          }
        }
        ```
        """
        resp = await self.credential_client.create_did(
            domain_name=self.domain.name,
            createdidhttp=createdidhttp,
        )
        return resp

    @authorised
    async def get_did(
        self,
        did_id: str,
    ) -> credential_schemas.DID:
        """
                    ## GET DID

        Args:
        - `did_id`: The MongoDB ObjectID or the `id` string of the DIDDocument (did_document.id).

        - `domain`: Name of the `Domain` where the `DID` is located.

        Returns:
        - A `DID` model, see the OpenAPI schema section of this documentation.
        """
        resp = await self.credential_client.get_did(
            did_id=did_id,
            domain_name=self.domain.name,
        )
        return resp

    @authorised
    async def create_vc(
        self,
        createvchttp: credential_schemas.CreateVCHttp,
    ) -> str:
        """
                    ## Create VC

        To create a VC requires two DIDs. Both DIDs must be valid published DIDs. Optional start and end dates can be
        supplied. Parameters that control proof generation must also be supplied.

        Args:

        - `domain`: The Domain name where the `VC` will be created.

        - `vc_http_input`:  The input model `CreateVCHttp`

            - `issuer`: The issuer DID-string ID.

            - `subject`: The `credentialSubject` DID-string ID.

            - `valid_from`: Date-time from which this VC is valid.

            - `valid_until`: Expiry date-time of this VC.

            - `material`: Proof challenge inputs, used to add the proof to the VC:

            - `claims`: is dictionary of `property: values` that represent individual claims about the `credentialSubject`.

        Returns:
        - `DocumentId`: The MongoDB ObjectID of the newly created Document.<br><br>

        ### CreateVCHttp detail:

        This method creates an empty VC that can be subsequently used to create a CredentialSubject followed by adding Claims to this CredentialSubject. Finally the add_proof endpoint should be called to sign the VC.

        - **tags (Optional)**:

          - Description: A list of _**tags**_ attached to the _**VC**_.

          - Example: `<Drivers License>`

        - **issuer**:

          - Description: The **DID** representing the issuing authority for this VC (requires DID.permssion==ISSUER).

          - Example: `did:smb1:1337:0xea0fc982ca22ea0141c3452325c372ff728e9ccd:18322500091651578819492444870201097984271428616569706638674662898632050307001`

        - **subject**:

          - Description: The **DID** representing the entity to which the VC applies (the credentialSubject).

          - Example: `did:smb1:1337:0xfc98c982ca22ea0141c3452325c372ff728e9ccd:18322500091651578819492444870201097984271428616569706638674662898632050307982`

        - **valid_from  (Optional)**:

          - Starting date-time that the VC becomes in force.

          - Example: `<2010-06-15T21:24:10.768473>`

        - **valid_until  (Optional)**:

          - Date-time that the VC will become invalid.

          - Example: `<2050-06-15T21:24:10.768473>`

        - **materials**:

          - Proof challenge inputs, used to add the proof to the VC

          - Example: `{"circom_circuit": "SMTInclusionSingleClaim"}`

        - **claims**: The claims being made about the `credentialSubject`.
            ```
            "claims": {
                "https://www.w3.org/2018/credentials/examples/v1": {
                    "degree": {
                        "type": "BachelorDegree",
                        "name": "Bachelor of Science and Arts"
                    }
                }
            }
            ```
            In the example,

            - `"representative"`: is the `claim_schema` property.

            - `"value"`: This can be a `bool`, `int`, `str`, or `dict` based on the *claim_schema* definition.

            - `"claim_schema"`:Is the IRI schema link identifying the schema for the specified claim.

        ## Full payload example
        Below is a full payload example. You must set the following fields (see above for descriptions):

        - `"issuer:` ...

        - `"subject":` ...

            - Update or delete `tags`, `validFrom`, `validUntil`.

            - The `claims` entered must be from a known schema.

                - If `claim_schema` is `null`, the `credential-service`looks for a schema in its known contexts.


        ### Example 1:

                {
                    "tags": ["degree", "bsc"],
                    "@context": ["https://www.w3.org/2018/credentials/v1"],
                    "issuer": "did:smb1:1337:0xfc98c982ca22ea0141c3452325c372ff728e9ccd:39517405560208510513658073967297468008711112795722749167466577185994559263742",
                    "valid_from": "2024-03-08T01:37:35.899Z",
                    "valid_until": "2026-03-08T01:37:35.899Z",
                    "type": ["VerifiableCredential"],
                    "material": {"circom_circuit": "SMTInclusionSingleClaim"},
                    "subject": "did:smb1:1337:0xfc98c982ca22ea0141c3452325c372ff728e9ccd:39517405560208510513658073967297468008711112795722749167466577185994559263742",
                    "claims": {
                        "https://www.w3.org/2018/credentials/examples/v1": {
                            "degree": {
                                "type": "BachelorDegree",
                                "name": "Bachelor of Science and Arts"
                            }
                        }
                    }
                }

        ### Example 2:

                {
                    "tags": ["dev1", "fred-holder"],
                    "@context": ["https://www.w3.org/2018/credentials/v1"],
                    "issuer": "did:smb1:1337:0xfc98c982ca22ea0141c3452325c372ff728e9ccd:35658973081941150517877546146441453457835196343845723562092740532250386250123",
                    "valid_from": "2024-03-08T01:37:35.899Z",
                    "valid_until": "2026-03-08T01:37:35.899Z",
                    "type": ["VerifiableCredential"],
                    "material": {"circom_circuit": "SMTInclusionSingleClaim"},
                    "subject": "did:smb1:1337:0xfc98c982ca22ea0141c3452325c372ff728e9ccd:78218754147316378273184740864117609881796548893517659643381541228635294090456",
                    "claims": {
                        "https://simbachain.github.io/context/claims/schema/demo/representative.jsonld": {
                            "representative": {"title": "King"}
                        }
                    }
                }
        """
        resp = await self.credential_client.create_vc(
            domain_name=self.domain.name,
            createvchttp=createvchttp,
        )
        return resp

    @authorised
    async def get_vc(
        self,
        vc_id: str,
    ) -> credential_schemas.CredentialServiceDomainModelsVerifiableCredential:
        """
                    ## GET VC

        Args:
        - `vc_id`: The MongoDB ObjectID of the VC.

        - `domain`: Name of the `Domain` where the `VC` is located.

        Returns:
        - A `VC` model, see the OpenAPI schema section of this documentation.
        """
        resp = await self.credential_client.get_vc(
            vc_id=vc_id,
            domain_name=self.domain.name,
        )
        return resp

    @authorised
    async def accept_vc(
        self,
        query_arguments: credential_queries.AcceptVcQuery,
        vc_id: str,
    ) -> str:
        """
                    ## Accept an issued VC

        When a user is issued a VC by another actor, the VC must be accepted before it can be used in a VP.
        The user can also reject the issued VC should they so desire.

        Args:
        - `accept`: If **True**, the vc will be accepted otherwise it is rejected.

        - `vc_id`: The id of the vc being accepted/rejected.

        Returns:
        - `DocumentId`: The MongoDB ObjectID of the updated VC.
        """
        resp = await self.credential_client.accept_vc(
            vc_id=vc_id,
            domain_name=self.domain.name,
            query_arguments=query_arguments,
        )
        return resp

    @authorised
    async def create_vp(
        self,
        createvphttp: credential_schemas.CreateVPHttp,
    ) -> str:
        """
                    ## Create VP

        Create a VP which can be used to present all or part of the logged-in-user's VerifiableCredential
        information in a secure and possibly redacted manner.

        Args:
        - `domain`: The Domain name where the `VP` will be created.

        - `vc_http`:  The input model `CreateVPHttp`

            - `vc_id`: the MongoDB ObjectID of the [VC][credential_service.domain.models.VerifiableCredential] being presented.

            - `proof_type`: `"SMTInclusionProof"`

            - `material`: Proof challenge input dict, used to add the proof to the VP, example,
                ```
                {
                    "challenge": "0x18",
                    "domain": "0x8d242e4bc081e2eeD5eb9d6BF734DdF5d2F435e0",
                    "presentation_time": 1698232514,
                }
                ```

        Returns:
        - `DocumentId`: The MongoDB ObjectID of the newly created Document.<br><br>

        ## Full payload example
        Below is a full payload example.
        - All fields should be set as required (see above descriptions of the fields):

        ```
        {
          "vc_id": "65f2c5d51f2315b03db61234",
          "proof_type": "SMTInclusionProof",
          "material": {
            "challenge": "0x18",
            "domain": "0x8d242e4bc081e2eeD5eb9d6BF734DdF5d2F435e0",
            "presentation_time": 1698232514
            }
        }
        ```
        """
        resp = await self.credential_client.create_vp(
            domain_name=self.domain.name,
            createvphttp=createvphttp,
        )
        return resp

    @authorised
    async def get_vp(
        self,
        vp_id: str,
    ) -> credential_schemas.CredentialServiceDomainModelsVerifiablePresentation:
        """
                    ## GET VP

        Args:
        - `vp_id`: The MongoDB ObjectID of the VP.

        - `domain`: Name of the `Domain` where the `VP` is located.

        Returns:
        - A `VP` model, see the OpenAPI schema section of this documentation.
        """
        resp = await self.credential_client.get_vp(
            vp_id=vp_id,
            domain_name=self.domain.name,
        )
        return resp

    @authorised
    async def credential_get_task(
        self,
        task_id: str,
    ) -> credential_schemas.Task:
        """
                    ## Get a Task created by the logged-in user.

        Args:
        - `task_id`: the mongodb document id returned by `create_did`

        - `x_simba_sub_id`: Optional Member service id (UUID) for the user

        Returns:
        - `Task`: a single task object which corresponds to the `task_id`
        """
        resp = await self.credential_client.get_task(
            task_id=task_id,
            domain_name=self.domain.name,
        )
        return resp

    @authorised
    async def verify_vc(
        self,
        body: object,
    ) -> credential_schemas.VerificationResult:
        """
                    ## Verify VC
        This endpoint can be used to verify the integrity of a VerifiableCredential.

        Args:
        - `vc`: A JSON_LD VerifiableCredential

        Returns:
        - A `VerificationResult` model, see the OpenAPI schema section of this documentation.
        """
        resp = await self.credential_client.verify_vc(
            body=body,
        )
        return resp

    @authorised
    async def verify_vp(
        self,
        body: object,
    ) -> credential_schemas.VerificationResult:
        """
                    ## Verify VP
        This endpoint can be used to verify the integrity of a VerifiablePresentation.

        Args:
        - `vp`: A JSON_LD VerifiablePresentation

        Returns:
        - A `VerificationResult` model, see the OpenAPI schema section of this documentation.
        """
        resp = await self.credential_client.verify_vp(
            body=body,
        )
        return resp
