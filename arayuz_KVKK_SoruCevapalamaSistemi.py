from sentence_transformers import SentenceTransformer, util
import pandas as pd
import tkinter
import tkinter.scrolledtext
# from zemberek import TurkishSentenceNormalizer, TurkishMorphology Yavaş Çalıştığı için normalizasyondan vazgeçtik

model = SentenceTransformer('sentence-transformers/quora-distilbert-multilingual')

def onIslemler(cumle):
    
    # Tüm büyük harfler küçük harflere çevriliyor
    cumle = cumle.lower()

    # Noklama işaretleri ve rakamlar kaldırılıyor
    for karakter in cumle:
        if not(karakter in "abcçdefgğhıijklmnoöprsştuüvyz "): #boşluk kalsın
                cumle = cumle.replace(karakter,"")

    # Bilinen kısaltmalar açılıyor
    while "kvkk" in cumle:
        cumle = cumle.replace("kvkk","kişisel verilerin korunumu kanunu")    

    # Etkisiz Kelimeler (Stop Words) Çıkartılıyor
    with open("poyraz_temiz_stop_words.txt", "rt", encoding="utf-8") as dosyaEtkisizKelimeler:
        etkisizKelimeListesi = dosyaEtkisizKelimeler.readlines()
        cumleListe = cumle.split(" ")
        for cumleninKelimesi in cumleListe:
            for kelime in etkisizKelimeListesi:
                if cumleninKelimesi in kelime:
                    while cumleninKelimesi in cumleListe:
                        cumleListe.remove(cumleninKelimesi)
        cumle = ""
        cumle = ' '.join(map(str, cumleListe))

    # Cümle normalizasyonu  YAVAŞ ÇALIŞTIĞI İÇİN normalizasyondan vazgeçtik.
#    morphology = TurkishMorphology.create_with_defaults()
#    normalizer = TurkishSentenceNormalizer(morphology)
#    cumle = normalizer.normalize(cumle)


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

def sohbetEkraniniOlustur():

    def soruyuCevapla(basilanTus):
        # Kullanıcı tarafından veri girişi yapılır.
        kullanicininGirdigiSoru = girdiEkrani.get().strip()
        girdiEkrani.delete(0, tkinter.END)
        if kullanicininGirdigiSoru:
            sohbetEkrani.config(state=tkinter.NORMAL)
            sohbetEkrani.tag_config("kullanicininAdininRengi", foreground="#000000")
            sohbetEkrani.tag_config("kullanicininSorusununRengi", foreground="#666666")
            sohbetEkrani.tag_config("uyariEkraniRengi", foreground="#CC0000", justify="center")
            sohbetEkrani.tag_config("sisteminAdininRengi", foreground="#000000")
            sohbetEkrani.tag_config("sisteminCevabininRengi", foreground="#999999")
            sohbetEkrani.insert(tkinter.END, "\nSorunuz analiz ediliyor.\n\n")
            sohbetEkrani.insert(tkinter.END, "\nSorduğunuz soru: ","kullanicininAdininRengi")
            sohbetEkrani.insert(tkinter.END, kullanicininGirdigiSoru + "\n", "kullanicininSorusununRengi")

            # Girilen soru ön işlemlerden geçirilir.
            kullanicininGirdigiSoru = onIslemler(kullanicininGirdigiSoru)

            # Ön işlemden geçirilen soru encode ediliyor.
            encodedSoru = model.encode(kullanicininGirdigiSoru)

            # Ön işlemden geçirilen ve encode edilen soru ile
            # hazır soruların encode edilmiş hallerinin benzerlik puanları bir listeye kaydediliyor
            benzerlikListesi = []
            soruListesi = sorulariDosyadanOkuveListeOlarakDondur()

            for i in range(100):
                soru = soruListesi[i][0]
                soru = onIslemler(soru)
                benzerlikListesi.append(util.cos_sim(encodedSoru, model.encode(soru)))

            # Benzerlik puanı en büyük soru ve cevabı döndürülür
            bul = benzerlikListesi.index(max(benzerlikListesi))
            soruMetni = soruListesi[bul][0]+"?\n"
            sohbetEkrani.insert(tkinter.END, soruMetni , "sisteminAdininRengi")
            ayir = chr(92)+"n"
            cevapMetni = str(soruListesi[bul][1]).split(ayir)
            for cevap in cevapMetni:
                sohbetEkrani.insert(tkinter.END, cevap+"\n\n", "sisteminCevabininRengi")
        
        sohbetEkrani.see(tkinter.END)

    ekran = tkinter.Tk()
    ekran.title("Son Dil Bükücüler - KVKK Soru Cevap Sistemi")
    ekran.geometry("1024x768")
    ekran.resizable(width=False, height=False)
    ekran.configure(background="#336699")
    sohbetEkrani = tkinter.scrolledtext.ScrolledText(ekran, bd=0, bg="#CCDDEE", width="1004", height="688", font="System",wrap=tkinter.WORD)
    sohbetEkrani.place(x=10, y=70, width=1004, height=598)
    etiket1 = tkinter.Label(ekran, bd=0, bg="#FFFFDD", text="Kişisel Verilerin Kullanımı Kanunu Soru - Cevap Sistemine hoş geldiniz.\nSistemimiz sorularınızı aşağıdaki kutucuktan kabul edecektir. Kabul edilen sorunuz analiz edilip anlaşılmaya çalışılacaktır. Anlaşılan sorunuza cevap verilecektir.", relief=tkinter.FLAT, justify= "center")
    etiket1.place(x=10, y=10, width=1004, height=50)
    etiket2 = tkinter.Label(ekran, bd=0, bg="#FFDDDD", text="Sorunuzu aşağıdaki kutucuğa yazdıktan sonra ENTER tuşuna basınız!", relief=tkinter.FLAT, justify= "center")
    etiket2.place(x=10, y=688, width=1004, height=30)
    girdiEkrani = tkinter.Entry(ekran, bd=0, bg="#EEEEFF", font="Terminal", justify="center")
    girdiEkrani.place(x=10, y=718, width=1004, height=30)
    girdiEkrani.focus()
    girdiEkrani.bind("<Return>", soruyuCevapla)
    ekran.mainloop()

sohbetEkraniniOlustur()