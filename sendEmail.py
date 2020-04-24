import smtplib
from email.message import EmailMessage

class SendEmail():
  
  def __init__(self):
    with open("emailCredentials.txt", "r") as file:
      creds = [x for x in file.readline().split()]
      self.origin = creds[0]
      self.pw = creds[1]
  
  def sendEmail(self, subject, content, recipients):
    msg = self.createMessage(subject, content, recipients)
    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.starttls()
    s.login(self.origin, self.pw)
    try:
      s.send_message(msg)
      print("Sent email!")
    except Exception as e:
      print(e)
    s.quit()
  
  def createMessage(self, subject, content, recipients):
    msg = EmailMessage()
    msg['Subject'] = subject
    msg["From"] = self.origin
    msg['Bcc'] = recipients
    msg.set_content(content)
    return msg
