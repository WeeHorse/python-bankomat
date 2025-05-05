from pydantic import BaseModel
from psycopg2.extensions import connection as PgConnection
import psycopg2

class DBModel(BaseModel):
    conn: PgConnection

    model_config = {
        "arbitrary_types_allowed": True
    }

    @classmethod
    def from_dsn(cls, dsn: str) -> "DBModel":
        return cls(conn=psycopg2.connect(dsn))

    def get_connection(self) -> PgConnection:
        return self.conn
