from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from pymongo import MongoClient
from tqdm import tqdm

# Web sürücüsünü başlatma
driver = webdriver.Chrome()

# MongoDB'bağlantısı
client = MongoClient("mongodb://localhost:27017/")  # MongoDB bağlantı adresi
db = client["smartmaple"]  # Veritabanı adı
collection = db["kitapyurdu"]  # Koleksiyon adı

# Web sitesine git
base_url = "https://www.kitapyurdu.com/index.php?route=product/category&filter_category_all=true&path=1_236&filter_in_stock=1&sort=purchased_365&order=DESC&limit=100"
driver.get(base_url)

time.sleep(1)

# Çerezleri kabul et
accept_cookie = driver.find_element(by=By.XPATH, value="//*[@id='js-popup-accept-button']")
accept_cookie.click()
time.sleep(1)

# Başlangıç değerleri
page_count = 1
data_count = 0

#Elementlerin text değerlerini alan fonksiyon
def get_element_text(element, by, value):
    try:
        return element.find_element(by=by, value=value).text
    except:
        print("\nVeri alınamadı!")
        return ""

#Bütün sayfalar üzerinde gezecek ve son sayfada kapanacak sonsuz döngü 
while True:
    products = driver.find_elements(by=By.CLASS_NAME, value="pr-img-link") #Sayfadaki ürünlerin linkleri

    for product in tqdm(products):
        try:
            product_url = product.get_attribute("href")  # Ürün sayfasının bağlantısı

            driver.execute_script("window.open('', '_blank');")
            time.sleep(1)

            driver.switch_to.window(driver.window_handles[1])  # Yeni sekme geçiş yapar

            driver.get(product_url)

            #Elementlerin ihtiyacımız olan özellikleri
            title = get_element_text(driver, By.CLASS_NAME, "pr_header__heading")
            publisher = get_element_text(driver, By.CLASS_NAME, "pr_producers__publisher")
            writers = get_element_text(driver, By.CLASS_NAME, "pr_producers__manufacturer")
            price = get_element_text(driver, By.CLASS_NAME, "price__item")

            pr_images_div = driver.find_element(by=By.CLASS_NAME, value="pr_images")
            # pr_images div içindeki a etiketini bulma
            a_tag = pr_images_div.find_element(By.TAG_NAME, "a")
            # a etiketinin href özelliğine erişme
            image = a_tag.get_attribute("href")
            
            #Diğer özelliklere erişmek için Tabloyu XPath ile seçebiliriz.
            table = driver.find_element(by=By.XPATH, value='//div[@class="attributes"]/table')
            rows = table.find_elements(by=By.TAG_NAME, value='tr')

            #Diğer Özellikler
            for row in rows:
                cells = row.find_elements(by=By.TAG_NAME, value='td')
                if len(cells) == 2:
                    label = cells[0].text.strip()
                    value = cells[1].text.strip()

                    if label == 'Sayfa Sayısı:':
                        page = value
                    elif label == 'ISBN:':
                        isbn = value

            # Verilerin doğrudan MongoDB'ye kaydedilmesi
            collection.insert_one({
                "title": title,
                "publisher": publisher,
                "writers": writers,
                "price": price,
                "page": page,
                "image": image,
                "isbn": isbn
            })

            data_count += 1
            time.sleep(1)

            # Detay sayfasındaki verileri aldıktan sonra liste sayfasına dönmek için sekmeyi kapatıp değiştirme
            driver.close() 
            driver.switch_to.window(driver.window_handles[0])

        except Exception as e:
            print("Kitap bilgisi alınırken hata oluştu!", str(e))

            driver.close() 
            driver.switch_to.window(driver.window_handles[0])
            continue

    # Sonraki sayfaya geçme komutu
    next_page = driver.find_element(by=By.CLASS_NAME, value="next")
    if not next_page:
        break  # Son sayfadaysak döngüyü bitir

    next_page.click()  # Sonraki sayfaya geç
    page_count += 1

    print("yeni sayfaya geçildi, ", "Sayfa Sayısı: ", page_count)
    print("Kazınan toplam veri: ", data_count)    
    time.sleep(1)  # Yeni sayfanın yüklenmesini bekle

# Tarayıcıyı kapatma
driver.quit()

print("Veriler MongoDB'ye kaydedildi.")
