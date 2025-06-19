from sqlalchemy.orm import DeclarativeBase


class Model(DeclarativeBase):
    pass


metadata_for_alembic = Model.metadata
