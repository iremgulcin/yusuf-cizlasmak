import streamlit as st
from PIL import Image
import os
import subprocess
import glob
import time
import shutil

# 📏 Görselleri sadece ekranda gösterirken küçült
def resize_for_display(image_path, max_size=(800, 600)):
    """Görseli ekranda düzgün gösterim için yeniden boyutlandırır"""
    img = Image.open(image_path)
    img.thumbnail(max_size, Image.Resampling.LANCZOS)
    return img

# 🖼️ YOLO işleme fonksiyonu
def process_image(uploaded_image, model_path='medium_model.pt', confidence=0.25):
    """Görseli işler ve YOLO modelini çalıştırır"""
    
    # ⏳ Progress bar başlat
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    try:
        # 📂 Geçici klasörleri oluştur
        os.makedirs("temp_output", exist_ok=True)
        input_image_path = "temp_input.jpg"
        
        # 🖼️ Orijinal görüntüyü kaydet (Modelin işleyeceği gerçek dosya)
        image = Image.open(uploaded_image)
        image.save(input_image_path)

        # 📍 Ekranda gösterilecek görüntüyü hazırla
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("📷 Yüklenen Görsel")
            display_image = resize_for_display(input_image_path)
            st.image(display_image, use_container_width=True)

        # 📊 Progress bar güncelle
        status_text.text("📥 Görüntü yüklendi...")
        progress_bar.progress(20)
        time.sleep(0.5)

        # 🏎️ YOLO komutunu çalıştır
        yolo_command = [
            "yolo",
            "task=detect",
            "mode=predict",
            f"conf=0.25",
            "save=True",
            f"model={model_path}",
            f"source={input_image_path}",
            "project=temp_output",
            "name=result",
            "device=cpu"
        ]
        subprocess.run(yolo_command, check=True)

        # 📊 Progress bar güncelle
        status_text.text("⚙️ Model çıktıyı işliyor...")
        progress_bar.progress(80)

        # 🎯 Çıktı dosyasını bul ve göster
        output_folder = "temp_output/result"
        output_images = glob.glob(os.path.join(output_folder, "*.jpg"))

        if output_images:
            output_image_path = output_images[0]

            with col2:
                st.subheader("📌 Model Sonucu")
                output_image = resize_for_display(output_image_path)
                st.image(output_image, use_container_width=True)

            # ✅ İşlem tamamlandı
            progress_bar.progress(100)
            status_text.text("✅ İşlem tamamlandı!")
            time.sleep(1)
            progress_bar.empty()
            status_text.empty()
        else:
            st.error("⚠️ Model bir çıktı üretmedi!")

    except Exception as e:
        st.error(f"❌ Hata oluştu: {str(e)}")
        progress_bar.empty()
        status_text.empty()

    finally:
        # 🗑️ Geçici dosyaları temizle
        try:
            if os.path.exists(input_image_path):
                os.remove(input_image_path)
            if os.path.exists("temp_output"):
                time.sleep(0.5)
                shutil.rmtree("temp_output", ignore_errors=True)
        except Exception as e:
            st.error(f"🗑️ Temizlik hatası: {e}")

# 🚀 Sayfa Yapısı
st.set_page_config(page_title="Çukur Tespit Sistemi", page_icon="🕳️", layout="wide")

# 📌 Sayfa Seçimi (Sol Menü)
menu = st.sidebar.radio("📌 Sayfa Seç", ["Ana Sayfa", "Dokümantasyon"])

# 📌 Ana Sayfa (Model Çalıştırma)
if menu == "Ana Sayfa":
    st.title("🕳️ Çukur Tespit Sistemi")
    st.markdown("""
    ### 📷 **Görselinizi yükleyin ve tespit yapın!**
    - Model, tespit edilen çukurları otomatik olarak işaretler.
    """)

    # 📂 Görsel Yükleme
    uploaded_image = st.file_uploader("📥 Bir görüntü seçin", type=["jpg", "jpeg", "png"])

    # 🔍 İşlem Başlat
    if uploaded_image:
        if st.button("🔍 Çukuru Tespit Et"):
            with st.spinner("🚀 Model çalıştırılıyor..."):
                process_image(uploaded_image, model_path='medium_model.pt', confidence=0.25)



# 📚 Dokümantasyon Sayfası
elif menu == "Dokümantasyon":
    st.title("📖 Dokümantasyon")
    
    st.markdown("""
    ## 📌 Çukur Tespit Sistemi Hakkında  
    Bu sistem, **YOLO (You Only Look Once)** modelini kullanarak çukur tespiti yapar.  
    Yüklediğiniz görüntü işlenerek model tarafından değerlendirilir ve çukurlar tespit edilir.  

    ### 🛠 Kullanım Adımları:
    1. **Ana Sayfa'ya gidin**  
    2. **Bir görüntü yükleyin** (JPG, JPEG veya PNG formatında olmalı)  
    3. **"Çukuru Tespit Et" butonuna basın**  
    4. Modelin çıktısını inceleyin 🎯  

    ### ⚙️ Model Detayları:
    - Kullanılan Model: **YOLOv11s**  
    
    """)

    #Yapılan Adımlar


    st.markdown("""
    ### 📊 Yapılan Adımlar:

    #### 1) Data Mining ⛏️ :
    - **Çukur görüntülerini elde etmek için DuckDuckGo, Flickr, Bing ve Yahoo API’leri kullanılmıştır. Yaklaşık 3000'den çekilen resim bulunmaktadır.**
    - **Örnek Görüntüler:**
    """, unsafe_allow_html=True)

    st.image("assets/1.png", caption="Örnek Görüntü")


    st.markdown("""
    ### 2) PCA Analizi ve K-Means Kümeleme 🌌

    - **Web’den çekilen 3.000’den fazla görselin manuel olarak incelenmesi zahmetli olduğu için, embeddings çıkarılarak boyutları azaltıldı ve  512 features--- > 120 new features elde edildi.**  
    - **Bu süreçte, PCA ile boyut indirgeme ve K-Means algoritması ile benzer görsellerin gruplandırılması sağlandı.**  

    #### **PCA analizi :**
    """, unsafe_allow_html=True)


    st.image("assets/2.png", caption="PCA Analizi")

    st.markdown("""
            #### **K-Means analizi :**   
    """)

    st.image("elbow_plots/pothole_elbow.png", caption="Dirsek Yöntemi ile Seç")
    st.image("cluster_plots/final_clusters.png", caption="K-Means Kümeleme")

    st.markdown("""
    ###

    - **K-Means algoritması ile benzer görsellerin gruplandırılması sağlandı. Teker teker istenilen görüntüler bu şekilde bir araya getirildi.
        Bu cluster'ların sol tarafı istenmeyen görüntüler (cluster-2 ve cluster-5) toplanırken, istenilen görüntüler ise sağ tarafta toplandığı gözlemi yapılmıştır.**
        
                
        #### **İstenilen ve istenmeyen, filigran görüntü sayısı :**


    """, unsafe_allow_html=True)


    st.image("assets/cluster_analizi.png", caption="Cluster Analizi")


    
    st.markdown("""
    ### 3) Activate Learning ve Data Augmentation 🧠

    - İlk başta Roboflow hazır veri seti tarafından eğitilen model, bu ayıklanan veri setiyle detect edildi. Ve çukur varken çukur yok olarak gösterilen resimler tekrardan elle etiketlendi. 
        Bu sayede hem veri çeşitliliği arttırıldı hem de modelin daha iyi öğrenmesi sağlanmaya çalıştı. Bunun yanında yeni eğitilecek model için farklı data augmentation teknikleri kullanıldı.
        
    #### **Kullanılan Data Augmentation Teknikleri  :**   
    """, unsafe_allow_html=True)


    st.image("assets/data_augmentation_3.png", caption="Klasik Data Augmentation Yöntemleri")

    st.markdown("""
    - Bu klasik data augmentation'ın kullanma nedenleri şunlardır:

        - **Rotation 90°**  
        Sadece dik uzanması veya yatay uzanması öğrenilmesin diye görüntüler döndürüldü.

        - **Brightness**  
        Karanlık çekilen görüntüler olabileceği için, parlaklıklarını artırmak faydalı olacaktır.

        - **Noise**  
        Kameralarda anlık bozulmalara (gürültü) meydana gelebileceği için eklendi.

        - **Blur**  
        Kameradan her zaman net görüntü alınamayabileceği için bulanıklık simüle edildi.
    """, unsafe_allow_html=True)


    st.markdown("""
    - Bunun yanında veri çeşiitliliğini arttırmak için **Cutout** ve **Mixup** teknikleri de kullanıldı. (Cutmix) 
                
    #### **Cutout ve Mixup Teknikleri kullanılmış bazı örnekler :**
    """, unsafe_allow_html=True)


    st.image("assets/data_augmentation_4.png", caption="Cutmix Tekniği")


    st.markdown("""
    ### 4) Model Eğitimi 🚀
    - Dummy model (Roboflow'dan alınan hazır etikelenmiş veri seti) ile sonrasında önceki aşamalarla elde edilen veri seti **YOLOV11s** ile eğitim yapıldı.
    - Modelin eğitim süreci 50 epoch olarak belirlendi. İlgili modellerin karşılaştırılması **test verisi** üzerinden yapıldı. Sonuçları models/ klasöründe bulunmaktadır.
    
    #### **Model Eğitim Sonuçları:**   
    """, unsafe_allow_html=True)

    st.image("assets/comparing_models_5.png", caption="Modellerin karşılaştırması (Test verisi üzerinden) Source: models/kaggle_dummy_last_compare_and_model_training.ipynb")


    st.markdown("""
    ### 5) Arayüz Tasarımı 🎨
                
    - Streamlit kütüphanesi kullanılarak arayüz tasarlandı. Kullanıcıdan alınan görsel, model tarafından işlenerek çukurlar tespit edildi.
   
    """, unsafe_allow_html=True)


    st.image("assets/arayuz_6.png", caption="Streamlit Arayüzü (ANASAYFA)")


    st.markdown("""
    ### 6) Gerçek Mekanlarda Test 🏢
                
    - Projenin başında hedeflenen gerçek mekanlarda test aşaması Sakarya Üniversitesi Merkez Kampüsünde gerçekleştirildi. Bu testler sonucunda modelin çukur tespit etme konusunda başarılı iyi sonuçlar verildiği tespit edildi.

    #### **Gerçek Mekanlarda Test Sonuçları :**      
    """, unsafe_allow_html=True)

    st.image("assets/testing_1_gorsel.jpg", caption="Sakarya Üniversitesi Merkez Kampüsü Test-1 Görseli")
    st.image("assets/testing_1_result.png", caption="Sakarya Üniversitesi Merkez Kampüsü Test-1 Sonucu")
    st.image("assets/testing_2_gorsel.jpg", caption="Sakarya Üniversitesi Merkez Kampüsü Test-2 Görseli")
    st.image("assets/testing_2_result.png", caption="Sakarya Üniversitesi Merkez Kampüsü Test-2 Sonucu")
    st.image("assets/testing_3_gorsel.jpg", caption="Sakarya Üniversitesi Merkez Kampüsü Test-3 Görseli")
    st.image("assets/testing_3_result.png", caption="Sakarya Üniversitesi Merkez Kampüsü Test-3 Sonucu")
    st.image("assets/testing_4_gorsel.jpg", caption="Sakarya Üniversitesi Merkez Kampüsü Test-4 Görseli")
    st.image("assets/testing_4_result.png", caption="Sakarya Üniversitesi Merkez Kampüsü Test-4 Sonucu")



    st.markdown("""
    ### 7) Dockerize 🐳
                
    - Proje Dockerize edilerek, herkesin kolayca kullanabilmesi sağlandı.
     
    """, unsafe_allow_html=True)

    st.image("assets/docker.png", caption="Bu tarz bir durumun önüne geçmek için Dockerize edildi.")


    st.markdown("""
    ### 8) Uygulamayı Başlatma ve Durdurma 🚀

    - Uygulamayı başlatmak için aşağıdaki komutu github'da bulunan docker-compose.yml kullanabilirsiniz:

    ```sh
    docker-compose up -d
    ```

    - Uygulamayı durdurmak için aşağıdaki komutu kullanabilirsiniz:

    ```sh
    docker-compose down
    ```
    """)



    st.markdown("""
    🔗 Daha fazla bilgi için [Samsung Innovation Campus AI Project-Github](https://github.com/iremgulcin/yusuf-cizlasmak) sayfasını ziyaret edebilirsiniz.  
    """)












# ℹ️ Footer
st.markdown("""
---
👨‍💻 **Geliştirici:** Yusuf Cızlaşmak

🚀 **Bu proje, Samsung Innovation Campus AI Project için tasarlanmıştır.**  
""")

