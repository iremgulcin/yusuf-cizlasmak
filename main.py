import gradio as gr
import subprocess
import os
from PIL import Image
import glob
import shutil
import time

def yolo_predict(image, conf, model_path='medium_model.pt'):
    if not model_path:  # Model path boş ise varsayılan değeri kullan
        model_path = "medium_model.pt"
        
    try:
        os.makedirs("temp_output", exist_ok=True)
        input_image_path = "temp_input.jpg"
        image.save(input_image_path)
        
        yolo_command = [
            "yolo",
            "task=detect",
            "mode=predict",
            f"conf={conf}",
            "save=True",
            f"model={model_path}",
            f"source={input_image_path}",
            "project=temp_output",
            "name=result",
            "device=cpu"
        ]
        
        subprocess.run(yolo_command, check=True)
        
        output_folder = "temp_output/result"
        output_images = glob.glob(os.path.join(output_folder, "*.jpg"))
        
        if output_images:
            output_image = Image.open(output_images[0])
            result = output_image.copy()
            output_image.close()
            return result
        return None
        
    except Exception as e:
        print(f"Error: {e}")
        return None
    finally:
        try:
            if os.path.exists("temp_input.jpg"):
                os.remove("temp_input.jpg")
            if os.path.exists("temp_output"):
                time.sleep(0.5)
                shutil.rmtree("temp_output", ignore_errors=True)
        except Exception as e:
            print(f"Cleanup error: {e}")

interface = gr.Interface(
    fn=yolo_predict,
    inputs=[
        gr.Image(type="pil", label="Resim Yükle")
    ],
    outputs=gr.Image(type="pil", label="Sonuç"),
    title="YOLO Nesne Tespiti"
)

if __name__ == "__main__":
    interface.launch()