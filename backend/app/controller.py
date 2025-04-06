import logging
import os
from uuid import uuid4

from azure.data.tables import TableServiceClient, UpdateMode

from .schemas import Test, User, UserCreate, UserUpdate
from .util import log

logger = logging.getLogger(__name__)


class Controller:
    def __init__(self) -> None:
        self.logger = logging.getLogger(__name__)
        self.table_service = TableServiceClient.from_connection_string(
            conn_str=os.environ["TABLE_CONNECTION"]
        )
        self.users_table_client = self.table_service.get_table_client("users")

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
    def delete_user(self, user_id: str):
        self.users_table_client.delete_entity(partition_key="user", row_key=user_id)
        return {"message": f"User {user_id} deleted"}
