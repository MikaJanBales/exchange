import databases
import ormar
import sqlalchemy

from exchange.app.config import settings

database = databases.Database(settings.db_url)
metadata = sqlalchemy.MetaData()


class BaseMeta(ormar.ModelMeta):
    metadata = metadata
    database = database


class Currency(ormar.Model):
    class Meta(BaseMeta):
        tablename = "Courses"

    id: int = ormar.Integer(primary_key=True)
    pair_name: str = ormar.String(max_length=10, nullable=False)
    price: int = ormar.Float(nullable=False)


engine = sqlalchemy.create_engine(settings.db_url)
metadata.create_all(engine)
