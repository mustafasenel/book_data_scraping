# KitapYurdu, Kitapsepeti Veri Kazıma ve MongoDB Entegrasyonu

![Python](https://img.shields.io/badge/Python-3.x-blue.svg)
![Selenium](https://img.shields.io/badge/Selenium-3.141.0-green.svg)
![pymongo](https://img.shields.io/badge/pymongo-3.12.0-red.svg)

Bu proje, kitapyurdu.com adlı web sitesinden kitap verilerini otomatik olarak kazımak (web scraping) ve elde edilen verileri MongoDB veritabanına kaydetmek için Python dilinde geliştirilmiştir.

- data/ klasörü içerisinde her iki web sitesinden kazınan bilim-mühendislik kategorisi altındaki tüm kitapların verileri csv formatında sunulmuştur.

## İşlev ve Özellikler

- kitapyurdu.com ve kitapsepeti.com sitesinde yer alan belirlenen kategorideki tüm kitapların verilerini otomatik olarak kazır ve bu verileri MongoDB veritabanına kaydeder.
- Kazınan kitap verileri, kitap başlığı, yayınevi, yazar, fiyat, sayfa sayısı, kapak resmi ve ISBN numarası gibi önemli bilgileri içerir.
- Web scraping işlemleri için Selenium kütüphanesi kullanılır. Bu sayede, web tarayıcısı otomasyonu sağlanarak sayfalar arasında gezinme ve içeriklere erişme işlemleri gerçekleştirilir.
- Veriler, MongoDB veritabanına pymongo kütüphanesi ile kaydedilir.
- Kod, hatalara karşı korumak için `try-except` blokları kullanır ve veri çekilemediği durumlarda devam etmeyi sağlar.
- Ayrıca tqdm kütüphanesi ile terminal ekranında veri kazıma işlemi kolay takip edilir.

## Kullanılan Kütüphaneler ve Gereksinimler

- [Python](https://www.python.org/downloads/): Proje Python 3.x sürümleriyle uyumludur.
- [Selenium](https://pypi.org/project/selenium/): Web tarayıcısı otomasyonu sağlamak için kullanılır.
- [pymongo](https://pypi.org/project/pymongo/): Python ile MongoDB arasında veri iletişimi için kullanılır.
- [tqdm](https://pypi.org/project/tqdm/): İlerleme çubuğu oluşturmak için kullanılır.

## Kurulum ve Kullanım

1.  Projenin çalıştırılabilmesi için Python'un bilgisayarınızda yüklü olması gereklidir.
2.  Projenin çalışması için gerekli olan kütüphanelerin yüklenmesi:

    ```
    pip install -r requirements.txt
    ```

3.  Proje dosyasındaki `webdriver.Chrome()` satırında kullanacağınız web tarayıcısını belirleyin. Bu projede Chrome tarayıcısı kullanılmıştır. Bu nedenle sisteminizde Chrome web tarayıcısı ve uyumlu sürücüsü yüklü olmalıdır.
4.  "MongoClient" fonksiyonu ile MongoDB bağlantısı kurun. Bağlantı adresi `("mongodb://localhost:27017/")` projedeki adresinizle uyumlu olacak şekilde düzenlenmelidir. Veritabanı adı ve koleksiyon adı da belirtilmelidir.
5.  "base_url" değişkenine belirlenen kategorideki tüm kitapların web sitesi adresini atayın.
6.  kitapyurdu.com web sitesinden veri kazımak için:
        
    ```
    python kitapyurdu.py
    ```

7.  kitapsepeti.com web sitesinden veri kazımak için:

    ```
    python kitapsepeti.py
    ```

    Komutlarını çalıştırın. Selenium aracılığıyla web sitesi açılacak ve belirtilen filtrelerle kitap verilerini içeren sayfaya yönlendirilecektir.
8.  Terminal ekranından kazınan veri sayısı, hangi safyada işlem yapıldığı ve sayfa içerisinde hangi elemanda işlem yapıldığı tqdm kütüphanesi ile görselleştirilmiştir.

## Not

- Bu kod örneği, özellikle kitapyurdu.com ve kitapsepeti.com sitesine özgü olarak tasarlanmıştır. Farklı web sitelerine uygulamak için HTML yapısı ve element seçimleri düzenlenmelidir.
