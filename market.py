# ==========================================
# AKILLI MARKET YONETIM SISTEMI
# ==========================================

urunler ={
    101: {"ad": "Süt", "fiyat": 42, "stok": 20},
    102: {"ad": "Pirinç", "fiyat": 95, "stok": 15},
    103: {"ad": "Peynir", "fiyat": 175, "stok": 10},
    104: {"ad": "Kahve", "fiyat": 210, "stok": 8},
    105: {"ad": "Zeytinyağı", "fiyat": 320, "stok": 12},
    106: {"ad": "Makarna", "fiyat": 48, "stok": 25},
    107: {"ad": "Çay", "fiyat":55, "stok": 3},
    108: {"ad": "Ekmek","fiyat":13,"stok":0}
}

sepet = {}


rapor = {
    "islem_sayisi":0,
    "toplam_satis_adet":0,
    "ciro":0.0,    
    "urun_satislari": {},
}

# İndirim
KAMPANYA_KURALLARI = [
    (1000, 10),   # 1000 TL ve uzeri -> %10
    (500, 5),     # 500 TL ve uzeri  -> %5
]

UYELIK_INDIRIM_ORANI = 5 

# Pozitif sayı kontrolü

def pozitif_sayi_al(mesaj):
    while True:
        veri = input(mesaj).strip()

        if veri.isdigit() and int(veri) > 0:
            return int(veri)

        print("Lütfen pozitif bir tam sayı giriniz.")

 
def evet_mi(mesaj):
    #Kullanicidan evet/hayır cevabi alir. Evet ise True dondurur
    while True:
        cevap = input(mesaj).strip().lower()
        if cevap in ("e", "evet"):
            return True
        elif cevap in ("h", "hayir", "hayır"):
            return False
        print("Lütfen 'e' veya 'h' giriniz.")

#-----------------Ürünler--------------
def urunleri_listele(urunler):
    print("\n========== ÜRÜN LİSTESİ ==========")
    for kod, bilgi in urunler.items():
        ad = bilgi["ad"]
        fiyat = bilgi["fiyat"]
        stok = bilgi["stok"]

        if stok == 0:
            durum = "STOKTA YOK"
        else:
            durum = f"Stok: {stok}"

        print(f"{kod} - {ad:<12} {fiyat:>5} TL  | {durum}")
    print("==================================")

# ------------Sepete Ekleme--------------
def sepete_ekle(urunler, sepet):
    kod = pozitif_sayi_al("Ürün kodu: ")
 
    if kod not in urunler:
        print("Bu kodda bir ürün bulunamadı.")
        return
 
    urun = urunler[kod]
 
    if urun["stok"] == 0:
        print(f"{urun['ad']} şu anda STOKTA YOK.")
        return
 
    adet = pozitif_sayi_al("Kaç adet: ")
 
    sepetteki_adet = sepet.get(kod, 0)
    yeni_toplam = sepetteki_adet + adet
 
    if yeni_toplam > urun["stok"]:
        eklenebilir = urun["stok"] - sepetteki_adet
        print(f"Yetersiz stok! Stok: {urun['stok']}, sepetinizde: {sepetteki_adet}.")
        print(f"En fazla {eklenebilir} adet daha ekleyebilirsiniz.")
        return
 
    sepet[kod] = yeni_toplam
    print(f"\n{adet} adet {urun['ad']} sepete eklendi.")
 
 
# ---------- Sepeti görüntüleme  ----------
 
def sepeti_goster(urunler, sepet):
    if not sepet:
        print("\nSepetiniz boş.")
        return
 
    print("\nSepetiniz:")
    for kod, adet in sepet.items():
        urun = urunler[kod]
        tutar = urun["fiyat"] * adet
        print(f"{kod} - {urun['ad']}: {adet} adet  ({tutar} TL)")
    print(f"Ara toplam: {ara_toplam_hesapla(urunler, sepet):.2f} TL")
 
 
# ---------- Sepetten Çıkarma  ----------
 
def sepetten_cikar(urunler, sepet):
    if not sepet:
        print("\nSepetiniz boş, çıkarılacak ürün yok.")
        return
 
    sepeti_goster(urunler, sepet)
 
    kod = pozitif_sayi_al("\nÇıkarılacak ürün kodu: ")
 
    if kod not in sepet:
        print("Bu ürün sepetinizde yok.")
        return
 
    miktar = pozitif_sayi_al("Çıkarılacak miktar: ")
    ad = urunler[kod]["ad"]
 
    if miktar > sepet[kod]:
        print(f"Sepetinizde sadece {sepet[kod]} adet {ad} var.")
        return
 
    if miktar == sepet[kod]:
        del sepet[kod]
        print(f"\n{ad} sepetten tamamen çıkarıldı.")
    else:
        sepet[kod] -= miktar
        print(f"\n{ad} ürününden {miktar} adet çıkarıldı.")
 
    print("\nYeni sepet:")
    if sepet:
        for k, a in sepet.items():
            print(f"{k} - {urunler[k]['ad']}: {a} adet")
    else:
        print("Sepetiniz boş.")
 
 
# ---------- Tutar ve İndirim  ----------
 
def ara_toplam_hesapla(urunler, sepet):
    toplam = 0
    for kod, adet in sepet.items():
        toplam += urunler[kod]["fiyat"] * adet
    return toplam
 
 
def kampanya_orani_bul(ara_toplam):
    for alt_sinir, oran in KAMPANYA_KURALLARI:
        if ara_toplam >= alt_sinir:
            return oran
    return 0
 
 
def odeme_hesapla(ara_toplam, uye_mi):
    """Kampanya indirimi once, uyelik indirimi kalan tutar uzerinden uygulanir."""
    kampanya_orani = kampanya_orani_bul(ara_toplam)
    kampanya_indirimi = ara_toplam * kampanya_orani / 100
 
    kalan = ara_toplam - kampanya_indirimi
 
    if uye_mi:
        uyelik_indirimi = kalan * UYELIK_INDIRIM_ORANI / 100
    else:
        uyelik_indirimi = 0
 
    odenecek = kalan - uyelik_indirimi
    return kampanya_orani, kampanya_indirimi, uyelik_indirimi, odenecek
 
 
# ---------- Ödeme ve Stok güncelleme  ----------
 
def odeme_yap(urunler, sepet, rapor):
    if not sepet:
        print("\nSepetiniz boş, ödeme yapılamaz.")
        return
 
    sepeti_goster(urunler, sepet)
 
    ara_toplam = ara_toplam_hesapla(urunler, sepet)
    uye_mi = evet_mi("\nÜye misiniz? (e/h): ")
 
    kampanya_orani, kampanya_ind, uyelik_ind, odenecek = odeme_hesapla(ara_toplam, uye_mi)
 
    print("\n----------- ÖDEME ÖZETİ -----------")
    print(f"Ara toplam              : {ara_toplam:>10.2f} TL")
    if kampanya_orani > 0:
        print(f"Kampanya indirimi (%{kampanya_orani:<2}) : {-kampanya_ind:>10.2f} TL")
    if uye_mi:
        print(f"Üyelik indirimi (%{UYELIK_INDIRIM_ORANI:<2})   : {-uyelik_ind:>10.2f} TL")
    print(f"Ödenecek tutar          : {odenecek:>10.2f} TL")
    print("-----------------------------------")
 
    if not evet_mi("Ödemeyi onaylıyor musunuz? (e/h): "):
        print("Ödeme iptal edildi. Sepetiniz ve stoklar değişmedi.")
        return
 
    # Stoklari dus ve rapora isle
    for kod, adet in sepet.items():
        urunler[kod]["stok"] -= adet
        rapor["toplam_satis_adet"] += adet
        rapor["urun_satislari"][kod] = rapor["urun_satislari"].get(kod, 0) + adet
 
    rapor["islem_sayisi"] += 1
    rapor["ciro"] += odenecek
 
    sepet.clear()
    print("Ödeme başarıyla tamamlandı. Teşekkür ederiz!")
 
 
# ---------- Satış raporu ----------
 
def rapor_goster(urunler, rapor):
    print("\n========== GÜNLÜK SATIŞ RAPORU ==========")
    print(f"Toplam Satış İşlemi : {rapor['islem_sayisi']}")
    print(f"Toplam Ciro         : {rapor['ciro']:.2f} TL")
    print(f"Satılan Ürün        : {rapor['toplam_satis_adet']} adet")
 
    satislar = rapor["urun_satislari"]
    if satislar:
        en_cok_kod = max(satislar, key=satislar.get)
        print(f"En Çok Satılan      : {urunler[en_cok_kod]['ad']} ({satislar[en_cok_kod]} adet)")
    else:
        print("En Çok Satılan      : -")
 
    dusuk_stoklar = []
    for kod, bilgi in urunler.items():
        if bilgi["stok"] <= 3:
            dusuk_stoklar.append(f"{bilgi['ad']} - {bilgi['stok']} adet")
 
    if dusuk_stoklar:
        print("Düşük Stoklu Ürünler:")
        for satir in dusuk_stoklar:
            print(f"   {satir}")
    else:
        print("Düşük Stoklu Ürünler: Yok")
    print("=========================================")
 

# Menu
def menu():
    while True:
        print("\n===== MARKET YÖNETİM SİSTEMİ =====")
        print("1. Ürünleri Listele")
        print("2. Sepete Ürün Ekle")
        print("3. Sepetten Ürün Çıkar")
        print("4. Sepeti Görüntüle")
        print("5. Ödeme Yap")
        print("6. Satış Raporunu Gör")
        print("7. Çıkış")

        secim = input("Seçiminiz: ").strip()

        if secim == "1":
            urunleri_listele(urunler)
        elif secim == "2":
            sepete_ekle(urunler, sepet)
        elif secim == "3":
            sepetten_cikar(urunler, sepet)
        elif secim == "4":
            sepeti_goster(urunler, sepet)
        elif secim == "5":
            odeme_yap(urunler, sepet, rapor)
        elif secim == "6":
            rapor_goster(urunler, rapor)
        elif secim == "7":
            print("Programdan çıkılıyor. İyi günler!")
            break
        else:
            print("Geçersiz seçim! Lütfen 1-7 arasında bir sayı girin.")
            

menu()
