import pstats
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
options = Options()

# Chrome ayarları
options = Options()
options.add_argument("--incognito")   # Gizli sekme
options.add_argument("--start-maximized")  # Tamö ekran başlatma

#-------- Konsol loglarını azaltma
options.add_argument("--log-level=3") 
options.add_experimental_option("excludeSwitches", ["enable-logging"])  
#-------- 

#--------
service = Service("./chromedriver.exe")
driver = webdriver.Chrome(service=service, options=options)
#--------

driver.get("https://www.amazon.com.tr")

#Continue Shopping butonu varsa tıkla yoksa devam
try:
    button = driver.find_element(By.XPATH, "//button[text()='Continue shopping']")
    button.click()
except:
    print("Continue shopping butonu yok devam ediyor..")
    
#Hesabım butonuna tıkla
account_lists = driver.find_element(By.ID, "nav-link-accountList")
account_lists.click()

#Eposta adresi girme
LogInBar = driver.find_element(By.ID, "ap_email_login")
LogInBar.send_keys("qa1testing2@gmail.com")

#Devam et butonuna tıklama
continue_bar = driver.find_element(By.ID, "continue")
continue_bar.click()

#Şifre gir
PasswordBar = driver.find_element(By.ID, "ap_password")
PasswordBar.send_keys("qa1testing2")

#Giriş yap butonuna tıklama
SubmitButton = driver.find_element(By.ID, "signInSubmit")
SubmitButton.click()

#Telefon numarası girmek istemiyorsan devam et butonuna tıkla
try:
    NotNowButton = driver.find_element(By.ID, "ap-account-fixup-phone-skip-link")
    NotNowButton.click()
except:
    print("Not now çıkmadı devam ediyor..")
    
#Arama çubuğuna Samsung yaz
searchbar = driver.find_element(By.ID, "twotabsearchtextbox")
searchbar.send_keys("Samsung")

#Arama butonuna tıkla
searchbutton = driver.find_element(By.ID, "nav-search-submit-button")
searchbutton.click()

#2. sayfaya git
page2 = driver.find_element(By.CSS_SELECTOR, "a.s-pagination-item.s-pagination-button")
page2.click()

# Ürünler yüklenene kadar bekle (gec yuklendigi icin secemiyor)
products = WebDriverWait(driver, 6).until(
    EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div[data-component-type='s-search-result']"))
)

# 3. ürünü bul
third_product = products[2]

# 3. ürünün sepete ekle butonuna tıkla  //  id ile çalışmıyor id'ye index atıyor bu yüzden name ile çağırdım
add_to_cart_button = third_product.find_element(By.NAME, "submit.addToCart")
add_to_cart_button.click()


# sayfa otomatik olarak kapanmasın diye
while True:
    pass
