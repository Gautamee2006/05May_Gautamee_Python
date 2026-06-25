'''Create a class InstaStory with a method share() that prints 'Sharing an image story'.
Now create another class WhatsAppStory that overrides share() to print 'Sharing a text status'.
Instantiate both and call share() to show method overriding in action.'''

class InstaStory:
    def share(self):
        print("Sharing an image story")

class WhatsAppStory(InstaStory):
    def share(self):
        print("Sharing a text status")
i=InstaStory()
w=WhatsAppStory()
i.share()
w.share()