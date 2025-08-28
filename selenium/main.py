import pstats
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
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

# Test sonucu takibi için değişkenler
passed = 0
failed = 0
failed_assertions = []


driver.get("https://www.amazon.com.tr")

# Sayfa başlığını al 
page_title = driver.title
print("Sayfa Başlığı:", page_title)

# Assertion ile kontrol
assert "Amazon" in page_title, "Assertion-1 💥 Homepage yüklenemedi veya başlık beklenenden farklı."
print("Assertion-1 ✅ Homepage başarıyla yüklendi.")
passed += 1

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

#aramayı doğrulama kısmı
searchbar = driver.find_element(By.ID, "twotabsearchtextbox")
if "Samsung" in searchbar.get_attribute("value"):
    print("Assertion-2 ✅  Arama çubuğu Samsung içeriyor sonuçlar doğru...")
    passed += 1
else:
    print("Assertion-2 💥  Arama çubuğu Samsung içermiyor.")
    failed += 1

#2. sayfaya git
page2 = driver.find_element(By.CSS_SELECTOR, "a.s-pagination-item.s-pagination-button")
page2.click()

# Sayfanın 2 olduğunu doğrula  (crush olmaması icin bekler)
current_page = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.CSS_SELECTOR, "span.s-pagination-selected"))
)
if current_page.text.strip() == "2":
    print("Assertion-3 ✅ Sayfa 2 başarıyla görüntülendi.")
    passed += 1
else:
    print(f"Assertion-3 💥 Farklı bir sayfa görünüyor: {current_page.text}")
    failed += 1

# Ürünlerin yüklenmesini bekler
products = WebDriverWait(driver, 10).until(
    EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.s-main-slot img.s-image"))
)

# 3. ürünü seç 
products[2].click()

#wish liste ekler
wishlistbutton = driver.find_element(By.ID, "wishListMainButton")
wishlistbutton.click()

# popupın açılması bekleme
time.sleep(5)

# popuptan çıkmak için esc tuşuna tıklar
ActionChains(driver).send_keys(Keys.ESCAPE).perform()

#navbardan left menü açılır
leftnaw = driver.find_element(By.ID, "nav-hamburger-menu")
leftnaw.click()

#yüklenmesini bekleyip hesabıma tıklama
hesabim_btn = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, "//a[@class='hmenu-item' and normalize-space(text())='Hesabım']"))
)
hesabim_btn.click()

#wishliste gider
wishlist_btn = driver.find_element(By.XPATH, "//div[@data-card-identifier='YourLists']/ancestor::a")
wishlist_btn.click()

# Wishlistteki ürünleri alma
wishlist_items = driver.find_elements(By.CSS_SELECTOR, "span[data-reg-item-delete]")

# İlk ürünü al (en üstteki veya eklediğimiz ürün)
first_item_span = wishlist_items[0]

# Delete butonunu bul
delete_button = first_item_span.find_element(By.CSS_SELECTOR, "input[name='submit.deleteItem']")

# Silmeden önce item idsini alır
item_id_to_delete = delete_button.get_attribute("data-csa-c-item-id")
print(f"Silinen ürün ID: {item_id_to_delete}")

#urunu wish listtewn kaldırır
delete_button.click()

# Sayfanın güncellenmesini bekler
WebDriverWait(driver, 10).until(EC.staleness_of(delete_button))

# Ürünün listede olmadığını doğrulama
try:
    driver.find_element(By.CSS_SELECTOR, f"input[data-csa-c-item-id='{item_id_to_delete}']")
    print("Assertion-4 💥  Ürün hala wishlistte.")
    failed += 1
except:
    print("Assertion-4 ✅  Ürün wishlistten kaldırıldı.")
    passed += 1
   
# Test sonucu
total = passed + failed
print(f"\nTest Skoru: {passed}/{total} Başarılı, {failed}/{total} Başarısız")
    
# sayfa otomatik olarak kapanmasın diye  
while True:
    pass
