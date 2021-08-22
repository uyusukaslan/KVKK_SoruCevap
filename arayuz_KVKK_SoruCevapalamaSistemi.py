from sentence_transformers import SentenceTransformer, util
import pandas as pd
import tkinter
import tkinter.scrolledtext

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
            
            sohbetEkrani.insert(tkinter.END, "\nSorduğunuz soru: ","kullanicininAdininRengi")
            sohbetEkrani.insert(tkinter.END, kullanicininGirdigiSoru + "\n", "kullanicininSorusununRengi")
            sohbetEkrani.insert(tkinter.END, "\nSorunuz analiz ediliyor.\n\n","uyariEkraniRengi")

            # Girilen soru ön işlemlerden geçirilir.
            kullanicininGirdigiSoru = onIslemler(kullanicininGirdigiSoru)

            # Ön işlemden geçirilen soru encode ediliyor.
            encodedSoru = model.encode(kullanicininGirdigiSoru)

            # Ön işlemden geçirilen ve encode edilen soru ile
            # hazır soruların encode edilmiş hallerinin benzerlik puanları bir listeye kaydediliyor
            benzerlikListesi = []
            soruListesi = sorulariDosyadanOkuveListeOlarakDondur()
            for i in range(100):
                benzerlikListesi.append(util.cos_sim(encodedSoru, model.encode(soruListesi[i][0])))

            # Benzerlik puanı en büyük soru ve cevabı döndürülür
            bul = benzerlikListesi.index(max(benzerlikListesi))
            soruMetni = soruListesi[bul][0]+"?\n"
            cevapMetni = soruListesi[bul][1]+".\n"
            sohbetEkrani.insert(tkinter.END, soruMetni , "sisteminAdininRengi")
            sohbetEkrani.insert(tkinter.END, cevapMetni, "sisteminCevabininRengi")
        
        sohbetEkrani.see(tkinter.END)

    ekran = tkinter.Tk()
    ekran.title("Son Dil Bükücüler - KVKK Soru Cevap Sistemi")
    ekran.geometry("640x480")
    ekran.resizable(width=False, height=False)
    ekran.configure(background="#336699")
    sohbetEkrani = tkinter.scrolledtext.ScrolledText(ekran, bd=0, bg="#CCDDEE", width="620", height="400", font="System",wrap=tkinter.WORD)
    sohbetEkrani.place(x=10, y=100, height=270, width=620)
    etiket1 = tkinter.Label(ekran, bd=0, bg="#FFFFDD", text="Kişisel Verilerin Kullanımı Kanunu Soru - Cevap Sistemine hoş geldiniz.\nSistemimiz sorularınızı aşağıdaki kutucuktan kabul edecektir.\nKabul edilen sorunuz analiz edilip anlaşılmaya çalışılacaktır.\nAnlaşılan sorunuza cevap verilecektir.", relief=tkinter.FLAT, justify= "center")
    etiket1.place(x=10, y=10, height=80, width=620)
    etiket2 = tkinter.Label(ekran, bd=0, bg="#FFDDDD", text="Sorunuzu aşağıdaki kutucuğa yazdıktan sonra ENTER tuşuna basınız!", relief=tkinter.FLAT, justify= "center")
    etiket2.place(x=10, y=390, height=30, width=620)
    girdiEkrani = tkinter.Entry(ekran, bd=0, bg="#EEEEFF", font="Terminal", justify="center")
    girdiEkrani.place(x=10, y=430, height=30, width=620)
    girdiEkrani.focus()
    girdiEkrani.bind("<Return>", soruyuCevapla)
    ekran.mainloop()

sohbetEkraniniOlustur()