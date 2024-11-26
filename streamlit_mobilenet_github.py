import streamlit as st
import tensorflow as tf
import numpy as np
from tensorflow.keras.models import load_model
from PIL import Image

# Load the pre-trained model
model = load_model(r'D:\SURYA\UAJY\Semester 5\Asdos Machine Learning\Pemegang Modul\Modul CNN\Notebook2\model_mobilenet.h5')  
class_names = ['Matang', 'Mentah']

# Function to preprocess and classify image
def classify_image(image_path):
    try:
        # Load and preprocess the image
        input_image = tf.keras.utils.load_img(image_path, target_size=(180, 180))
        input_image_array = tf.keras.utils.img_to_array(input_image)
        input_image_exp_dim = tf.expand_dims(input_image_array, 0)

        # Predict using the model
        predictions = model.predict(input_image_exp_dim)
        result = tf.nn.softmax(predictions[0])  # Apply softmax for probability
        
        # Get class with highest confidence
        class_idx = np.argmax(result)
        confidence_scores = result.numpy()
        return class_names[class_idx], confidence_scores
    except Exception as e:
        return "Error", str(e)

# Function to create a custom progress bar
def custom_progress_bar(confidence, color1, color2):
    percentage1 = confidence[0] * 100  # Confidence for class 0 (Matang)
    percentage2 = confidence[1] * 100  # Confidence for class 1 (Mentah)
    progress_html = f"""
    <div style="border: 1px solid #ddd; border-radius: 5px; overflow: hidden; width: 100%; font-size: 14px;">
        <div style="width: {percentage1:.2f}%; background: {color1}; color: white; text-align: center; height: 24px; float: left;">
            {percentage1:.2f}%
        </div>
        <div style="width: {percentage2:.2f}%; background: {color2}; color: white; text-align: center; height: 24px; float: left;">
            {percentage2:.2f}%
        </div>
    </div>
    """
    st.sidebar.markdown(progress_html, unsafe_allow_html=True)

# Add snow animation background
snow_animation = """
<style>
body {
    background: linear-gradient(to bottom, #1e3c72, #2a5298);
    color: white;
    font-family: Arial, sans-serif;
}

.snowflake {
    color: white;
    font-size: 1.5em;
    position: absolute;
    top: -10%;
    animation: snow 10s linear infinite;
    opacity: 0.8;
}

@keyframes snow {
    0% { transform: translateY(0); }
    100% { transform: translateY(100vh); }
}

.snowflake:nth-child(1) { left: 10%; animation-delay: 0s; }
.snowflake:nth-child(2) { left: 20%; animation-delay: 2s; }
.snowflake:nth-child(3) { left: 30%; animation-delay: 4s; }
.snowflake:nth-child(4) { left: 40%; animation-delay: 6s; }
.snowflake:nth-child(5) { left: 50%; animation-delay: 8s; }
.snowflake:nth-child(6) { left: 60%; animation-delay: 1s; }
.snowflake:nth-child(7) { left: 70%; animation-delay: 3s; }
.snowflake:nth-child(8) { left: 80%; animation-delay: 5s; }
.snowflake:nth-child(9) { left: 90%; animation-delay: 7s; }
.snowflake:nth-child(10) { left: 100%; animation-delay: 9s; }
</style>

<div class="snowflake">❄</div>
<div class="snowflake">❅</div>
<div class="snowflake">❆</div>
<div class="snowflake">❄</div>
<div class="snowflake">❅</div>
<div class="snowflake">❆</div>
<div class="snowflake">❄</div>
<div class="snowflake">❅</div>
<div class="snowflake">❆</div>
<div class="snowflake">❄</div>
"""

st.markdown(snow_animation, unsafe_allow_html=True)

# Streamlit UI
st.title("🎄 Prediksi Kematangan Buah Naga - xxxx 🎅") #4 digit npm

# Upload multiple files in the main page
uploaded_files = st.file_uploader("Unggah Gambar (Beberapa diperbolehkan)", type=["jpg", "png", "jpeg"], accept_multiple_files=True)

# Sidebar for prediction button and results
if st.sidebar.button("Prediksi"):
    if uploaded_files:
        st.sidebar.write("### 🎁 Hasil Prediksi")
        for uploaded_file in uploaded_files:
            with open(uploaded_file.name, "wb") as f:
                f.write(uploaded_file.getbuffer())

            # Perform prediction
            label, confidence = classify_image(uploaded_file.name)
            
            if label != "Error":
                # Define colors for the bar and label
                primary_color = "#007BFF"  # Blue for "Matang"
                secondary_color = "#FF4136"  # Red for "Mentah"
                label_color = primary_color if label == "Matang" else secondary_color
                
                # Display prediction results
                st.sidebar.write(f"**Nama File:** {uploaded_file.name}")
                st.sidebar.markdown(f"<h4 style='color: {label_color};'>Prediksi: {label}</h4>", unsafe_allow_html=True)
                
                # Display confidence scores
                st.sidebar.write("**Confidence:**")
                for i, class_name in enumerate(class_names):
                    st.sidebar.write(f"- {class_name}: {confidence[i] * 100:.2f}%")
                
                # Display custom progress bar
                custom_progress_bar(confidence, primary_color, secondary_color)
                
                st.sidebar.write("---")
            else:
                st.sidebar.error(f"Kesalahan saat memproses gambar {uploaded_file.name}: {confidence}")
    else:
        st.sidebar.error("Silakan unggah setidaknya satu gambar untuk diprediksi.")

# Preview images in the main page
if uploaded_files:
    st.write("### Preview Gambar")
    for uploaded_file in uploaded_files:
        image = Image.open(uploaded_file)
        st.image(image, caption=f"{uploaded_file.name}", use_column_width=True)