import json
from tornado.web import RequestHandler
from services.db_proxy import DBProxy

class PingHandler(RequestHandler):
    _response = {
        'status': 'ok'
    }

    def get(self):
        self.write(self._response)
        self.set_status(200)
        self.finish()


class UserItemHandler(RequestHandler):
    def initialize(self):
        self.error_msg = list()
        self.user = None
        self.item = None

    def _get(self):
        try:
            body = json.loads(self.request.body)
            self.user = body.get('user', None)
            self.item = body.get('item', None)
        except json.JSONDecodeError as e:
            self.error_msg.append(str(e))
            self.set_status(400)

    def prepare(self):
        self._get()

        if self.user is None:
            self.set_status(400)
            self.error_msg.append("user field is empty")
        elif ';' in self.user:
            self.set_status(400)
            self.error_msg.append("prohibited symbol ; is in the name")

        if self.item is None:
            self.set_status(400)
            self.error_msg.append("item field is empty")
        elif ';' in self.item:
            self.set_status(400)
            self.error_msg.append("prohibited symbol ; is in the name")

        if self.get_status() != 200:
            log(Exception(self.error_msg), ctx)
            self.write({
                "Error msg": self.error_msg
            })
            self.finish()


class AddToFavourite(UserItemHandler):
    async def post(self, *args, **kwargs):
        db: DBProxy = self.application.db_proxy
        success = await db.insert_user_item_if_not_exists(user=self.user, item=self.item)
        self.write({"Msg": f'tried to add {self.user} {self.item}',
                    "Success": success})


class CheckIfFavourite(UserItemHandler):
    async def post(self, *args, **kwargs):
        db: DBProxy = self.application.db_proxy
        success = await db.check_if_user_item_exists(user=self.user, item=self.item)
        self.write({"Msg": f'{self.user} {self.item}',
                    "Exists": success})


class RemoveFromFavourite(UserItemHandler):
    async def post(self, *args, **kwargs):
        db: DBProxy = self.application.db_proxy
        success = await db.delete_user_item(user=self.user, item=self.item)
        self.write({"Msg": f'tried to remove {self.item} from {self.user} ',
                    "Success": success})


class GetAllFavourite(RequestHandler):
    def initialize(self):
        self.error_msg = list()
        self.user = None

        try:
            body = json.loads(self.request.body)
            self.user = body.get('user', None)
        except json.JSONDecodeError as e:
            self.error_msg.append(str(e))
            self.set_status(400)

    def prepare(self):
        if self.user is None:
            self.set_status(400)
            self.error_msg.append("user field is empty")
        elif ';' in self.user:
            self.set_status(400)
            self.error_msg.append("prohibited symbol ; is in the name")

        if self.get_status() != 200:
            # log(Exception(self.error_msg), ctx)
            self.write({
                "Error msg": self.error_msg
            })
            self.finish()

    async def get(self, *args, **kwargs):
        db: DBProxy = self.application.db_proxy
        result = await db.get_all_favourite(user=self.user)
        self.write({"Msg": f'tried to get all favourite {self.user}',
                    "Result": result})
