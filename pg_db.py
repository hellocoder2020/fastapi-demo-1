import databases, sqlalchemy

## Postgres Database
DATABASE_URL = "postgresql://usertest:usertest222@127.0.0.1:5432/dbtest"
database = databases.Database(DATABASE_URL)
metadata = sqlalchemy.MetaData()

users = sqlalchemy.Table(
    "py_users",
    metadata,
    sqlalchemy.Column("id"        , sqlalchemy.String, primary_key=True),
    sqlalchemy.Column("username"  , sqlalchemy.String),
    sqlalchemy.Column("password"  , sqlalchemy.String),
    sqlalchemy.Column("first_name", sqlalchemy.String),
    sqlalchemy.Column("last_name" , sqlalchemy.String),
    sqlalchemy.Column("gender"    , sqlalchemy.CHAR  ),
    sqlalchemy.Column("create_at" , sqlalchemy.String),
    sqlalchemy.Column("status"    , sqlalchemy.CHAR  ),
)

engine = sqlalchemy.create_engine(
    DATABASE_URL
)
metadata.create_all(engine)