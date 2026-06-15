from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

driver = webdriver.Chrome()

driver.get("https://web.whatsapp.com")
input("QR scan karne ke baad Enter dabao...")

number = "917874116909"

driver.get(f"https://web.whatsapp.com/send?phone={number}")

wait = WebDriverWait(driver, 30)

# Chat load hone ka wait
time.sleep(10)

# File input directly find karo
file_input = wait.until(
    EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='file']"))
)

file_input.send_keys(r"F:\123\IMG-20250831-WA0004.jpg")

print("Image selected")

time.sleep(10)

send_btn = wait.until(
    EC.element_to_be_clickable((By.XPATH, '//span[@data-icon="send"]'))
)


send_btn.click()

print("Photo sent")