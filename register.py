import json
import pymongo
import falcon
import hashlib

class Register(object):

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
            "username":"username"
            "firstname":"first name",
            "lastname":"last name",
            "email":"email",
            "password":"password",
            "phone":"phone number"
        }

        Response
        {
            "status": "success" \ "failure",
            "message": "something about the failure"
        }
        """
        data = json.loads(req.stream.read().decode('utf-8'))
        data["friends"] = []
        data["events"] = {"mine":[], "friends":[]}
        try:
            total1 = self.users.count_documents({"email":data["email"]})
            total2 = self.users.count_documents({"username":data["username"]})
            total3 = self.users.count_documents({"phone":data["phone"]})
            if total1 != 0:
                respName = {"status": "failure", "message": "User already registered with that email"}
            elif total2 != 0:
                respName = {"status": "failure", "message": "User already registered with that username"}
            elif total3 != 0:
                respName = {"status": "failure", "message": "User already registered with that phone number"}
            else:     
                # Hash password before storing
                data["password"] = hashlib.sha512(data["password"].encode()).hexdigest()
                self.users.insert_one(data)
                respName = {"status": "success"}
        except Exception as e:
            print(e)
            respName = {"status": "failure", "message": e}

        resp.body = json.dumps(respName, ensure_ascii=False)
        resp.status = falcon.HTTP_200
        return 