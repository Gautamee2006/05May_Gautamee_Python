'''Use ChatGPT to generate a Python example where a base class Notification has a send() method, 
and two subclasses (EmailNotification, SMSNotification) override send() to print different messages.
Paste the generated code, run it, and write one line explaining 
how method overriding works in your example.'''

class Notification:
    def send(self):
        print("sending notification")

class EmailNotification(Notification):
    def send(self):
        print("sending email notificatiob")

class SMSNotification(Notification):
    def send(self):
        print("sending sms notification")

e=EmailNotification()
s=SMSNotification()

e.send()
s.send()