import json
from bson import json_util
import pymongo
import falcon
from bson import objectid
from sendText import SendText

class inviteEvent(object):

    def __init__(self):
        with open("mongoCredentials.txt", "r") as file:
            creds = [x.strip() for x in file.readlines()]
            self.client = pymongo.MongoClient("mongodb+srv://"+creds[0]+":"+creds[1]+"@cluster0-rv4qi.mongodb.net/test?retryWrites=true&w=majority")
            self.db = self.client["LetsHang"]
            self.events = self.db["Events"]
            self.users = self.db["users"]
            self.st = SendText()

    def on_post(self, req, resp):
        """
        Request
        {
            "oid": "5ee0690ef7687bc5bb720a79", #example here
            "users":[{identifying info}, ... ]
        }
        
        Response
        {
            "status": standard shit
        }
        """
        data = json.loads(req.stream.read().decode('utf-8'))
        eid = objectid.ObjectId(data["oid"])

        for identifyingInfo in data["users"]:
            user = self.users.find_one(identifyingInfo)
            if user == None:
                if "phone" in identifyingInfo:
                    self.st.sendText("You have been invited to an event on Let's Hang, visit the app to check it out!", identifyingInfo["phone"])
            else:
                self.events.update({"_id":eid}, {"$addToSet":{"participants":{key:user[key] for key in ["_id","firstname","lastname","username","email"]}}})
                self.users.update({"_id":user["_id"]}, {"$addToSet":{"events.friends":{"_id":eid, "status":"invited"}}})

        try:
            respName = {"status":"success"}
            resp.body = json_util.dumps(respName, ensure_ascii=False)
        except Exception as e:
            respName = {"status": "failure", "message":str(e)}
            resp.body = json_util.dumps(respName, ensure_ascii=False)
        
        resp.status = falcon.HTTP_200
        return 
