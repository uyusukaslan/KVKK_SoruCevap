import torch
import pandas as pd
from transformers import AdamW, AutoTokenizer, AutoModelForSequenceClassification
import warnings
import time
from tqdm import tqdm

def sorulariDosyadanOkuveListeOlarakDondur(son): #batch dolmasın diye soruları ikişer ikişer gönderiyoruz.
    gecici = []
    df = pd.read_csv('KVKK_100_SORU_CEVAP.txt',sep="\t")
    #print(df.to_numpy()[soruNo-1][0],sep="",end=" - ")   #Soru numarası
    gecici.append(df.to_numpy()[son][1])       #Soru
    gecici.append(df.to_numpy()[son+1][1])       #Soru
    #for eleman in df.to_numpy()[soruNo-1][2].split('\\n'): #Sorunun cevabı
    #    print(eleman,end='\n\n')
    return(gecici)

warnings.filterwarnings('ignore')

# device = torch.device("cuda:0") if torch.cuda.is_available() else torch.device("cpu") 
# GPU kullanmak için .to(device) yazmanız yeterlidir.
# Örneğin, model = model.to(device)

# Daha detaylı kullanım için aşağıdaki torch komutları incelenebilir. 
# if torch.cuda.is_available():
    # torch.cuda.current_device()
    # torch.cuda.device(0)
    # torch.cuda.device_count()
    # torch.cuda.get_device_name(0)

checkpoint = "sentence-transformers/paraphrase-MiniLM-L3-v2"
tokenizer = AutoTokenizer.from_pretrained(checkpoint)
model = AutoModelForSequenceClassification.from_pretrained(checkpoint)

print("\n\n----Model Eğitimi Başlıyor----\n\n")

baslamaZamani = time.time()
performansCubugu = tqdm(total = 100, bar_format='Modelin egitim durumu:[{bar:50}]\t[{n_fmt}/{total_fmt}]')
for i in range(0,100,2):
    sequences = sorulariDosyadanOkuveListeOlarakDondur(i)
    batch = tokenizer(sequences, padding=True, truncation=True, return_tensors="pt")
    batch = batch
    batch["labels"] = torch.tensor([1, 1])

    optimizer = AdamW(model.parameters())
    loss = model(**batch).loss
    loss.backward()
    optimizer.step()
    performansCubugu.update(2)

performansCubugu.close()
gecenSure = time.time() - baslamaZamani #Saniye cinsinden

print("\n\n----Eğitim için geçen süre----")
print("Saat:\t",int(gecenSure//3600))
print("Dakika:\t",int((gecenSure%3600)//60))
print("Saniye:\t", int(gecenSure%60))

model.save_pretrained("D:\EgitilmisModeller")

# model.push_to_hub("KVKK-sentence-similarity-pytorch-roberta", use_temp_dir=True, repo_url="https://huggingface.co/sertacates/KVKK-sentence-similarity-pytorch-roberta")

# Eğitilmiş Modelinizi huggingface ile paylaşabilirsiniz.
