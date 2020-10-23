import json
import logging

from botovod.dbdrivers.gino import DBDriver
from sqlalchemy import asc, desc

from .fixtures import FIXTURES
from .models import FollowerState


logger = logging.getLogger(__name__)


class DBClient(DBDriver):
    EMPTY = object()
    QUERY_LOGIC = {
        None: (lambda field, value: field == value),
        "like": (lambda field, value: field.like(value)),
        "lt": (lambda field, value: field < value),
        "le": (lambda field, value: field <= value),
        "gt": (lambda field, value: field > value),
        "ge": (lambda field, value: field >= value),
    }

    def __init__(self, engine, name, host=None, port=None, username=None, password=None):
        self._engine = engine
        self._name = name
        self._host = host
        self._port = port
        self._username = username
        self._password = password

    async def connect(self):
        await super().a_connect(
            engine=self._engine,
            database=self._name,
            host=self._host,
            username=self._username,
            password=self._password,
        )
        logger.info("Connected to database")

    async def close(self):
        await super().a_close()
        logger.debug("Disconnected with database")

    @staticmethod
    async def add_fixtures():
        count = 0
        for fixture in FIXTURES:
            try:
                await fixture["model"].create(**fixture["fields"])
                count += 1
                logger.debug("Add record in table '%s': %s", fixture["model"].__tablename__,
                             fixture["fields"])
            except Exception as exception:
                logger.debug(
                    "Cannot add record in table '%s': %s. Exception message: %s",
                    fixture["model"].__tablename__,
                    fixture["fields"],
                    exception,
                )

        logger.info("Add %d fixtures", count)

    @classmethod
    def _get_query(cls, model, order_by=(), offset=None, limit=None, **kwargs):
        query = model.query
        for key, value in kwargs.items():
            field, *operation = key.rsplit("__", 1)
            field = getattr(model, field)
            operation = operation[0] if operation else None
            query = query.where(cls.QUERY_LOGIC[operation](field=field, value=value))

        for order in order_by:
            function = asc
            if order[0] == "-":
                order = order[1:]
                function = desc
            query = query.order_by(function(getattr(model, order)))

        if offset is not None:
            query = query.offset(offset)
        if limit is not None:
            query = query.limit(limit)

        return query

    @classmethod
    async def get_follower_state(cls, **kwargs):
        return await cls._get_query(model=FollowerState, **kwargs).gino.first()

    @classmethod
    async def get_followers_states(cls, **kwargs):
        return await cls._get_query(model=FollowerState, **kwargs).gino.all()

    @classmethod
    async def create_follower_state(cls, follower):
        return await FollowerState.create(follower_id=follower.id)

    @classmethod
    async def update_follower_state(cls, follower_state, state, data):
        await follower_state.update(state=state, data=json.dumps(data)).apply()

