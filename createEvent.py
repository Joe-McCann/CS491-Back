import json
from bson import json_util
import pymongo
import falcon

class createEvent(object):

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
        owner = self.users.find({"username":data["username"]})[0]
        participants = data["participants"]
        people = []
        for person in participants:
            cur = list(self.users.find(person))
            if len(cur) != 0:
                p = cur[0]
                people.append({"_id":p["_id"], "firstname":p["firstname"], "lastname":p["lastname"], "username":p["username"], "email":p["email"]})
        data["participants"] = people
        try:
            self.events.insert_one(data)
            self.users.update_one({"_id":owner["_id"]}, {"$push":{"events.mine":data["_id"]}})
            for person in people:
                self.users.update_one({"_id":person["_id"]}, {"$push":{"events.friends":{"_id":data["_id"], "status":"invited"}}})
            respName = {"status": "success"}
            resp.body = json_util.dumps(respName, ensure_ascii=False)
        except Exception as e:
            respName = {"status": "failure", "message":e}
            resp.body = json_util.dumps(respName, ensure_ascii=False)
        
        resp.status = falcon.HTTP_200
        return 
