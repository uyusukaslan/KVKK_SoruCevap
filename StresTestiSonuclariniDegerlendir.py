import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

testTuru = [11,12,13,21,22,23,31,32,33]
for TT in testTuru:
    df = pd.read_csv("stresTestiSonuclari"+str(TT)+".tsv",sep="\t")
    print("Test Türü: ",TT)
    print(*"ORTALAMA\n",df.groupby(["M"]).mean())
    print(*"EN BÜYÜK\n",df.groupby(["M"]).max())
    print(*"EN KÜÇÜK\n",df.groupby(["M"]).min())
    print(*"EN STANDART SAPMA\n",df.groupby(["M"]).std())
