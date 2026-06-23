'''Write a Python class called InstagramPost with attributes caption, likes, and comments (a list). 
Add a method add_comment(comment_text) that appends a new comment to the comments list and 
increases the likes by 1.'''

class InstagramPost:
    def __init__(self,caption,likes,comments):
        self.caption=caption
        self.likes=likes
        self.comments=comments

    def add_comment(self,comment_text):
        self.comments.append(comment_text)
        self.likes+=1

caption=input("enter caption:")
likes=int(input("enter likes:"))
comments=[]

post=InstagramPost(caption,likes,comments)

comment_text=input("enter comments:")

post.add_comment(comment_text)

print()
print("post caption:",post.caption)
print("post likes:",post.likes)
print("post comments:",post.comments)