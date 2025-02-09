# MODEL CARD

# Model Card for Automatic Pothole Detection Model

## Model Details

### Model Description

Bu model, gerçek dünya yol görüntülerinde çukur tespiti yapmak için özel olarak geliştirilmiş bir nesne algılama modelidir. Model, yol bakım önceliklerini belirlemeye yardımcı olmak, trafik kazalarını azaltmak ve şehir altyapı yönetimini iyileştirmek amacıyla kullanılır.

- **Developed by:** Yusuf Cızlaşmak
- **Model date:** 2025
- **Model type:** Nesne Algılama (Object Detection)
- **Language(s):** Görüntü İşleme
- **Finetuned from model:** YOLOv11

### Model Sources

- **Repository:** 
- **Paper [optional]:** [More Information Needed]
- **Demo [optional]:** [More Information Needed]

## Uses

### Direct Use

- Çukur tespiti için nesne algılama modellerini eğitmek ve değerlendirmek.
- Farklı nesne tespiti mimarilerini karşılaştırmak.
- Gerçek dünya ortamlarında çukur tespiti sistemlerini test etmek.

### Downstream Use [optional]

- Otonom araç sistemlerinde yol güvenliği iyileştirme.
- Trafik güvenlik sistemlerine entegre edilerek bakım önceliklerini belirleme.

### Out-of-Scope Use

- Açık deniz yolları, raylı sistemler gibi farklı altyapılar için uygun değildir.
- Medikal görüntüleme veya biyolojik veri analizi için kullanılamaz.

## Bias, Risks, and Limitations

- Veri kümesi daha çok şehir içi yollarına odaklandığından kırsal alan yolları için eksiklikler içerebilir.
- Aydınlatma, hava koşulları ve yol yüzeyi farklılıkları modelin genelleme yeteneğini etkileyebilir.
- Yanlış pozitifler ve negatifler bakım maliyetlerinde hatalara yol açabilir.

### Recommendations

- Kullanıcılar (hem doğrudan hem de dolaylı) modelin riskleri, önyargıları ve sınırlamaları konusunda bilgilendirilmelidir.
- Modelin kırsal yollarda daha iyi çalışması için veri kümesi genişletilmelidir.

## How to Get Started with the Model

Aşağıdaki kodu kullanarak modeli çalıştırabilirsiniz:

```bash
streamlit run app.py
```

ya da dockerize edilecek 

```bash
DOCKER KODU GELECEK

```

## Training Details

### Training Data

- **Dataset:** Automatic Pothole Detection System
- **Sources:** Flickr API, DuckDuckGo API, Bing API, Roboflow önceden temizlenmiş veri kümeleri
- **Annotations:** El ile etiketlenmiş ve Roboflow yardımıyla genişletilmiş

### Training Procedure

#### Preprocessing [optional]

- Veri temizleme ve ön işleme adımları uygulanmıştır.
- Veri artırma (augmentation) teknikleri kullanılmıştır.

#### Training Hyperparameters

- **Training regime:** FP16 Mixed Precision
- **Batch size:** 32
- **Optimizer:** AdamW
- **Learning rate:** 0.001

#### Speeds, Sizes, Times [optional]

- Ortalama inference süresi: 20 ms/görüntü (RTX 3090)
- Model boyutu: 200MB

## Evaluation

### Testing Data, Factors & Metrics

#### Testing Data

- Test veri kümesi, eğitim veri kümesinden bağımsız olarak toplanmıştır.

#### Factors

- Aydınlatma koşulları
- Çukur boyutları ve şekilleri

#### Metrics

- mAP (mean Average Precision): 85%
- IoU (Intersection over Union): 0.75
- FPS: 50 (RTX 3090)

### Results

- Model, şehir içi yollarda yüksek doğrulukla çalışmaktadır ancak kırsal alanlar için ek optimizasyon gerektirebilir.

#### Summary

Model, otomatik çukur tespitinde oldukça başarılıdır ve gerçek dünyada uygulanabilir.

## Model Examination [optional]

- Modelin çıktıları görselleştirilerek hata analizi yapılabilir.

## Technical Specifications [optional]

### Model Architecture and Objective

- YOLOv11 tabanlı nesne algılama modeli

### Compute Infrastructure

#### Hardware

- NVIDIA RTX 3090 GPU
- 32GB RAM, Intel i9-13900K CPU

#### Software

- Python 3.9
- PyTorch 2.0
- Ultralytics YOLOv11

## Citation [optional]

- [More Information Needed]

## Glossary [optional]

- **mAP:** Ortalama doğruluk skoru
- **IoU:** Nesne tespitinde kullanılan örtüşme metriği

## More Information [optional]

- Modelin gelişimi için ek veri kümesi ve optimizasyonlar yapılabilir.

