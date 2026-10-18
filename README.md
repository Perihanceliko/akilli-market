# İŞLETİM SİSTEMİ TEMELLERİ

İşletim sistemi (OS), yazdığın programla bilgisayarın donanımı arasında duran yöneticidir. Programın işlemciye, belleğe veya diske doğrudan dokunmaz; her şeyi işletim sisteminden ister.

Bunu bir restoran gibi düşünebilirsin. Müşteriler (programlar) mutfağa (donanım) giremez. Garson (işletim sistemi) siparişi alır, mutfağa iletir ve sırayı yönetir. Böylece hiçbir müşteri diğerinin yemeğine karışamaz.

Örneğin bir Python programında input() yazdığında, klavyeyi Python okumaz. Python işletim sistemine "klavyeden bir satır getir" der, işletim sistemi bunu yapıp sonucu geri verir. print() da aynı şekilde ekrana yazma işini işletim sistemine devreder.

# 1. Kernel nedir?

Kernel (çekirdek), işletim sisteminin donanıma doğrudan erişebilen tek parçasıdır. İşletim sisteminin geri kalanı (masaüstü, dosya gezgini, terminal) aslında kernel'in üzerinde çalışan sıradan programlardır.

Program bir şey istediğinde sistem çağrısıyla kernel'e başvurur; donanıma sadece kernel dokunur.

Kullanıcı alanı ve çekirdek alanı

İşlemci iki farklı yetki seviyesinde çalışır:

Kullanıcı alanı (user space): Senin programların burada çalışır. Donanıma doğrudan erişemez, başka programların belleğini göremez. Bir hata yaparsa sadece kendisi çöker.
Çekirdek alanı (kernel space): Kernel burada çalışır. Her şeye erişim yetkisi vardır. Burada bir hata olursa tüm sistem çöker (Windows'taki mavi ekran bunun örneğidir).

Bu ayrım bir güvenlik duvarı gibidir. Bozuk ya da kötü niyetli bir program, diğer programlara ve donanıma zarar veremez.

Sistem çağrısı (system call)

Kullanıcı programı kernel'den bir şey istediğinde sistem çağrısı yapar. Bu, kernel'e açılan kontrollü bir kapıdır. Dosya açmak, ekrana yazmak, ağdan veri almak, yeni süreç başlatmak hep sistem çağrısıdır.

Python'da open("rapor.txt") yazdığında arka planda şu olur:

1-Python, işletim sisteminin open sistem çağrısını yapar.
2-İşlemci çekirdek moduna geçer, kontrol kernel'e geçer.
3-Kernel dosyanın var olup olmadığını ve iznin olup olmadığını kontrol eder.
4-Diskten gerekli bilgiyi alır, sonucu döndürür.
5-İşlemci kullanıcı moduna geri döner, programın çalışmaya devam eder.

Kernel'in görevleri
Görev	Ne yapar?
Süreç yönetimi	Programları başlatır, durdurur, hangisinin çalışacağına karar verir
Bellek yönetimi	Her programa bellek verir, birbirlerinin alanına girmelerini engeller
Aygıt sürücüleri	Klavye, disk, ekran kartı gibi donanımlarla konuşur
Dosya sistemi	Dosyaları diskte düzenler, okuma ve yazmayı yönetir
Güvenlik	Kullanıcı izinlerini ve erişim haklarını denetler
Kernel türleri
Monolitik kernel: Tüm görevler tek büyük programın içindedir. Hızlıdır ama bir parçadaki hata her şeyi etkileyebilir. Örnek: Linux.
Mikro kernel: Kernel çok küçük tutulur, sürücüler gibi parçalar dışarıda ayrı programlar olarak çalışır. Daha güvenlidir ama parçalar arası iletişim yüzünden daha yavaş olabilir. Örnek: MINIX, QNX.
Hibrit kernel: İkisinin karışımıdır. Örnek: Windows (NT kernel) ve macOS (XNU).
# 2. Süreç (process) ve iş parçacığı (thread)

Kısa cevap: süreç çalışan bir programdır ve kendine ait belleği vardır; thread ise bir sürecin içinde çalışan, o sürecin belleğini diğer thread'lerle paylaşan bir iş koludur.

Süreç (process)

Program, diskte duran bir dosyadır (örneğin market.py). Onu çalıştırdığında işletim sistemi bir süreç oluşturur. Aynı programı iki kez açarsan iki ayrı süreç olur.

Her sürecin kendine ait şunları vardır:

Bellek alanı: Kodu, değişkenleri, verileri. Başka süreçler bunu göremez.
Süreç kimliği (PID): İşletim sisteminin onu tanıdığı numara.
Açık dosyalar ve kaynaklar.
En az bir thread.

Windows'ta Görev Yöneticisi'ni açtığında listede gördüklerin süreçlerdir. Chrome'un her sekmeyi ayrı süreç olarak açmasının nedeni budur: bir sekme çökerse diğerleri etkilenmez.

Thread (iş parçacığı)

Thread, bir süreç içinde çalışan bağımsız bir iş koludur. Bir süreçte birden fazla thread olabilir ve hepsi aynı belleği paylaşır.

Bir kelime işlemci düşün. Bir thread senin yazdıklarını ekrana basar, bir başkası arka planda yazım denetimi yapar, bir üçüncüsü belgeyi otomatik kaydeder. Hepsi aynı belgeye (aynı belleğe) erişir.

Benzetme
Süreç = bir ev. Kendi duvarları, kendi mutfağı, kendi eşyaları var. Komşu ev senin buzdolabını açamaz.
Thread = evde yaşayan kişiler. Aynı mutfağı, aynı buzdolabını kullanırlar. İşbirliği kolaydır ama iki kişi aynı anda son yumurtayı almaya kalkarsa sorun çıkar.

Bu son durum programlamada yarış durumu (race condition) olarak bilinir. İki thread aynı değişkeni aynı anda değiştirmeye çalışırsa sonuç bozulabilir. Bunu önlemek için kilit (lock) gibi araçlar kullanılır.

Karşılaştırma
Özellik	Süreç	Thread
Bellek	Kendine ait, izole	Süreçteki diğer thread'lerle ortak
Oluşturma maliyeti	Yüksek (yeni bellek alanı gerekir)	Düşük
Birbiriyle iletişim	Zor (özel yöntemler gerekir: pipe, soket)	Kolay (aynı değişkenlere erişir)
Biri çökerse	Diğer süreçler etkilenmez	Tüm süreç çökebilir
Geçiş hızı	Daha yavaş	Daha hızlı
Ne zaman?	Güvenlik ve izolasyon gerekince	Paylaşılan veriyle paralel iş gerekince
Python örneği
python
import threading

def say(isim):
    for i in range(3):
        print(f"{isim}: {i}")

t1 = threading.Thread(target=say, args=("A",))
t2 = threading.Thread(target=say, args=("B",))
t1.start()
t2.start()
t1.join()
t2.join()

Bu kod tek bir süreç içinde iki thread başlatır. Çıktıda A ve B satırları karışık sırada görünebilir, çünkü hangisinin ne zaman çalışacağına işletim sistemi karar verir.

Not: Standart Python'da (CPython) GIL adlı bir kilit, aynı anda yalnızca bir thread'in Python kodu çalıştırmasına izin verir. Bu yüzden Python'da hesaplama ağırlıklı işleri hızlandırmak için genellikle multiprocessing (çoklu süreç) kullanılır. Thread'ler ise dosya okuma, ağdan veri bekleme gibi bekleme ağırlıklı işlerde faydalıdır.

# 3. Bellek yönetimi

Kısa cevap: işletim sistemi her sürece kendine ait sahte bir bellek alanı (sanal bellek) verir ve bu sahte adresleri arka planda gerçek RAM'deki yerlere eşler.

Neden gerekli?

Aynı anda onlarca program çalışıyor ve hepsi RAM kullanmak istiyor. İşletim sistemi şu üç sorunu çözmek zorunda:

İzolasyon: Bir program diğerinin verisini okuyamamalı veya bozamamalı.
Paylaştırma: Sınırlı RAM, programlar arasında adil şekilde bölünmeli.
Yetersizlik: RAM dolduğunda sistem çökmemeli.
Sanal bellek (virtual memory)

Her süreç, sanki bilgisayarda tek başınaymış ve kocaman bir bellek alanı varmış gibi davranır. Programın gördüğü adresler sanal adreslerdir. Gerçek RAM'deki konum (fiziksel adres) farklıdır.

Bu çeviriyi işlemcideki MMU (Bellek Yönetim Birimi) adlı donanım parçası yapar. Kernel de hangi sanal adresin hangi fiziksel adrese karşılık geldiğini tutan tabloları yönetir.

Benzetme: Her otel misafirine "oda 1" yazan bir anahtar verilir. Ama resepsiyon (MMU) bir misafirin "oda 1"ini gerçekte 304 numaraya, diğerininkini 512 numaraya yönlendirir. Misafirler birbirinin odasına asla giremez.

Sayfalama (paging)

Bellek, sayfa (page) denen küçük eşit parçalara bölünür, genellikle 4 KB. Kernel, sürecin sanal sayfalarını RAM'deki boş çerçevelere (frame) yerleştirir. Sayfaların RAM'de yan yana olması gerekmez, bu da belleği verimli kullanmayı sağlar.

Hangi sayfanın nerede olduğu sayfa tablosunda (page table) tutulur.

Swap ve sayfa hatası (page fault)

RAM dolunca kernel, uzun süredir kullanılmayan sayfaları diske yazar. Diskteki bu alana swap (Windows'ta sayfa dosyası, pagefile) denir.

Program, diske taşınmış bir sayfaya erişmeye çalışırsa sayfa hatası (page fault) oluşur. Bu bir hata değil, normal bir olaydır: kernel devreye girer, sayfayı diskten RAM'e geri getirir ve program kaldığı yerden devam eder.

Ama disk RAM'den binlerce kat yavaştır. Sistem sürekli swap yapmak zorunda kalırsa bilgisayar ciddi şekilde yavaşlar. Buna thrashing denir. Çok fazla sekme açık olduğunda bilgisayarın donması genellikle bundandır.

Bir sürecin bellek düzeni
Bölüm	İçinde ne var?
Kod (text)	Programın makine kodu, sadece okunur
Veri (data)	Global değişkenler
Heap	Çalışma sırasında oluşturulan nesneler. İhtiyaç oldukça büyür
Stack	Fonksiyon çağrıları, yerel değişkenler, dönüş adresleri. Her thread'in kendi stack'i vardır

Python'da sepet = {} yazdığında sözlük nesnesi heap'te oluşur. Bir fonksiyon çağrıldığında içindeki yerel değişkenler ise stack'te durur ve fonksiyon bitince silinir.

Sonsuz bir özyinelemeli fonksiyon yazarsan stack dolar ve stack overflow hatası alırsın. Python bunu RecursionError olarak gösterir.

Bellek sızıntısı

Program belleği alıp işi bitince geri vermezse kullandığı bellek sürekli büyür. Buna bellek sızıntısı (memory leak) denir. Python gibi dillerde çöp toplayıcı (garbage collector) kullanılmayan nesneleri otomatik temizler. C gibi dillerde bunu programcı kendisi yapmak zorundadır.

# 4. CPU zamanlayıcıları (scheduler)

Kısa cevap: zamanlayıcı, kernel'in "şu an işlemcide hangi thread çalışsın ve ne kadar süre?" sorusuna karar veren parçasıdır.

Neden gerekli?

Bilgisayarında aynı anda yüzlerce thread çalışıyor ama işlemcinin belki 8 çekirdeği var. Her çekirdek aynı anda yalnızca bir thread çalıştırabilir.

Çözüm: Zamanlayıcı, thread'lere sırayla çok kısa süreler (milisaniyeler) verir. Bu geçişler o kadar hızlıdır ki her şey aynı anda çalışıyormuş gibi görünür. Buna eşzamanlılık (concurrency) denir.

Bir thread'in durumları:

Hazır (ready): Çalışmaya hazır, sırasını bekliyor.
Çalışıyor (running): Şu an işlemcide.
Bekliyor (blocked): Bir şey bekliyor: klavye girişi, disk okuma, ağ cevabı. İşlemciye ihtiyacı yok.

Bir program input("Seçiminiz: ") satırında beklerken bekliyor durumundadır ve hiç işlemci harcamaz. Sen Enter'a basınca kernel onu hazır durumuna alır, zamanlayıcı da sırası gelince çalıştırır.

Bağlam değiştirme (context switch)

Zamanlayıcı bir thread'i durdurup diğerine geçerken, durdurulan thread'in o anki durumunu (işlemci register'ları, hangi satırda kaldığı) kaydeder. Sonra yeni thread'in kaydedilmiş durumunu yükler. Buna bağlam değiştirme denir.

Bu işlem bedava değildir. Çok sık yapılırsa işlemci zamanının bir kısmı asıl iş yerine geçiş yapmaya harcanır.

Temel zamanlama algoritmaları
Algoritma	Nasıl çalışır?	Artı	Eksi
FCFS (İlk gelen ilk çalışır)	Sıraya kim önce girdiyse o çalışır, bitene kadar	Çok basit	Uzun bir iş, arkasındaki kısa işleri bekletir
SJF (En kısa iş önce)	Süresi en kısa olan iş önce çalışır	Ortalama bekleme süresi en düşük	İşin süresini önceden bilmek zor; uzun işler sıra bulamayabilir
Round Robin (Sırayla)	Her işe sabit bir süre dilimi verilir, süre bitince sıranın sonuna geçer	Adil, her iş düzenli sıra alır	Süre dilimi çok kısaysa bağlam değiştirme maliyeti artar
Öncelik tabanlı	Önceliği yüksek olan önce çalışır	Önemli işler hızlı yapılır	Düşük öncelikli işler sonsuza kadar bekleyebilir (açlık, starvation)

Örnek: Market kasasında FCFS'de herkes sırayla geçer, ama önündeki kişinin arabası doluysa iki ürünle bekleyen sen de bekler durursun. SJF, "az ürünlüler kasası" gibidir. Round Robin ise kasiyerin her müşteriden sırayla 5 ürün okutup sonrakine geçmesine benzer.

Gerçek işletim sistemleri ne kullanır?

Gerçek sistemler bu fikirleri karıştırır. Genel prensip şudur: etkileşimli işler (fare tıklaması, klavye) hızlı cevap almalı, arka plan işleri (dosya sıkıştırma, yedekleme) kalan zamanı kullanmalı.

Linux: Uzun yıllar CFS (Completely Fair Scheduler) kullandı. Bu, her thread'in ne kadar işlemci zamanı aldığını takip edip en az alana öncelik verir. Daha yeni sürümlerde yerini EEVDF adlı benzer mantıkta bir zamanlayıcı aldı.
Windows: Önceliğe dayalı bir sistem kullanır. Ön plandaki pencere ve kullanıcı etkileşimi bekleyen thread'ler geçici olarak öncelik artışı alır.
Önleyici (preemptive) zamanlama

Modern işletim sistemleri önleyicidir. Yani kernel, bir thread işini bitirmese bile süresi dolunca onu zorla durdurabilir. Böylece kötü yazılmış bir program sonsuz döngüye girse bile tüm bilgisayarı kilitleyemez. Diğer programlar çalışmaya devam eder.

Özet: Bir yazılımcı için neden önemli?

Yazdığın her kod bu dört mekanizmanın içinde çalışır. Bunları bilmek, karşılaştığın sorunların nedenini anlamanı sağlar.

Kavram	Bir cümlede	Yazılımcı olarak nerede karşına çıkar?
Kernel	Donanıma erişen tek yetkili parça	Dosya, ağ, ekran işlemlerinin neden "yavaş" olabildiğini anlamak; izin hataları
Süreç / thread	Süreç izole bir program, thread onun içindeki paylaşımlı iş kolu	Programı paralel çalıştırma; yarış durumu hataları
Bellek yönetimi	Her sürece izole sanal bellek, arka planda gerçek RAM'e eşleme	Bellek sızıntısı, programın RAM tüketimi, stack overflow
CPU zamanlayıcısı	Hangi thread'in ne zaman çalışacağına karar verir	Thread çıktılarının neden karışık sırada geldiği, programın neden takıldığı
