import pymongo

with open("mongoCredentials.txt", "r") as file:
  creds = [x.strip() for x in file.readlines()]
  
client = pymongo.MongoClient("mongodb+srv://"+creds[0]+":"+creds[1]+"@cluster0-rv4qi.mongodb.net/test?retryWrites=true&w=majority")
db = client["LetsHang"]
users = db["users"]
import datetime
personDocument = {
  "name": { "first": "Alan", "last": "Turing" },
  "birth": datetime.datetime(1912, 6, 23),
  "death": datetime.datetime(1954, 6, 7),
  "contribs": [ "Turing machine", "Turing test", "Turingery" ],
  "views": 1250000
}
users.insert_one(personDocument)
   