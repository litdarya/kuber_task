DEFAULT_PORT = 8000

CASSANDRA_CONF = {
    'contact_points': (
        'cassandra-0.cassandra.default.svc.cluster.local',
    ),
    'executor_threads': 8,
}