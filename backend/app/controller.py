import logging
import os
from uuid import uuid4

from azure.data.tables import TableServiceClient, UpdateMode

from .schemas import (
    Item,
    ItemCreate,
    ItemUpdate,
    ShoppingList,
    ShoppingListCreate,
    ShoppingListUpdate,
    Test,
    User,
    UserCreate,
    UserUpdate,
)
from .util import log

logger = logging.getLogger(__name__)


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
        row_key = str(uuid4())
        entity = {
            "PartitionKey": "user",
            "RowKey": row_key,
            "email": user.email,
            "name": user.name,
        }
        self.users_table_client.create_entity(entity=entity)
        return User(id=row_key, **user.model_dump())

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
        if user.email is not None:
            entity["email"] = user.email

        self.users_table_client.update_entity(entity=entity, mode=UpdateMode.REPLACE)
        return User(id=user_id, email=entity["email"], name=entity["name"])

    @log
    def delete_user(self, user_id: str) -> dict:
        self.users_table_client.delete_entity(partition_key="user", row_key=user_id)
        return {"message": f"User {user_id} deleted"}

    # ShoppingLists db
    @log
    def create_shoppinglist(self, shoppinglist: ShoppingListCreate) -> ShoppingList:
        row_key = str(uuid4())
        entity = {
            "PartitionKey": "shoppinglist",
            "RowKey": row_key,
            "name": shoppinglist.name,
            "items": shoppinglist.items,
        }
        self.shoppinglists_table_client.create_entity(entity=entity)
        return ShoppingList(id=row_key, **shoppinglist.model_dump())

    @log
    def get_shoppinglist(self, shoppinglist_id: str) -> ShoppingList:
        entity = self.shoppinglists_table_client.get_entity(
            partition_key="shoppinglist", row_key=shoppinglist_id
        )
        return ShoppingList(
            id=entity["RowKey"], name=entity["name"], items=entity["items"]
        )

    @log
    def update_shoppinglist(
        self, shoppinglist_id: str, shoppinglist: ShoppingListUpdate
    ) -> ShoppingList:
        entity = self.shoppinglists_table_client.get_entity(
            partition_key="shoppinglist", row_key=shoppinglist_id
        )

        if shoppinglist.name is not None:
            entity["name"] = shoppinglist.name
        if shoppinglist.items is not None:
            entity["items"] = shoppinglist.items

        self.shoppinglists_table_client.update_entity(
            entity=entity, mode=UpdateMode.REPLACE
        )
        return ShoppingList(
            id=shoppinglist_id, name=entity["name"], items=entity["items"]
        )

    @log
    def delete_shoppinglist(self, shoppinglist_id: str) -> dict:
        self.shoppinglists_table_client.delete_entity(
            partition_key="shoppinglist", row_key=shoppinglist_id
        )
        return {"message": f"ShoppingList {shoppinglist_id} deleted"}

    # Items db
    @log
    def create_item(self, item: ItemCreate) -> Item:
        row_key = str(uuid4())
        entity = {"PartitionKey": "item", "RowKey": row_key, "name": item.name}
        self.items_table_client.create_entity(entity=entity)
        return Item(id=row_key, **item.model_dump())

    @log
    def get_item(self, item_id: str) -> Item:
        entity = self.items_table_client.get_entity(
            partition_key="item", row_key=item_id
        )
        return Item(id=entity["RowKey"], name=entity["name"])

    @log
    def update_item(self, item_id: str, item: ItemUpdate) -> Item:
        entity = self.items_table_client.get_entity(
            partition_key="item", row_key=item_id
        )

        if item.name is not None:
            entity["name"] = item.name

        self.items_table_client.update_entity(entity=entity, mode=UpdateMode.REPLACE)
        return Item(id=item_id, name=entity["name"])

    @log
    def delete_item(self, item_id: str) -> dict:
        self.items_table_client.delete_entity(partition_key="item", row_key=item_id)
        return {"message": f"Item {item_id} deleted"}
