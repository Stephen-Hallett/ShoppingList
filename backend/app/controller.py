import logging
import os
from uuid import uuid4

from azure.data.tables import TableServiceClient, UpdateMode

from .schemas import (
    Item,
    ItemCreate,
    Itemmap,
    ItemmapCreate,
    ItemmapUpdate,
    ItemUpdate,
    List,
    ListCreate,
    ListUpdate,
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
        self.lists_table_client = self.table_service.get_table_client("lists")
        self.items_table_client = self.table_service.get_table_client("items")
        self.itemmaps_table_client = self.table_service.get_table_client("itemmap")

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

    # Lists db
    @log
    def create_list(self, _list: ListCreate) -> List:
        row_key = str(uuid4())
        entity = {"PartitionKey": "list", "RowKey": row_key, "name": _list.name}
        self.lists_table_client.create_entity(entity=entity)
        return List(id=row_key, **_list.model_dump())

    @log
    def get_list(self, list_id: str) -> List:
        entity = self.lists_table_client.get_entity(
            partition_key="list", row_key=list_id
        )
        return List(id=entity["RowKey"], name=entity["name"])

    @log
    def update_list(self, list_id: str, _list: ListUpdate) -> List:
        entity = self.lists_table_client.get_entity(
            partition_key="list", row_key=list_id
        )

        if _list.name is not None:
            entity["name"] = _list.name

        self.lists_table_client.update_entity(entity=entity, mode=UpdateMode.REPLACE)
        return List(id=list_id, name=entity["name"])

    @log
    def delete_list(self, list_id: str) -> dict:
        self.lists_table_client.delete_entity(partition_key="list", row_key=list_id)
        return {"message": f"List {list_id} deleted"}

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

    # Itemmaps db
    @log
    def create_itemmap(self, itemmap: ItemmapCreate) -> Itemmap:
        row_key = str(uuid4())
        entity = {
            "PartitionKey": "itemmap",
            "RowKey": row_key,
            "item_id": itemmap.item_id,
            "list_id": itemmap.list_id,
        }
        self.itemmaps_table_client.create_entity(entity=entity)
        return Itemmap(id=row_key, **itemmap.model_dump())

    @log
    def get_itemmap(self, itemmap_id: str) -> Itemmap:
        entity = self.itemmaps_table_client.get_entity(
            partition_key="itemmap", row_key=itemmap_id
        )
        return Itemmap(id=entity["RowKey"], name=entity["name"])

    @log
    def update_itemmap(self, itemmap_id: str, itemmap: ItemmapUpdate) -> Itemmap:
        entity = self.itemmaps_table_client.get_entity(
            partition_key="itemmap", row_key=itemmap_id
        )

        if itemmap.name is not None:
            entity["name"] = itemmap.name

        self.itemmaps_table_client.update_entity(entity=entity, mode=UpdateMode.REPLACE)
        return Itemmap(id=itemmap_id, name=entity["name"])

    @log
    def delete_itemmap(self, itemmap_id: str) -> dict:
        self.itemmaps_table_client.delete_entity(
            partition_key="itemmap", row_key=itemmap_id
        )
        return {"message": f"Itemmap {itemmap_id} deleted"}
