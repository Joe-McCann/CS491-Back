import json
import pymongo
import falcon
import hashlib

class Login(object):

    def __init__(self):
        with open("mongoCredentials.txt", "r") as file:
            creds = [x.strip() for x in file.readlines()]
            self.client = pymongo.MongoClient("mongodb+srv://"+creds[0]+":"+creds[1]+"@cluster0-rv4qi.mongodb.net/test?retryWrites=true&w=majority")
            self.db = self.client["LetsHang"]
            self.users = self.db["users"]

    def on_post(self, req, resp):
        '''
        Request format
        {
            "email":"some email address string",
            "password":"password for user"
        }

        Response format
        {
            "status":"success" or "failure"
            "message":"..." depending on failure reason
        }
        '''
        data = json.loads(req.stream.read().decode('utf-8'))
        try:
            # Hash password before checking
            data["password"] = hashlib.sha512(data["password"].encode()).hexdigest()
            user = self.users.find_one(data)
            if len(list(user)):
                respName = {"status": "success", "username":user["username"], "firstname":user["firstname"], "lastname":user["lastname"]}
            else:
                respName = {"status": "failure", "message":"username or password incorrect"}
        except Exception as e:
            print(e)
            respName = {"status": "failure", "message":str(e)}

        resp.body = json.dumps(respName, ensure_ascii=False)
        resp.status = falcon.HTTP_200
        return 