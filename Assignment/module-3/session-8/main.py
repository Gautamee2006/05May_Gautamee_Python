'''Organize your code by creating a package called insta_utils with two modules: likes.py 
(function: like_count(current, increment)) and comments.py
 (function: comment_count(current, new_comments)). In a main.py file,
 import both modules and simulate updating likes and comments for a post.'''

from insta_utils import likes
from insta_utils import comments

current_likes = int(input("Enter current likes: "))
new_likes = int(input("Enter new likes: "))

current_comments = int(input("Enter current comments: "))
new_comments = int(input("Enter new comments: "))

total_likes = likes.like_count(current_likes,new_likes)
total_comments = comments.comment_count(current_comments, new_comments)

print("\nUpdated Post Details")
print("Total Likes:", total_likes)
print("Total Comments:", total_comments)