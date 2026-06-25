'''Create a function extract_hashtags(text) that uses re.findall() to return all hashtags
 (words starting with #) from a given Instagram-style caption string.'''

import re

caption = input("Enter Instagram caption: ")

hashtags = re.findall(r'#\w+', caption)

print("Hashtags:", hashtags)