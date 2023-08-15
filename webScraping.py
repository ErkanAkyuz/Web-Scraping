import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import re
import pandas as pd

""" Chrome Driver """
service = Service("./chromedriver.exe")

""" Chrome Ayarları """
chromeOptions = Options()
chromeOptions.add_argument("--disable-infobars")
chromeOptions.add_argument("--allow-running-insecure-content")
chromeOptions.add_argument("--disable-notifications")
chromeOptions.add_argument("--disable-save-password")
chromeOptions.add_argument("--disable-extensions")
chromeOptions.add_argument("--disable-popup-blocking")
chromeOptions.add_argument("--headless")

""" Otomasyonun Başlatılması """
driver = webdriver.Chrome(service=service, options=chromeOptions)
driver.implicitly_wait(15)

""" Linke Yönlendirme """
link = "http://ilan.tasimacilar.com/isim-var-arac-ariyorum/"
driver.get(link)

""" Verilerin depolanması """
kullaniciListesi = set()
def verileri_kaydet(x):
    veriler = list(kullaniciListesi)
    pattern = re.compile(r'(.+)\n.+Tarihi : .+\n([\d()-]+)')
    veri_listesi = []

    for veri in veriler:
        match = pattern.match(veri)
        if match:
            isim = match.group(1)
            numara = match.group(2)
            # Numaradaki - işaretlerini ve () karakterlerini kaldırarak sadece sayıları alır
            numara = re.sub(r'[-()\s]', '', numara)
            veri_listesi.append({"İsim": isim, "Numara": numara})

    # Sayfa sayısına göre excel dosyasına kaydet
    df = pd.DataFrame(veri_listesi)
    excel_dosya_adi = f"sayfa{str(x)}.xlsx"
    df.to_excel(excel_dosya_adi, index=False)
    print(f"Veriler {excel_dosya_adi} dosyasına kaydedildi.")


""" Sayfa Sayısı"""
sayfa_sayisi = driver.find_element(By.XPATH, "//*[@id='dsfgfdgdsvfdsa']/div[2]/div/input[2]").get_attribute("value")

"""Veri toplama işlermleri"""
for x in range(1,36):
    for i in range(x-1):
        sonraki_sayfa=driver.find_element(By.XPATH,"//*[@id='dsfgfdgdsvfdsa']/div[2]/div/input[3]")
        sonraki_sayfa.click()
        time.sleep(1)
    for array in range(2, 51):
        if array == 7 or array == 13 or array == 19 or array == 25 or array== 31:
            pass
        else:
            try:
                ilan_detayi = driver.find_element(By.XPATH,"//*[@id='dsfgfdgdsvfdsa']/div[1]/div[" + str(array) + "]/div[1]/a").click()
                bilgiler = driver.find_element(By.XPATH,"/html/body/main/div/div/div[2]/div/div[2]/div[1]").text
                kullaniciListesi.add(bilgiler)
                driver.back()
            except Exception:
                print("sayfa", x, "- ", array, ".sırada Hata Bulundu")
    driver.get(link)
    time.sleep(5)
    verileri_kaydet(x)
    kullaniciListesi=set()
driver.quit()
