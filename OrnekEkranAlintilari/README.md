Çalışmamızı daha iyi ifade edebilmek için örnek ekran alıntılarımız aşağıdaki gibidir.

Bu kısımda hangi ekranın neyi anlattığı yazılacaktır.

# Arayüz

Arayüzümüz, son kullanıcının hizmetimizi daha rahat bir şekilde kullanabilmesi için oluşturulmuş olup gerekli bütün fonksiyonları içermektedir.

------------------------------------

Bu iki ekran alıntısı, arayüzümüzün ilk prototipidir. Girilen soruyu alma, işleme ve geriye bir cevap döndürme özelliklerine sahiptir.

![](SoruCevapSistemininCalışmaOrneği01.png)


![](SoruCevapSistemininCalışmaOrneği02.png)

---------------------

Buradaki ekran alıntısı ise arayüzümüzün son halidir. Bir önceki prototipten farkları şunlardır:

- İlk prototipteki ekran boyutunun yetersizliğinden kaynaklı olarak, yazılan veya geri döndürülen yazıların okunması zordu. Bu yüzden, arayüzümüzü "1024x768" olarak güncelledik.
- İlk prototipte, beyaz boşluk olarak tanımlanan "\n" karakterini (Enter tuşu) ekrana herhangi bir boşluk olarak değil, "\n" olarak yazıyor ve kaçış karakteri olan "\\" karakterini algılayamıyordu. Bu sorunu gidererek daha anlaşılır bir yazı olmasını sağladık.
- İlk prototipte soruların vektörleri önceden hesaplanmak yerine her sorulan soru için bir daha hesaplanıyordu. Bu, gereksiz bir hesap olarak sistem gücünü boşa harcamanın yanı sıra sorulan soru başına 2 ila 10 saniye arasında bir bekleme süresine denk geliyordu. Bu sırada arayüze hiçbir komut girilemiyor, pencere yanıt vermiyordu. Kullanıcı deneyimini olumsuz etkileyen bu durumu, bütün sorular için sadece bir defaya mahsus olmak üzere açılırken 3 saniye kadar bir süre içinde bütün soruların vektörlerini hesaplayarak gidermiş bulunmaktayız. Böylece kullanıcı, istediği cevaplara anında erişebilir duruma geldi.

![](SoruCevapSistemininCalışmaOrneği03.png)


-------

Bu GIF'te ise nihai arayüzümüzün kullanımı gösteriliyor.

![](KVKK_Soru_Cevap_Sistemi_On_izlemesi01.gif)





# Model Eğitimi

Eğer modelinizi eğitmek isterseniz, karşınıza böyle bir ekran çıkacaktır. Bu ekranda modelin eğitilirkenki durumu gözlemlenebilmektedir. 

![](ModelEgitimiOrnek01.png)

-----------------

Bu ekran alıntısı ise modelin eğitimi tamamlandığında ortaya çıkacaktır. Modelin ne kadar sürede eğitildiği bilgisi, burada yazacaktır.

![](ModelEgitimiOrnek02.png)
