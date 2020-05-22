FROM python:3.7.3

RUN mkdir -p /app
WORKDIR /app
COPY favourite/requirements.txt .
RUN pip3 install -r requirements.txt
COPY favourite /app/favourite
CMD exec cqlsh localhost -f create_tables.cql
CMD exec python3 favourite/client.py --port 8000