import json
import pymongo
import falcon

class HelloWorld(object):

    def on_get(self, req, resp):
        ret_data = {"status":"Good", "message":"Hello World"}
        resp.body = json.dumps(ret_data, ensure_ascii=False)
        resp.status = falcon.HTTP_200
        return 