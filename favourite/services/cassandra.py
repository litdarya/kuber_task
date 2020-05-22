class CassandraManager:
    def __init__(self, session):
        self.session = session

        self.prepared_queries = {
            'insert_user_item_if_not_exists': self._prepare_insert_user_item_if_not_exists,
            'check_if_user_item_exists': self._prepare_check_if_user_item_exists,
            'delete_user_item': self._prepare_delete_user_item,
            'get_all_favourite': self._prepare_get_all_favourite
        }

    @property
    def _prepare_insert_user_item_if_not_exists(self):
        query = '''INSERT INTO
                   user_item (user, item)
                   VALUES (?, ?)
                   IF NOT EXISTS;'''
        return self.session.prepare(query)

    @property
    def _prepare_check_if_user_item_exists(self):
        query = '''SELECT user, item
                   FROM user_item
                   WHERE user = ? AND item = ?
                   LIMIT 1;
                   '''
        return self.session.prepare(query)

    @property
    def _prepare_delete_user_item(self):
        query = '''DELETE FROM user_item 
                   WHERE user=? and item=?
                   IF EXISTS;
                   '''
        return self.session.prepare(query)

    @property
    def _prepare_get_all_favourite(self):
        query = '''SELECT item
                   FROM user_item
                   WHERE user=?;
                   '''
        return self.session.prepare(query)

    async def get_all_favourite(self, *, user) -> list:
        result = await self.session.execute_future(
            self.prepared_queries['get_all_favourite'],
            parameters=(user,)
        )

        assert result is not None

        return list(map(lambda row: row.item, result))

    async def delete_user_item(self, *, user, item) -> bool:
        result = await self.session.execute_future (
            self.prepared_queries['delete_user_item'],
            parameters=(user, item)
        )

        assert result is not None
        assert len(result) == 1

        return result[0].applied

    async def check_if_user_item_exists(self, *, user, item) -> bool:
        result = await self.session.execute_future(
            self.prepared_queries['check_if_user_item_exists'],
            parameters=(user, item)
        )

        return not len(result) == 0

    async def insert_user_item_if_not_exists(self, *, user, item) -> bool:
        result = await self.session.execute_future(
            self.prepared_queries['insert_user_item_if_not_exists'],
            parameters=(user, item)
        )

        assert result is not None
        assert len(result) == 1

        return result[0].applied
