from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from pymongo import MongoClient
from tqdm import tqdm

# Web sürücüsünü başlatma
driver = webdriver.Chrome()

# MongoDB'bağlantısı
client = MongoClient("mongodb://localhost:27017/")  # MongoDB bağlantı adresini
db = client["smartmaple"]  # Veritabanı adı
collection = db["kitapsepeti"]  # Koleksiyon adı

# Web sitesine git
base_url = "https://www.kitapsepeti.com/bilim-muhendislik?stock=1"
driver.get(base_url)

time.sleep(10)

# Görünümü değiştir
view = driver.find_element(by=By.XPATH, value="//*[@id='filterSort']/div[2]/div/span[4]")
view.click()
time.sleep(1)

#Başlangıç değerleri
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
    products = driver.find_elements(by=By.XPATH, value="//*[@class='col col-md-4 col-sm-6 col-xs-6 p-right mb productItem zoom ease col-2']/div/div[1]/a")

    for product in tqdm(products):
        try:
            product_url = product.get_attribute("href")  # Ürün sayfasının bağlantısı

            driver.execute_script("window.open('', '_blank');")
            time.sleep(1)

            driver.switch_to.window(driver.window_handles[1])  # Yeni sekme geçiş yapar
            driver.get(product_url)

            title = get_element_text(driver, By.XPATH, "//*[@id='productName']")
            publisher = get_element_text(driver, By.XPATH, "//*[@id='productInfo']/a")
            writers = get_element_text(driver, By.XPATH, "//*[@id='productModelText']")
            price = get_element_text(driver, By.CLASS_NAME, "product-price")

            image = driver.find_element(By.XPATH, "//*[@id='productImage']/li/a/span/img").get_attribute("src") 

            #Diğer özelliklere erişmek için Tabloyu XPath ile seçebiliriz.
            table = driver.find_element(by=By.XPATH, value='//*[@id="productRight"]/div[2]/div[2]')
            rows = table.find_elements(by=By.TAG_NAME, value='div')

            #Diğer Özellikler
            for row in rows:
                cells = row.find_elements(by=By.TAG_NAME, value='span')
                if len(cells) == 2:
                    label = cells[0].text.strip()
                    value = cells[1].text.strip()

                    if label == 'Sayfa Sayısı:':
                        page = value
                    elif label == 'ISBN:':
                        isbn = value

            # Verileri doğrudan MongoDB'ye kaydet
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
    time.sleep(3)

    if not next_page:
        break  # Son sayfadaysak döngüyü bitir


    next_page.click()  # Sonraki sayfaya geç

    # Görünümü değiştir
    view = driver.find_element(by=By.XPATH, value="//*[@id='filterSort']/div[2]/div/span[4]")
    view.click()
    time.sleep(1)

    page_count += 1

    print("Yeni sayfaya geçildi")
    print("Sayfa Sayısı: ", page_count)
    print("Kazınan toplam veri: ", data_count)    
    time.sleep(1)  # Yeni sayfanın yüklenmesini bekle

# Tarayıcıyı kapatma
driver.quit()

print("Veriler MongoDB'ye kaydedildi.")
