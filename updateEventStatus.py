import json
from bson import json_util
import pymongo
import falcon
from bson import objectid

class updateEventStatus(object):

    def __init__(self):
        with open("mongoCredentials.txt", "r") as file:
            creds = [x.strip() for x in file.readlines()]
            self.client = pymongo.MongoClient("mongodb+srv://"+creds[0]+":"+creds[1]+"@cluster0-rv4qi.mongodb.net/test?retryWrites=true&w=majority")
            self.db = self.client["LetsHang"]
            self.users = self.db["users"]

    def on_post(self, req, resp):
        """
        Request
        {
            "user":{identifying information}
            "request":{identifying information}
            "type": reject or accept
        }
        
        Response
        {
            all the events your part of
        }
        """
        data = json.loads(req.stream.read().decode('utf-8'))
        eid = objectid.ObjectId(data["oid"])

        self.users.update({"username":data["username"], "events.friends._id":eid}, {"$set":{"events.friends.$.status":data["status"]}})
        #self.users.update({"username":data["username"]}, {"$set":{"events.friends.0.status":data["status"]}})
        try:
            respName = {"status":"success"}
            resp.body = json_util.dumps(respName, ensure_ascii=False)
        except Exception as e:
            respName = {"status": "failure", "message":str(e)}
            resp.body = json_util.dumps(respName, ensure_ascii=False) 

        resp.status = falcon.HTTP_200
        return 
