# Model Stres Testi
import torch
from sentence_transformers import SentenceTransformer, util
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import random
from tqdm import tqdm

def sorulariDosyadanOkuveListeOlarakDondur():
    gecici = []
    for i in range(100):
        gecici.append([])
    df = pd.read_csv('KVKK_100_SORU_CEVAP.txt',sep="\t")
    for i in range(100):
        gecici[i].append(df.to_numpy()[i][1])       #Soru
        gecici[i].append(df.to_numpy()[i][2])       #Cevabı
    return(gecici)

def testSoruListesiUret(sayi,testCinsi):

    # sayi      -> Rastgeleliği sabitliyor.
    # testCinsi -> 11 (sadece 1 harf değişmiş)
    # testCinsi -> 21 (sadece 1 kelime çıkartılmış)
    # testCinsi -> 31 (sadece 1 kelime eklenmiş)
    # testCinsi -> 12 (sadece 2 harf değişmiş)
    # testCinsi -> 22 (sadece 2 kelime çıkartılmış)
    # testCinsi -> 32 (sadece 2 kelime eklenmiş)
    # testCinsi -> 13 (sadece 3 harf değişmiş)
    # testCinsi -> 23 (sadece 3 kelime çıkartılmış)
    # testCinsi -> 33 (sadece 3 kelime eklenmiş)

    gecici = []
    cevaplar = []
    for i in range(100):
        gecici.append([])
        cevaplar.append([])
    df = pd.read_csv('KVKK_100_SORU_CEVAP.txt',sep="\t")
    for i in range(100):
        gecici[i].append(df.to_numpy()[i][1])       #Soru
        cevaplar[i].append(df.to_numpy()[i][2])       #Cevap

    uretilenSorular = []
    random.seed(sayi)
    turkAlfabe = "abcçdefgğhıijklmnoöprsştuüvyz"

    if testCinsi==11:
        for cogalt in range(3): # Test soru sayısını çoğaltıyoruz (100 x 3)
            for oge in gecici:
                kelime = str(oge[0])
                kelime = kelime.replace(oge[0][random.randint(0,len(oge[0])-1)],turkAlfabe[random.randint(0,28)],1) # Sadece 1 kez
                uretilenSorular.append(kelime) # Aynı soru 1 harfi değişik
        return uretilenSorular

    if testCinsi==12:
        for cogalt in range(3): # Test soru sayısını çoğaltıyoruz (100 x 3)
            for oge in gecici:
                kelime = str(oge[0])
                kelime = kelime.replace(oge[0][random.randint(0,(len(oge[0])//2))],turkAlfabe[random.randint(0,28)],1) # 1. kez
                kelime = kelime.replace(oge[0][random.randint((len(oge[0])//2),len(oge[0])-1)],turkAlfabe[random.randint(0,28)],1) # 2. kez
                uretilenSorular.append(kelime) # Aynı soru 2 harfi değişik
        return uretilenSorular

    if testCinsi==13:
        for cogalt in range(3): # Test soru sayısını çoğaltıyoruz (100 x 3)
            for oge in gecici:
                kelime = str(oge[0])
                kelime = kelime.replace(oge[0][random.randint(0,len(oge[0])//3)],turkAlfabe[random.randint(0,28)],1) # 1. kez
                kelime = kelime.replace(oge[0][random.randint(len(oge[0])//3,len(oge[0])*2//3)],turkAlfabe[random.randint(0,28)],1) # 2. kez
                kelime = kelime.replace(oge[0][random.randint(len(oge[0])*2//3,len(oge[0])-1)],turkAlfabe[random.randint(0,28)],1) # 3. kez
                uretilenSorular.append(kelime) # Aynı soru 3 harfi değişik
        return uretilenSorular

    if testCinsi==21:
        list = []
        for cogalt in range(3): # Test soru sayısını çoğaltıyoruz (100 x 3)
            for sayi in range(100):
                list = str(gecici[sayi][0]).split(" ")
                list.insert(random.randint(0,len(list)-1),str(cevaplar[sayi][0]).split(" ")[random.randint(0,len(list)-1)])
                uretilenSorular.append(" ".join(list)) # Aynı soru rastgele bir kelime eklenmiş
                list.clear()
        return uretilenSorular

    if testCinsi==22:
        list = []
        for cogalt in range(3): # Test soru sayısını çoğaltıyoruz (100 x 3)
            for sayi in range(100):
                list = str(gecici[sayi][0]).split(" ")
                list.insert(random.randint(0,len(list)//2),str(cevaplar[sayi][0]).split(" ")[random.randint(0,len(list)-1)])
                list.insert(random.randint(len(list)//2,len(list)-1),str(cevaplar[sayi][0]).split(" ")[random.randint(0,len(list)-1)])
                uretilenSorular.append(" ".join(list)) # Aynı soru rastgele iki kelime eklenmiş
                list.clear()
        return uretilenSorular

    if testCinsi==23:
        list = []
        for cogalt in range(3): # Test soru sayısını çoğaltıyoruz (100 x 3)
            for sayi in range(100):
                list = str(gecici[sayi][0]).split(" ")
                list.insert(random.randint(0,len(list)//3),str(cevaplar[sayi][0]).split(" ")[random.randint(0,len(list)-1)])
                list.insert(random.randint(len(list)//3,len(list)*2//3),str(cevaplar[sayi][0]).split(" ")[random.randint(0,len(list)-1)])
                list.insert(random.randint(len(list)*2//3,len(list)-1),str(cevaplar[sayi][0]).split(" ")[random.randint(0,len(list)-1)])
                uretilenSorular.append(" ".join(list)) # Aynı soru rastgele üç kelime eklenmiş
                list.clear()
        return uretilenSorular

    if testCinsi==31:
        list = []
        for cogalt in range(3): # Test soru sayısını çoğaltıyoruz (100 x 3)
            for sayi in range(100):
                list = str(gecici[sayi][0]).split(" ")
                list.pop(random.randint(0,len(list)-1))
                uretilenSorular.append(" ".join(list)) # Aynı soru rastgele bir kelime çıkarılmış
                list.clear()
        return uretilenSorular

    if testCinsi==32:
        list = []
        for cogalt in range(3): # Test soru sayısını çoğaltıyoruz (100 x 3)
            for sayi in range(100):
                list = str(gecici[sayi][0]).split(" ")
                if len(list)>1:
                    list.pop(random.randint(0,len(list)-1))
                if len(list)>1:
                    list.pop(random.randint(0,len(list)-1))
                    uretilenSorular.append(" ".join(list)) # Aynı soru rastgele en fazla iki kelime çıkarılmış
                list.clear()
        return uretilenSorular

    if testCinsi==33:
        list = []
        for cogalt in range(3): # Test soru sayısını çoğaltıyoruz (100 x 3)
            for sayi in range(100):
                list = str(gecici[sayi][0]).split(" ")
                if len(list)>1:
                    list.pop(random.randint(0,len(list)-1))
                if len(list)>1:
                    list.pop(random.randint(0,len(list)-1))
                if len(list)>1:
                    list.pop(random.randint(0,len(list)-1))
                    uretilenSorular.append(" ".join(list)) # Aynı soru rastgele en fazla üç kelime çıkarılmış
                list.clear()
        return uretilenSorular

    return(uretilenSorular)

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

# device = torch.device("cuda:0") if torch.cuda.is_available() else torch.device("cpu") 

soruListesi = sorulariDosyadanOkuveListeOlarakDondur()  # Bizim 100 soru
testTurleri = [33]

for TT in testTurleri:
    testSorulari = []
    testSorulari = testSoruListesiUret(61,TT)
    with open("stresTestiSonuclari"+str(TT)+".tsv",'w',encoding = 'utf-8') as dosya:
        say = 0
        dosya.write("HS"+"\t"+"TS"+"\t"+"M"+"\t"+"BO"+"\n")

        # HS - KVKK ile ilgili Hazır Soru
        # TS - Test Sorumuz
        # M - Test edilen modelimiz
        # BO - Benzerlik Oranı

        benzerlikListesi = []
        performansCubugu = tqdm(total = 6600, bar_format="Test Türü - "+str(TT)+"- Modelin egitim durumu:[{bar:50}]\t[{n_fmt}/{total_fmt}]")
        for m in modelListesi:
            model = SentenceTransformer(m)
    #        torch.cuda.empty_cache()
    #        model = model.to(device)
            for hazirKVKKSorusu in soruListesi[0]:
                for soru in testSorulari:
                    benzerlik = float(util.cos_sim(model.encode(soru),model.encode(hazirKVKKSorusu)))
                    benzerlikListesi.append(benzerlik)
                    dosya.write(hazirKVKKSorusu+"\t"+soru+"\t"+m+"\t"+str(benzerlik)+"\n")
                    performansCubugu.update(1)

# GPU Kullanmak için gerekli üç satır yukarıda mevcuttur. Burası açıklamadır.
# device = torch.device("cuda:0") if torch.cuda.is_available() else torch.device("cpu") 
# GPU kullanmak için .to(device) yazmanız yeterlidir.
# Örneğin, model = model.to(device)

# Bir önceki modeli temizlemek için
# torch.cuda.empty_cache()
# komutunu unutmayın!!!

# Daha detaylı kullanım için aşağıdaki torch komutları incelenebilir. 
# if torch.cuda.is_available():
    # torch.cuda.current_device()
    # torch.cuda.device(0)
    # torch.cuda.device_count()
    # torch.cuda.get_device_name(0)
