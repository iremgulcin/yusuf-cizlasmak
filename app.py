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
            st.image(display_image, use_column_width=True)

        # 📊 Progress bar güncelle
        status_text.text("📥 Görüntü yüklendi...")
        progress_bar.progress(20)
        time.sleep(0.5)

        # 🏎️ YOLO komutunu çalıştır
        yolo_command = [
            "yolo",
            "task=detect",
            "mode=predict",
            f"conf={confidence}",
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
                st.image(output_image, use_column_width=True)

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
    - Güven skoru ayarlayarak hassasiyeti değiştirebilirsiniz.
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
    - Kullanılan Model: **YOLO**
    - İşlem Süreci:  
      - Görsel yüklenir  
      - Model çalıştırılır  
      - Çıktı üretilir ve ekranda gösterilir  

    ### 📊 Yapılan Adımlar:
            

    **🔗 Daha fazla bilgi için [Samsung Innovation Campus AI Project](https://github.com/iremgulcin/yusuf-cizlasmak) sayfasını ziyaret edebilirsiniz.**  
    """)

# ℹ️ Footer
st.markdown("""
---
👨‍💻 **Geliştirici:** Yusuf Cızlaşmak

🚀 **Bu proje, Samsung Innovation Campus AI Project için tasarlanmıştır.**  
""")

