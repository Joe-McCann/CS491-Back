import json
import pymongo
import falcon
<<<<<<< HEAD
=======
import hashlib
>>>>>>> 7d3f5fba7605bcb985c156ff2c2d8501a2ed7aab

class Register(object):

    def __init__(self):
        with open("mongoCredentials.txt", "r") as file:
            creds = [x.strip() for x in file.readlines()]
            self.client = pymongo.MongoClient("mongodb+srv://"+creds[0]+":"+creds[1]+"@cluster0-rv4qi.mongodb.net/test?retryWrites=true&w=majority")
            self.db = self.client["LetsHang"]
            self.users = self.db["users"]

    def on_post(self, req, resp):
        data = json.loads(req.stream.read().decode('utf-8'))
        try:
            total = self.users.count_documents({"email":data["email"]})
            if total == 0:
                # Hash password before storing
                data["password"] = hashlib.sha512(data["password"].encode()).hexdigest()
                self.users.insert_one(data)
                respName = {"status": "success"}
            else:
                respName = {"status": "failure", "message": "User already registered with that email"}
        except Exception as e:
            print(e)
            respName = {"status": "failure", "message": e}

        resp.body = json.dumps(respName, ensure_ascii=False)
        resp.status = falcon.HTTP_200
        return 