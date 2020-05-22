import click
from aiocassandra import aiosession
from tornado import ioloop
from tornado.web import Application

import cassandra.io.asyncioreactor
import cassandra.policies
from cassandra.cluster import (Cluster,
                               ExecutionProfile,
                               EXEC_PROFILE_DEFAULT)

from settings import CASSANDRA_CONF, DEFAULT_PORT
from services.cassandra import CassandraManager
from web.urls import get_all_urls
from services.db_proxy import DBProxy


class FavouriteApplication(Application):
    def __init__(self, handlers, **kwargs):
        super(FavouriteApplication, self).__init__(handlers=handlers, **kwargs)

    def prepare(self):
        node_profile = ExecutionProfile(load_balancing_policy=cassandra.policies.RoundRobinPolicy())

        self.cassandra_cluster = Cluster(
            **CASSANDRA_CONF,
            execution_profiles={EXEC_PROFILE_DEFAULT: node_profile}
        )
        self.cassandra_session = self.cassandra_cluster.connect('favourite')
        aiosession(self.cassandra_session)

        self.cassandra_manager = CassandraManager(self.cassandra_session)
        self.db_proxy = DBProxy(cassandra_manager=self.cassandra_manager)


@click.command()
@click.option('--port', default=DEFAULT_PORT)
def serve(port: int):
    handlers = get_all_urls()
    application = FavouriteApplication(handlers)
    application.listen(port)
    application.prepare()
    ioloop.IOLoop.current().start()


if __name__ == '__main__':
    serve()
