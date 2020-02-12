import json
import pymongo
import falcon

class HelloWorld(object):

    def on_get(self, req, resp):
        ret_data = {"status":"Good", "message":"Hello World"}
        resp.body = json.dumps(ret_data, ensure_ascii=False)
        resp.status = falcon.HTTP_200
        return 

    def on_post(self, req, resp):
        data = json.loads(req.stream.read().decode('utf-8'))
        respName = {"name": data["name"]}
        resp.body = json.dumps(respName, ensure_ascii=False)
        resp.status = falcon.HTTP_200
        return 
        