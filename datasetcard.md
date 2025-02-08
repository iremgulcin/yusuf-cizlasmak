# Dataset Card

---

## Dataset Card for Automatic Pothole Detection System

### Dataset Summary

Gerçek dünya yol görüntülerinden oluşan, çukur tespiti için nesne algılama modellerini eğitmeye yönelik özel bir veri kümesi. Otomatik yol bakım sistemleri ve güvenlik yönetimi için geliştirilmiştir. Bu proje, aşağıdaki Birleşmiş Milletler Sürdürülebilir Kalkınma Amaçları (SDGs) ile uyumludur:

3.6: 2030 yılına kadar trafik kazalarından kaynaklanan ölüm ve yaralanma oranlarını yarıya indirmek.
9.1: Ekonomik kalkınmayı ve insan refahını desteklemek için güvenilir, sürdürülebilir ve dayanıklı altyapı geliştirmek.
11.2: 2030 yılına kadar herkes için güvenli, uygun fiyatlı, erişilebilir ve sürdürülebilir ulaşım sistemleri sağlamak ve yol güvenliğini artırmak.

## Dataset Details

### Dataset Description

Bu veri kümesinin amacı, gerçek dünya verilerini kullanarak nesne tespiti teknikleriyle otomatik çukur tespiti yapan bir sistemin geliştirilmesini desteklemektir. Veri kümesi aşağıdaki amaçlara hizmet etmektedir:

- Yetkililere yol bakım önceliklerini belirlemede yardımcı olmak.
- Trafik kazalarını azaltmak.
- Şehir altyapı yönetimini iyileştirmek.

- **Curated by:** [More Information Needed]
- **License:** [More Information Needed]

### Dataset Sources

- **Repository:** 
- **Paper (optional):** [More Information Needed]
- **Demo (optional):** [More Information Needed]

## Uses

### Direct Use

Bu veri kümesi şunlar için tasarlanmıştır:

- Çukur tespiti için nesne algılama modellerini eğitmek ve değerlendirmek.
- Farklı nesne tespiti mimarilerini karşılaştırmak ve kıyaslamak.
- Gerçek dünya ortamlarında çukur tespiti sistemlerini test etmek.

## Dataset Structure

- **Data Type:**:  Özel olarak oluşturulmuş, gerçek yol görüntülerinden oluşan veri kümesi. Sentetik ve animasyonlu görüntüler hariç tutulmuştur.
- **Sources:**
  - Flickr API
  - DuckDuckGo API
  - Bing API
  - Önceden temizlenmiş bazı Roboflow veri kümeleri (dummy model oluşturma amaçlı)

## Dataset Creation

### Source Data

#### Data Collection and Processing

- Veriler, API tabanlı web kazıma (web scraping) yöntemleriyle gerçek dünya kaynaklarından toplanmıştır.
- Sentetik ve animasyonlu görüntüler hariç tutulmuştur.
- Veri kümesi, çukur içeren yüksek kaliteli ve çeşitli görüntüler içerecek şekilde filtrelenmiştir.
- Ek temizlik ve veri artırma (augmentation) teknikleri uygulanmıştır.

#### Features and the Target

- **Features:**  Çukur içeren gerçek yol görüntüleri.
- **Target:** 
  - İkili sınıflandırma (pothole / no pothole)
  - Nesne tespiti (çukurların etrafında sınır kutuları oluşturma)

### Annotations

#### Annotation Process

- Roboflow'dan alınan bir pothole dataset (hazır görüntü kümesinden) model eğitilmiş, API'lerden çekilen ve filtrelerden geçen görüntüler gösterilmiştir.
- Eğitilen modelde, çukur olmasına rağmen gözükmeyen görüntüler tekrardan el ile etiketlenmiş ardından data augmentation veri seti çoğaltılmıştır.

#### Who are the Annotators?

- Yusuf.

## Bias, Risks, and Limitations

- Veri kümesi, şehir içi yollarına daha fazla odaklandığı için kırsal alanlardaki yolları temsil etmekte eksik kalabilir.
- Aydınlatma, hava koşulları ve yol yüzeyi farklılıkları modelin genelleme yeteneğini etkileyebilir.
- Otomatik yol değerlendirme araçlarının kullanımı, etik sorunlar ve karar alma süreçleri açısından dikkatli bir şekilde ele alınmalıdır.

## Citation (optional)

- If a paper or blog post introducing the dataset is available, APA and BibTeX citations should be included here.



