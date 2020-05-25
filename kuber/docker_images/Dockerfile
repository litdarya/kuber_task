FROM cassandra:3.0.20

COPY create_keyspace.sh /usr/local/
RUN chmod +x /usr/local/create_keyspace.sh

COPY ready_probe.sh /usr/local/
RUN chmod +x /usr/local/ready_probe.sh
