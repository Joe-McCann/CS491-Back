import json
import pymongo
import falcon

class Events(object):

    def __init__(self):
        with open("mongoCredentials.txt", "r") as file:
            creds = [x.strip() for x in file.readlines()]
            self.client = pymongo.MongoClient("mongodb+srv://"+creds[0]+":"+creds[1]+"@cluster0-rv4qi.mongodb.net/test?retryWrites=true&w=majority")
            self.db = self.client["LetsHang"]
            self.events = self.db["Events"]

    def on_post(self, req, resp):
        data = json.loads(req.stream.read().decode('utf-8'))
        if data["method"] == "create event":
            del data["method"]
            try:
                self.events.insert_one(data)
                respName = {"status": "success"}
                resp.body = json.dumps(respName, ensure_ascii=False)
            except Exception as e:
                respName = {"status": "failure", "message":e}
                resp.body = json.dumps(respName, ensure_ascii=False)

        elif data["method"] == "get event":
            del data["method"]
            try:
                event = self.events.find(data)
                dic = event[0]
                del dic["_id"]
                respName = {"status": "success", "event":dic}
                print(respName)
                resp.body = json.dumps(respName, ensure_ascii=False)
            except Exception as e:
                respName = {"status": "failure", "message":e}
                resp.body = json.dumps(respName, ensure_ascii=False)
        else:
            respName = {"status": "failure", "message":"no method specified"}
            resp.body = json.dumps(respName, ensure_ascii=False)
        
        resp.status = falcon.HTTP_200
        return 
