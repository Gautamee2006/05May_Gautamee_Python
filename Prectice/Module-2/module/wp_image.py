import pywhatkit as kit

# Phone number country code ke sath
phone_number = "+917874116909"

# Photo ka path
image_path = r"f:\123\IMG-20250831-WA0004.jpg"

# Caption
caption = "Hello, ye photo Python se bheji gayi hai."

# Photo send
kit.sendwhats_image(
    receiver=phone_number,
    img_path=image_path,
    caption=caption,
    wait_time=30
)

print("Photo send ho gayi.")