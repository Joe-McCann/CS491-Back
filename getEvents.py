import json
from bson import json_util
import pymongo
import falcon

class getEvents(object):

    def __init__(self):
        with open("mongoCredentials.txt", "r") as file:
            creds = [x.strip() for x in file.readlines()]
            self.client = pymongo.MongoClient("mongodb+srv://"+creds[0]+":"+creds[1]+"@cluster0-rv4qi.mongodb.net/test?retryWrites=true&w=majority")
            self.db = self.client["LetsHang"]
            self.events = self.db["Events"]
            self.users = self.db["users"]

    def on_post(self, req, resp):
        """
        Request
        {
            "username":"username", 
        }
        
        Response
        {
            all the events your part of
        }
        """
        data = json.loads(req.stream.read().decode('utf-8'))
        owner = self.users.find_one({"username":data["username"]})
        eventsList = {"mine":[], "friends":[], "public":[]}
        for my_event in owner["events"]["mine"]:
            event = self.events.find_one({"_id":my_event})
            #event["_id"]
            eventsList["mine"].append(event)
        print(owner["events"]["friends"])
        for friend_event in owner["events"]["friends"]:
            event = self.events.find_one({"_id":friend_event["_id"]})
            #event["_id"]
            event["status"] = friend_event["status"]
            eventsList["friends"].append(event)
        public_events = self.events.find({"type":"public"})
        for p_event in public_events:
            #p_event["_id"]
            eventsList["public"].append(p_event)
        try:
            respName = eventsList
            resp.body = json_util.dumps(respName, ensure_ascii=False)
        except Exception as e:
            respName = {"status": "failure", "message":e}
            resp.body = json_util.dumps(respName, ensure_ascii=False)
        
        resp.status = falcon.HTTP_200
        return 
