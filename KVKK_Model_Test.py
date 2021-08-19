from sentence_transformers import SentenceTransformer, util
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def sorulariDosyadanOkuveListeOlarakDondur():
    gecici = []
    for i in range(100):
        gecici.append([])
    df = pd.read_csv('KVKK_100_SORU_CEVAP.txt',sep="\t")
    for i in range(100):
        gecici[i].append(df.to_numpy()[i][1])       #Soru
        gecici[i].append(df.to_numpy()[i][2])       #Cevabı
    return(gecici)

testSorulari = ["Rızası Açık Nedir","Bizim rıza kimdir","Açık Rıza Nedir","Veri Sorumlusunun Meşru Menfaatini Tespit Etmek İçin Göz Önünde Bulundurulması Gereken Hususlar Nelerdir?","Kanun Kapsamındaki Kısmi İstisna Halleri Nelerdir"]

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

for m in modelListesi:
    model = SentenceTransformer(m)
    encodedSoru = []
    for soru in testSorulari:
        encodedSoru.append(model.encode(soru))

    benzerlikListesi = []
    soruListesi = sorulariDosyadanOkuveListeOlarakDondur()

    sayac=0
    for soru in encodedSoru:
        for i in range(100):
            benzerlikListesi.append(util.cos_sim(soru,model.encode(soruListesi[i][0])))
        sayac+=1

    benzerlikListesi2 = []
    for oge in benzerlikListesi:
        benzerlikListesi2.append(float(oge))
    del(benzerlikListesi)

    for s in range(sayac):
        bul = benzerlikListesi2.index(max(benzerlikListesi2[0+s*100:99+s*100]))
        print("Model: ",m)
        print("Test sorusu: ",testSorulari[s])
        print("En yakın soru: ",soruListesi[bul%100][0])
        print("En yakın sorunun benzerlik puanı: ",max(benzerlikListesi2[0+s*100:99+s*100]))
        print("100 soru için standart sapma: ",np.std(benzerlikListesi2[0+s*100:99+s*100]))
        print("100 soru için varyans: ",np.var(benzerlikListesi2[0+s*100:99+s*100]))
        print("100 soru için en az benzerlik: ",np.min(benzerlikListesi2[0+s*100:99+s*100]))
        print("100 soru için en çok benzerlik: ",np.max(benzerlikListesi2[0+s*100:99+s*100]))
        plt.hist(benzerlikListesi2[0+s*100:99+s*100], 100)
        plt.show() # subplot ile gösterim geliştirilecek/iyileştirilecek 
        print("\n")