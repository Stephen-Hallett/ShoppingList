import base64
import hashlib
import hmac
import json
import logging
import os

from azure.core.exceptions import ResourceExistsError
from azure.data.tables import TableServiceClient, UpdateMode

from .schemas import (
    Item,
    ItemCreate,
    ShoppingList,
    ShoppingListCreate,
    ShoppingListUpdate,
    Test,
    User,
    UserCreate,
    UserUpdate,
    EmailRequest,
    ItemName
)
from .util import log

logger = logging.getLogger(__name__)


def make_rowid(primaryKey: str, secret_key: str = os.environ["HASH_KEY"]) -> str:
    message = primaryKey.lower().strip().encode("utf-8")
    key = secret_key.encode("utf-8")

    digest = hmac.new(key, message, hashlib.sha256).digest()
    return base64.urlsafe_b64encode(digest).decode("utf-8").rstrip("=")


class Controller:
    def __init__(self) -> None:
        self.logger = logging.getLogger(__name__)
        self.table_service = TableServiceClient.from_connection_string(
            conn_str=os.environ["TABLE_CONNECTION"]
        )
        self.users_table_client = self.table_service.get_table_client("users")
        self.shoppinglists_table_client = self.table_service.get_table_client("lists")
        self.items_table_client = self.table_service.get_table_client("items")

    @log
    def test(self) -> Test:
        return {"test": "Dw it's working"}

    @log
    def create_user(self, user: UserCreate) -> User:
        row_key = make_rowid(user.email)
        entity = {
            "PartitionKey": "user",
            "RowKey": row_key,
            "email": user.email,
            "name": user.name.strip(),
        }
        try:
            self.users_table_client.create_entity(entity=entity)
            return User(id=row_key, **user.model_dump())
        except ResourceExistsError as e:
            error_message = "A user with the name and email provided already exists."
            raise ResourceExistsError(error_message) from e

    @log
    def get_user(self, user_id: str) -> User:
        entity = self.users_table_client.get_entity(
            partition_key="user", row_key=user_id
        )
        return User(id=entity["RowKey"], email=entity["email"], name=entity["name"])

    @log
    def update_user(self, user_id: str, user: UserUpdate) -> User:
        entity = self.users_table_client.get_entity(
            partition_key="user", row_key=user_id
        )

        if user.name is not None:
            entity["name"] = user.name

        self.users_table_client.update_entity(entity=entity, mode=UpdateMode.REPLACE)
        return User(id=user_id, email=entity["email"], name=entity["name"])

    @log
    def delete_user(self, user_id: str) -> dict:
        self.users_table_client.delete_entity(partition_key="user", row_key=user_id)
        return {"message": f"User {user_id} deleted"}

    @log
    def list_users(self) -> list[User]:
        all_entities = list(self.users_table_client.list_entities())
        for entity in all_entities:
            entity["id"] = entity["RowKey"]
        return [User.model_validate(entity) for entity in all_entities]

    # ShoppingLists db
    @log
    def create_shoppinglist(self, shoppinglist: ShoppingListCreate) -> ShoppingList:
        row_key = make_rowid(f"{shoppinglist.name}_{shoppinglist.owner}")
        entity = {
            "PartitionKey": "shoppinglist",
            "RowKey": row_key,
            "name": shoppinglist.name,
            "owner": shoppinglist.owner,
            "members": json.dumps(shoppinglist.members),
            "items": json.dumps(shoppinglist.items),
        }
        try:
            self.shoppinglists_table_client.create_entity(entity=entity)
            return ShoppingList(id=row_key, **shoppinglist.model_dump())
        except ResourceExistsError as e:
            error_message = "You already have a shopping list with that name."
            raise ResourceExistsError(error_message) from e

    @log
    def get_shoppinglist(self, shoppinglist_id: str) -> ShoppingList:
        entity = self.shoppinglists_table_client.get_entity(
            partition_key="shoppinglist", row_key=shoppinglist_id
        )
        return ShoppingList(
            id=entity["RowKey"],
            name=entity["name"],
            owner=entity["owner"],
            items=json.loads(entity["items"]),
            members=json.loads(entity["members"]),
        )

    @log
    def update_shoppinglist(
        self, shoppinglist_id: str, shoppinglist: ShoppingListUpdate
    ) -> ShoppingList:
        entity = self.shoppinglists_table_client.get_entity(
            partition_key="shoppinglist", row_key=shoppinglist_id
        )

        if shoppinglist.items is not None:
            entity["items"] = json.dumps(shoppinglist.items)
        if shoppinglist.members is not None:
            entity["members"] = json.dumps(shoppinglist.members)

        self.shoppinglists_table_client.update_entity(
            entity=entity, mode=UpdateMode.REPLACE
        )
        return ShoppingList(
            id=shoppinglist_id,
            name=entity["name"],
            owner=entity["owner"],
            items=json.loads(entity["items"]),
            members=json.loads(entity["members"]),
        )

    @log
    def delete_shoppinglist(self, shoppinglist_id: str) -> dict:
        self.shoppinglists_table_client.delete_entity(
            partition_key="shoppinglist", row_key=shoppinglist_id
        )
        return {"message": f"ShoppingList {shoppinglist_id} deleted"}

    @log
    def list_shoppinglists(self, user_id: str) -> list[ShoppingList]:
        all_entities = list(self.shoppinglists_table_client.list_entities())
        for entity in all_entities:
            entity["id"] = entity["RowKey"]
            entity["members"] = json.loads(entity["members"])
            entity["items"] = json.loads(entity["items"])
        return [
            ShoppingList.model_validate(entity)
            for entity in all_entities
            if user_id in [entity["owner"], *entity["members"]]
        ]
    
    def invite_to_shopping(self, shoppinglist_id: str, email: EmailRequest):
        print(email)
        entity = self.shoppinglists_table_client.get_entity(
            partition_key="shoppinglist", row_key=shoppinglist_id
        )
        current_members = json.loads(entity["members"])
        if make_rowid(email.email) not in current_members:
            entity["members"] = json.dumps([*current_members, make_rowid(email.email)])
            self.shoppinglists_table_client.update_entity(
                entity=entity, mode=UpdateMode.REPLACE
            )
        return ShoppingList(
            id=shoppinglist_id,
            name=entity["name"],
            owner=entity["owner"],
            items=json.loads(entity["items"]),
            members=json.loads(entity["members"]),
        )
    
    def delete_from_shopping(self, shoppinglist_id: str, email: EmailRequest):
        entity = self.shoppinglists_table_client.get_entity(
            partition_key="shoppinglist", row_key=shoppinglist_id
        )
        current_members = json.loads(entity["members"])
        if make_rowid(email.email) in current_members:
            current_members.remove(make_rowid(email.email))
            entity["members"] = json.dumps(current_members)
            self.shoppinglists_table_client.update_entity(
                entity=entity, mode=UpdateMode.REPLACE
            )
        return ShoppingList(
            id=shoppinglist_id,
            name=entity["name"],
            owner=entity["owner"],
            items=json.loads(entity["items"]),
            members=json.loads(entity["members"]),
        )
    
    def delete_item_from_shopping(self, shoppinglist_id: str, item: ItemName):
        entity = self.shoppinglists_table_client.get_entity(
            partition_key="shoppinglist", row_key=shoppinglist_id
        )
        current_items = json.loads(entity["items"])
        if make_rowid(item.item) in current_items:
            current_items.remove(make_rowid(item.item))
            entity["items"] = json.dumps(current_items)
            self.shoppinglists_table_client.update_entity(
                entity=entity, mode=UpdateMode.REPLACE
            )
        return ShoppingList(
            id=shoppinglist_id,
            name=entity["name"],
            owner=entity["owner"],
            items=json.loads(entity["items"]),
            members=json.loads(entity["members"]),
        )


    # Items db
    @log
    def create_item(self, item: ItemCreate) -> Item:
        row_key = make_rowid(item.name)
        entity = {"PartitionKey": "item", "RowKey": row_key, "name": item.name}
        try:
            self.items_table_client.create_entity(entity=entity)
            return Item(id=row_key, **item.model_dump())
        except ResourceExistsError as e:
            error_message = "An item with the name provided already exists."
            raise ResourceExistsError(error_message) from e

    @log
    def get_item(self, item_id: str) -> Item:
        entity = self.items_table_client.get_entity(
            partition_key="item", row_key=item_id
        )
        return Item(id=entity["RowKey"], name=entity["name"])

    @log
    def delete_item(self, item_id: str) -> dict:
        self.items_table_client.delete_entity(partition_key="item", row_key=item_id)
        return {"message": f"Item {item_id} deleted"}

    @log
    def list_items(self) -> list[Item]:
        all_entities = list(self.items_table_client.list_entities())
        for entity in all_entities:
            entity["id"] = entity["RowKey"]
        return [Item.model_validate(entity) for entity in all_entities]
