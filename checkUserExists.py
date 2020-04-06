import json
import pymongo
import falcon
import hashlib

class CheckUserExists(object):

    def __init__(self):
        with open("mongoCredentials.txt", "r") as file:
            creds = [x.strip() for x in file.readlines()]
            self.client = pymongo.MongoClient("mongodb+srv://"+creds[0]+":"+creds[1]+"@cluster0-rv4qi.mongodb.net/test?retryWrites=true&w=majority")
            self.db = self.client["LetsHang"]
            self.users = self.db["users"]

    def on_post(self, req, resp):

        data = json.loads(req.stream.read().decode('utf-8'))
        try:
            user = self.users.find_one(data)
            if len(list(user)):
                respName = {"status": "success", "username":user["username"], "firstname":user["firstname"], "lastname":user["lastname"], "phone":user["phone"], "email":user["email"]}
            else:
                respName = {"status": "failure", "message":"username or password incorrect"}
        except Exception as e:
            print(e)
            respName = {"status": "failure", "message":str(e)}

        resp.body = json.dumps(respName, ensure_ascii=False)
        resp.status = falcon.HTTP_200
        return 