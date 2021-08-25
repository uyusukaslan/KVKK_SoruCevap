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

def testSoruListesiUret(sayi):
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
    for oge in gecici:
        kelime = str(oge[0])
        kelime = kelime.replace(oge[0][random.randint(0,len(oge[0])-1)],turkAlfabe[random.randint(0,28)],1) # Sadece 1 kez
        uretilenSorular.append(kelime) # Aynı soru 1 harfi değişik

    list = []
    for sayi in range(100):
        list = str(gecici[sayi][0]).split(" ")
        list.insert(random.randint(0,len(list)-1),str(cevaplar[sayi][0]).split(" ")[random.randint(0,len(list)-1)])
        uretilenSorular.append(" ".join(list)) # Aynı soru rastgele bir kelime eklenmiş
        list.clear()

    for sayi in range(100):
        list = str(gecici[sayi][0]).split(" ")
        list.pop(random.randint(0,len(list)-1))
        uretilenSorular.append(" ".join(list)) # Aynı soru rastgele bir kelime çıkarılmış
        list.clear()

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


soruListesi = sorulariDosyadanOkuveListeOlarakDondur()  # Bizim 100 soru
testSorulari = testSoruListesiUret(61) # 300 civarı değiştirilmiş soru

# device = torch.device("cuda:0") if torch.cuda.is_available() else torch.device("cpu") 

with open("stresTestiSonuclari.csv",'w',encoding = 'utf-8') as dosya:
    dosya.write("KVKK ile ilgili Hazır Soru"+","+"Test Sorumuz (1 - 100 Bir harf değişik | 101 - 200 Rastgele bir kelime eklenmiş | 201 - 300 Rastgele bir kelime çıkartılmış)"+","+"Test edilen modelimiz"+","+"Benzerlik Oranı"+"\n")
    benzerlikListesi = []
    performansCubugu = tqdm(total = 6600, bar_format='Modelin egitim durumu:[{bar:50}]\t[{n_fmt}/{total_fmt}]')
    for m in modelListesi:
        model = SentenceTransformer(m)
#        torch.cuda.empty_cache()
#        model = model.to(device)
        for hazirKVKKSorusu in soruListesi[0]:
            for soru in testSorulari:
                benzerlik = float(util.cos_sim(model.encode(soru),model.encode(hazirKVKKSorusu)))
                benzerlikListesi.append(benzerlik)
                dosya.write(hazirKVKKSorusu+","+soru+","+m+","+str(benzerlik)+"\n")
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