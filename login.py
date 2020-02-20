import json
import pymongo
import falcon

class Login(object):

    def __init__(self):
        with open("mongoCredentials.txt", "r") as file:
            creds = [x.strip() for x in file.readlines()]
            self.client = pymongo.MongoClient("mongodb+srv://"+creds[0]+":"+creds[1]+"@cluster0-rv4qi.mongodb.net/test?retryWrites=true&w=majority")
            self.db = self.client["LetsHang"]
            self.users = self.db["users"]

    def on_post(self, req, resp):
        data = json.loads(req.stream.read().decode('utf-8'))
        if data["method"] == "register":
            del data["method"]

            try:
                total = self.users.count_documents({"email":data["email"]})
                if total == 0:
                    self.users.insert_one(data)
                    respName = {"status": "success"}
                else:
                    respName = {"status": "failure", "message":"user already registered with that email"}
            except Exception as e:
                respName = {"status": "failure", "message":e}

        elif data["method"] == "login":
            del data["method"]
            try:
                user = self.users.find(data)
                if len(list(user)):
                    respName = {"status": "success"}
                else:
                    respName = {"status": "failure", "message":"username or password incorrect"}
            except Exception as e:
                print(e)
                respName = {"status": "failure", "message":e}
        else:
            respName = {"status": "failure", "message":"no method specified"}

        resp.body = json.dumps(respName, ensure_ascii=False)
        resp.status = falcon.HTTP_200
        return 