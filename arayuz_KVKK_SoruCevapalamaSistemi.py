from sentence_transformers import SentenceTransformer, util
import pandas as pd

model = SentenceTransformer('sentence-transformers/clip-ViT-B-32-multilingual-v1')

def onIslemler(cumle):
    
    # Tüm büyük harfler küçük harflere çevriliyor
    cumle = cumle.lower()

    # Noklama işaretleri kaldırılıyor
    for karakter in cumle:
        if not(karakter.isalnum or " "):
            if not(karakter in "çğıöşü"):
                cumle.replace(karakter,"")
    return str(cumle)

def sorulariDosyadanOkuveListeOlarakDondur():
    gecici = []
    for i in range(100):
        gecici.append([])
    df = pd.read_csv('KVKK_100_SORU_CEVAP.txt',sep="\t")
    for i in range(100):
        gecici[i].append(df.to_numpy()[i][1])       #Soru
        gecici[i].append(df.to_numpy()[i][2])       #Cevabı
    return(gecici)

    # Bilinen kısaltmalar açılıyor
    while "kvkk" in cumle:
        cumle.replace("kvkk","kişisel verilerin korunumu kanunu")

# Kullanıcı tarafından veri girişi yapılır.
#soru = input("Sorunuzu giriniz:")
soru="Veri Sorumlusunun Meşru Menfaatini Tespit Etmek İçin Göz Önünde Bulundurulması Gereken Hususlar Nelerdir?"

# Girilen soru ön işlemlerden geçirilir.
soru = onIslemler(soru)

# Ön işlemden geçirilen soru encode ediliyor.
encodedSoru = model.encode(soru)

# Ön işlemden geçirilen ve encode edilen soru ile
# hazır soruların encode edilmiş hallerinin benzerlik puanları bir listeye kaydediliyor
benzerlikListesi = []
soruListesi = sorulariDosyadanOkuveListeOlarakDondur()
for i in range(100):
    benzerlikListesi.append(util.cos_sim(encodedSoru, model.encode(soruListesi[i][0])))

for i in range(100):
    print(i+1,". ",benzerlikListesi[i],"\t",soruListesi[i][0])

# Benzerlik puanı en büyük 3 soru döndürülür
for i in range(3):
    bul = benzerlikListesi.index(max(benzerlikListesi))
    print(i,". en yakın soru: ",soruListesi[bul][0])
    print(i,". en yakın soruya cevap: ",soruListesi[bul][1])
    benzerlikListesi[bul]=-2