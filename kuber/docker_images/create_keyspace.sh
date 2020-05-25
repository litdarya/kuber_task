#!/bin/bash

until /usr/local/ready_probe.sh ; do
  echo "Waiting node to be ready" 1>&2
  sleep 1
done

if [ "$(hostname)" == 'cassandra-0' ] ; then
  cqlsh -e "CREATE KEYSPACE IF NOT EXISTS favourite
    WITH REPLICATION = {
        'class' : 'SimpleStrategy',
        'replication_factor' : 2
    };

  CREATE TABLE IF NOT EXISTS favourite.user_item (
      user TEXT,
      item TEXT,
      PRIMARY KEY (user, item))
  WITH CLUSTERING ORDER BY (item DESC);"
fi