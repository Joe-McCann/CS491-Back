import json
from bson import json_util
import pymongo
import falcon

class friendRequest(object):

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
        }
        
        Response
        {
            all the events your part of
        }
        """
        data = json.loads(req.stream.read().decode('utf-8'))
        owner = self.users.find_one(data["user"])
        friend = self.users.find_one(data["request"])
        owner_insert = {key : owner[key] for key in ["_id", "username", "firstname", "lastname"]}
        friend_insert = {key : friend[key] for key in ["_id", "username", "firstname", "lastname"]}
        owner_insert["status"] = "waiting"
        friend_insert["status"] = "pending"
        self.users.update_one({"_id":owner_insert["_id"]}, {"$addToSet":{"friends":friend_insert}})
        self.users.update_one({"_id":friend_insert["_id"]}, {"$addToSet":{"friends":owner_insert}})
        #print(owner_insert, friend_insert)
        try:
            respName = {"status":"success"}
            resp.body = json_util.dumps(respName, ensure_ascii=False)
        except Exception as e:
            respName = {"status": "failure", "message":str(e)}
            resp.body = json_util.dumps(respName, ensure_ascii=False)
        
        resp.status = falcon.HTTP_200
        return 
