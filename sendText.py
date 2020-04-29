from twilio.rest import Client

class SendText():
  def __init__(self):
    with open('twilioCredentials.txt', 'r') as f:
      creds = [x for x in f.readline().split()]
      self.acctSid = creds[0]
      self.token = creds[1]
      self.phoneNumber = creds[2]
    self.client = Client(self.acctSid, self.token)

  def sendText(self, content, recipient):
    try:
      message = self.client.messages \
          .create(
              body=content,
              from_=self.phoneNumber,
              to=recipient
          )
      print("Sent text!")
    except Exception as e:
      print(e)