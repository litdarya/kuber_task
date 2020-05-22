CREATE KEYSPACE IF NOT EXISTS favourite
    WITH REPLICATION = {
        'class' : 'SimpleStrategy', 'replication_factor' : 2
    };


CREATE TABLE favourite.user_item (
    user TEXT,
    item TEXT,
    PRIMARY KEY (user, item))
WITH CLUSTERING ORDER BY (item DESC);


INSERT INTO favourite.user_item(user, item)
VALUES ('Darya', 'flowers #1');