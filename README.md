# yusuf-cizlasmak


* ## Hedefler: 

- Roboflow'dan toplanan dummy modeller ile başlangıç için model eğitimi

- DuckDuckGo, Flickr, Bing, Yahoo API kullanarak resimleri Çukur 
Görüntülerini indirme

- İndirilen görüntülerin;
    
    * Embeddings'lerini çıkartma
    * PCA ile Boyut azaltımı sağlama
    * Azaltılan PCA boyutları ile K-Means algoritmalarıyla kümeleme yapılması
    * Kümeleme yapılan görüntülerin hızlı bir şekilde ayrılıştırması ve ayrıştırılan görüntülerin modelin tahminine tabii tutulup, göremediklerinin etiketlenip tekrardan eğitilmesi( ACTIVATE LEARNING)

    * Her aşamada modellerin belirli bir val. setiyle karşılaştırılması* (Gerçek veri seti)    