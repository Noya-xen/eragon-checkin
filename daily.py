import os
import time
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Konfigurasi folder dan file token
TOKEN_FOLDER = "../token"
TOKEN_FILE = f"{TOKEN_FOLDER}/token.json"
WEBSITE_URL = "https://eragon.gg/store/home"
XPATH_POPUP = "/html/div[1]"
XPATH_CLAIM = "/html/body/div[3]/div[3]/div/section/div/div[2]/div[2]/div/button"

# Fungsi untuk meminta akses token dari pengguna
def request_access_tokens():
    print("Masukkan akses token Anda (pisahkan dengan koma jika lebih dari satu):")
    token_input = input("> ")
    tokens = [token.strip() for token in token_input.split(",") if token.strip()]
    return tokens

# Fungsi untuk menyimpan token ke dalam file JSON
def save_tokens(tokens):
    if not os.path.exists(TOKEN_FOLDER):
        os.makedirs(TOKEN_FOLDER)  # Buat folder jika belum ada
    with open(TOKEN_FILE, "w") as file:
        json.dump(tokens, file, indent=4)
    print(f"Access token disimpan ke {TOKEN_FILE}")

# Fungsi untuk memuat token dari file
def load_tokens():
    try:
        with open(TOKEN_FILE, "r") as file:
            tokens = json.load(file)
            print(f"Ditemukan {len(tokens)} access token.")
            return tokens
    except FileNotFoundError:
        print(f"Error: File {TOKEN_FILE} tidak ditemukan.")
        return []
    except json.JSONDecodeError:
        print(f"Error: Format file {TOKEN_FILE} tidak valid.")
        return []

# Fungsi untuk menjalankan daily check-in menggunakan access token
def checkin_with_token(access_token):
    # Setup Selenium dengan ChromeDriver
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Jalankan dalam mode headless
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")

    driver = webdriver.Chrome(options=chrome_options)
    driver.get(WEBSITE_URL)

    # Menambahkan access token ke header
    script = f"""
    fetch("{WEBSITE_URL}", {{
        method: "GET",
        headers: {{
            "Authorization": "Bearer {access_token}"
        }}
    }});
    """
    driver.execute_script(script)

    # Tunggu halaman memuat ulang dengan token
    driver.refresh()
    time.sleep(5)

    try:
        # Tunggu hingga elemen popup muncul
        popup_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, XPATH_POPUP))
        )
        print("Popup ditemukan, mencoba klaim...")

        # Klik tombol Claim Now
        claim_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, XPATH_CLAIM))
        )
        claim_button.click()
        print("Berhasil melakukan check-in!")
    except Exception as e:
        print(f"Gagal melakukan check-in: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    print("=== Daily Check-In Script ===")

    # Cek apakah file token sudah ada
    tokens = load_tokens()
    if not tokens:
        # Jika tidak ada token, minta dari pengguna
        print("Tidak ada access token yang ditemukan.")
        tokens = request_access_tokens()
        save_tokens(tokens)

    # Proses check-in untuk setiap token
    if tokens:
        for i, token in enumerate(tokens):
            print(f"\n=== Check-in akun ke-{i+1} ===")
            checkin_with_token(token)
            if i < len(tokens) - 1:
                print("Menunggu 5 detik sebelum akun berikutnya...")
                time.sleep(5)
    else:
        print("Tidak ada token yang diproses.")
