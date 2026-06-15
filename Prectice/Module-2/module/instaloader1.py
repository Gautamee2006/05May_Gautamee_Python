'''import instaloader

instaid="topstech"
x=instaloader.Instaloader()

x.download_profile(instaid,profile_pic_only=True)'''

from instagrapi import Client

cl = Client()

user_id = cl.user_id_from_username("topstech")
user = cl.user_info(user_id)

print(user.public_phone_country_code)