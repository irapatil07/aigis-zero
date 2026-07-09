from client import OsqueryClient
from scheduler import QueryScheduler
import asyncio
from asyncio import Queue
import logging #for errors

logger=logging.getLogger(__name__)


class OsqueryConfig:

    def __init__(self, socket_path, db_path):
        self.socket_path = socket_path
        self.db_path = db_path


class OsqueryCollector:

    def __init__(self, config):
        self.config = config

    async def start(self, agent_uuid:str):
      
      result_queue = asyncio.Queue(maxsize=100)
      scheduler = QueryScheduler(self.config.db_path)

      asyncio.create_task(
        scheduler.run(
            result_queue,
            self.config.socket_path,
            agent_uuid,
        )
    )

    return result_queue

    async def live_query(self, sql):

        client = await OsqueryClient.connect(
            self.config.socket_path
        )

        return await client.live_query(sql)

    async def update_schedule(self, queries):

        scheduler = QueryScheduler(
            self.config.db_path
        )

        scheduler.upsert_queries(queries)
     

# Error handling here?
