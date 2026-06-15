import pandas as pd
import pywhatkit
import time

data = pd.read_excel(r"E:\Python\Prectice\Module-2\module\number.xlsx")

for number in data["Mobile"]:
    phone = "+91" + str(number)

    pywhatkit.sendwhatmsg_instantly(
        phone,
        "Hello! This is a test message."
    )

    time.sleep(20)