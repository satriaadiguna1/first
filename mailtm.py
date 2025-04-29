import requests
import random
import string
import time

BASE_URL = "https://api.mail.tm"
PASSWORD = "Reno@#$0909"

def get_domains():
    response = requests.get(f"{BASE_URL}/domains")
    response.raise_for_status()
    domains = response.json()["hydra:member"]
    return [d["domain"] for d in domains]

def generate_username():
    random_number = ''.join(random.choices(string.digits, k=5))
    return f"apa{random_number}"

def create_account(email, password):
    payload = {
        "address": email,
        "password": password
    }
    response = requests.post(f"{BASE_URL}/accounts", json=payload)
    if response.status_code == 201:
        print(f"✅ Email berhasil dibuat: {email}")
    elif response.status_code == 422:
        print(f"⚠️ Email {email} sudah dipakai. Coba nama lain.")
    else:
        print(f"❌ Gagal membuat email: {response.status_code} - {response.text}")

def main():
    try:
        jumlah = int(input("Mau bikin email berapa? "))
        if jumlah < 1:
            print("Jumlah harus minimal 1.")
            return
    except ValueError:
        print("Masukkan angka yang valid.")
        return

    print("[*] Mengambil daftar domain dari mail.tm...")
    domains = get_domains()

    if not domains:
        print("[✖] Tidak ada domain tersedia.")
        return

    # Pilih domain yang mengandung 'indigobook.com' jika ada
    chosen_domain = next((d for d in domains if "indigobook.com" in d), domains[0])
    print(f"[✔] Menggunakan domain: {chosen_domain}")

    for i in range(jumlah):
        username = generate_username()
        email = f"{username}@{chosen_domain}"
        create_account(email, PASSWORD)
        time.sleep(1)  # Delay antar request

if __name__ == "__main__":
    main()
