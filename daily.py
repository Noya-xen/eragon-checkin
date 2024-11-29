import os
import time
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

# Konfigurasi folder token dan URL
TOKEN_FOLDER = "../token"
WEBSITE_URL = "https://eragon.gg/store/home"
XPATH_POPUP = "/html/body/div[3]/div[3]/div/section/div/div[2]"
XPATH_CLAIM = "/html/body/div[3]/div[3]/div/section/div/div[2]/div[2]/div/button"

# Fungsi untuk memuat token akun dari folder
def load_tokens():
    tokens = []
    for file_name in os.listdir(TOKEN_FOLDER):
        if file_name.endswith(".json"):
            file_path = os.path.join(TOKEN_FOLDER, file_name)
            with open(file_path, "r") as file:
                tokens.append(json.load(file))
    return tokens

# Fungsi untuk menjalankan daily check-in
def checkin_with_token(token):
    # Setup Selenium dengan ChromeDriver
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Jalankan dalam mode headless
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")

    driver = webdriver.Chrome(options=chrome_options)
    driver.get(WEBSITE_URL)

    # Tambahkan token atau cookie
    for key, value in token.items():
        driver.add_cookie({"name": key, "value": value, "domain": ".eragon.gg"})

    # Refresh halaman agar cookie diterapkan
    driver.refresh()
    time.sleep(5)  # Tunggu popup muncul

    try:
        # Cek jika elemen popup muncul
        popup_element = driver.find_element(By.XPATH, XPATH_POPUP)
        print("Popup ditemukan, mencoba klaim...")

        # Klik tombol Claim Now
        claim_button = driver.find_element(By.XPATH, XPATH_CLAIM)
        claim_button.click()
        print("Berhasil melakukan check-in!")
    except Exception as e:
        print(f"Gagal melakukan check-in: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    tokens = load_tokens()
    print(f"Ditemukan {len(tokens)} akun untuk check-in.")

    for i, token in enumerate(tokens):
        print(f"\n=== Check-in akun ke-{i+1} ===")
        checkin_with_token(token)
        if i < len(tokens) - 1:
            print("Menunggu 5 detik sebelum akun berikutnya...")
            time.sleep(5)
