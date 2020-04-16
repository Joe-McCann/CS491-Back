import json
from bson import json_util
import pymongo
import falcon
from bson import objectid

class inviteEvent(object):

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
            "name":"event name",
            "username":"username", 
            "firstname":"first name",
            "lastname":"last name",
            "location":{"lat":latitude number, "lng": longitude number}
            "participants":[{"identifying key":"identifying value"}, ... ]
            "date": yyyy/mm/dd
            "time": hh:mm
            "type":"public"/"private"
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
