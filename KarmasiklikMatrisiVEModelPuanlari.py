# İlgili kütüphaneleri çalışma ortamınıza yükleyiniz
from sentence_transformers import SentenceTransformer, util
import pandas as pd
import random

modelListesi = [\
    "sentence-transformers/paraphrase-xlm-r-multilingual-v1",\
    "sentence-transformers/paraphrase-MiniLM-L12-v2",\
    "sentence-transformers/paraphrase-MiniLM-L3-v2",\
    "sentence-transformers/clip-ViT-B-32-multilingual-v1",\
    "sentence-transformers/distiluse-base-multilingual-cased-v2",\
    "sentence-transformers/quora-distilbert-multilingual",\
    "sentence-transformers/msmarco-distilbert-base-v4",\
    "flax-sentence-embeddings/multi-qa_v1-distilbert-cls_dot",\
    "flax-sentence-embeddings/all_datasets_v3_distilroberta-base",\
    "flax-sentence-embeddings/multi-qa_v1-MiniLM-L6-mean_cos",\
    "sentence-transformers/stsb-xlm-r-multilingual"]

turkAlfabe = "abcçdefgğhıijklmnoöprsştuüvyz"

# Bu fonksiyon KVKK için oluşturduğumuz TSV dosyasından soru ve cevapları okuyor.
def sorulariDosyadanOkuveListeOlarakDondur():
    gecici = []
    for i in range(100):
        gecici.append([])
    df = pd.read_csv('KVKK_100_SORU_CEVAP.txt',sep="\t")
    for i in range(100):
        gecici[i].append(df.to_numpy()[i][1])       #Soru
        gecici[i].append(df.to_numpy()[i][2])       #Cevabı
    return(gecici)

def testSorusuUret(testCinsi,gonderilenSoru):
    random.seed(61)

    if testCinsi==11: # Aynı soru 1 harfi değişik
        kelime = str(gonderilenSoru)
        kelime = kelime.replace(gonderilenSoru[random.randint(0,len(gonderilenSoru)-1)],turkAlfabe[random.randint(0,28)],1) # Sadece 1 kez
        return kelime

    if testCinsi==12: # Aynı soru 2 harfi değişik
        kelime = str(gonderilenSoru)
        kelime = kelime.replace(gonderilenSoru[random.randint(0,(len(gonderilenSoru)//2))],turkAlfabe[random.randint(0,28)],1) # Sadece 1 kez
        kelime = kelime.replace(gonderilenSoru[random.randint((len(gonderilenSoru)//2),len(gonderilenSoru)-1)],turkAlfabe[random.randint(0,28)],1) # Sadece 1 kez
        return kelime

    if testCinsi==13: # Aynı soru 3 harfi değişik
        kelime = str(gonderilenSoru)
        kelime = kelime.replace(gonderilenSoru[random.randint(0,(len(gonderilenSoru)//3))],turkAlfabe[random.randint(0,28)],1) # Sadece 1 kez
        kelime = kelime.replace(gonderilenSoru[random.randint((len(gonderilenSoru)//3),(len(gonderilenSoru)//3)*2)],turkAlfabe[random.randint(0,28)],1) # Sadece 1 kez
        kelime = kelime.replace(gonderilenSoru[random.randint((len(gonderilenSoru)//3)*2,len(gonderilenSoru)-1)],turkAlfabe[random.randint(0,28)],1) # Sadece 1 kez
        return kelime

    if testCinsi==21:# Aynı soru rastgele bir kelime eklenmiş
        list = []
        list = str(gonderilenSoru).split(" ")
        list.insert(random.randint(0,len(list)-1),str(soruListesi[random.randint(0,100)][1]).split(" ")[random.randint(0,(len(list)-1))])
        return " ".join(list)

    if testCinsi==22:# Aynı soru rastgele iki kelime eklenmiş
        list = []
        list = str(gonderilenSoru).split(" ")
        list.insert(random.randint(0,len(list)//2),str(soruListesi[random.randint(0,100)][1]).split(" ")[random.randint(0,(len(list)-1))])
        list.insert(random.randint(len(list)//2,len(list)-1),str(soruListesi[random.randint(0,100)][1]).split(" ")[random.randint(0,(len(list)-1))])
        return " ".join(list)

    if testCinsi==23:# Aynı soru rastgele üç kelime eklenmiş
        list = []
        list = str(gonderilenSoru).split(" ")
        list.insert(random.randint(0,len(list)//3),str(soruListesi[random.randint(0,100)][1]).split(" ")[random.randint(0,(len(list)-1))])
        list.insert(random.randint(len(list)//3,len(list)*2//3),str(soruListesi[random.randint(0,100)][1]).split(" ")[random.randint(0,(len(list)-1))])
        list.insert(random.randint(len(list)*2//3,len(list)-1),str(soruListesi[random.randint(0,100)][1]).split(" ")[random.randint(0,(len(list)-1))])
        return " ".join(list)

    if testCinsi==31:# Aynı soru rastgele bir kelime çıkarılmış
        list = []
        list = str(gonderilenSoru).split(" ")
        list.pop(random.randint(0,(len(list)-1)))
        return " ".join(list)

    if testCinsi==32:# Aynı soru rastgele iki kelime çıkarılmış
        list = []
        list = str(gonderilenSoru).split(" ")
        if len(list)>1:
            list.pop(random.randint(0,(len(list)-1)))
        if len(list)>1:
            list.pop(random.randint(0,(len(list)-1)))
        return " ".join(list)

    if testCinsi==33:# Aynı soru rastgele üç kelime çıkarılmış
        list = []
        list = str(gonderilenSoru).split(" ")
        if len(list)>1:
            list.pop(random.randint(0,(len(list)-1)))
        if len(list)>1:
            list.pop(random.randint(0,(len(list)-1)))
        if len(list)>1:
            list.pop(random.randint(0,(len(list)-1)))
        return " ".join(list)

    return "Test Cinsi Hatalıdır!"+str(testCinsi)

print("Lütfen bekleyiniz ön hesaplamalar yapılıyor ve ardından KVKK Soru Cevap Sistemi açılacaktır!")
# Her seferinde çalırılıp aynı hesaplamaları yapmaması için soru listesini PUBLIC oluşturuyoruz.
soruListesi = sorulariDosyadanOkuveListeOlarakDondur()

# Her seferinde çalırılıp aynı encode işlemini yapmaması için hazır encode soru listesini PUBLIC oluşturuyoruz.
hazirEncodeSorular = []
sayBakalim = 0
for m in modelListesi:
    model = SentenceTransformer(m)
    # Soru listesindeli tüm soruları onIslemden geciriyoruz.
    hazirEncodeSorular = []
    for i in range(100):
        soru = soruListesi[i][0]
        soru = model.encode(soru)
        hazirEncodeSorular.append(soru)

    def tahminDondur(gonderilenSoru):
        benzerlikListesi = []
        for i in range(100):
            benzerlikListesi.append(util.cos_sim(model.encode(gonderilenSoru), hazirEncodeSorular[i]))
        bul = benzerlikListesi.index(max(benzerlikListesi))
        return bul

    print("Model: ",m,"Başladı...")
    dogruluk = [0,0,0,0,0,0,0,0,0]
    testTuru = [11,12,13,21,22,23,31,32,33]
    for testNo in range(100):
        for TT in range(9):
            soru = testSorusuUret(testTuru[TT],soruListesi[testNo][0])
            if (testNo == tahminDondur(soru)):
                dogruluk[TT]+=1
            sayBakalim += 1
            print(sayBakalim)
    for TT in range(9):
        with open("KarmasiklikMatrisiVEModelPuanlari"+str(TT)+".tsv",'a',encoding = 'utf-8') as dosya:
            dosya.write(m+"\t"+str(TT)+"\t"+str(dogruluk[TT]/900)+"\n")
    print("Model: ",m,"Bitti...")
