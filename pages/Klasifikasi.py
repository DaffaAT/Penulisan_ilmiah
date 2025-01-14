import streamlit as st
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
from tensorflow.keras.models import Model, load_model
from tensorflow.keras.preprocessing.image import load_img, img_to_array

st.sidebar.success("Klasifikasi")

# Memuat model
modelbean = load_model('Coffee_Bean.keras')
modelclassification = load_model('Coffee_Classification.keras')

# Mendefinisikan class names (ganti dengan nama-nama kelas yang sesuai)
class_beanclassification = ['Arabika', 'Bukan Biji Kopi', 'Liberika', 'Robusta']
class_roast = ['Dark', 'Green', 'Light', 'Medium'] 

# Fungsi untuk menampilkan gambar
def show_image(image, title=''):
    plt.imshow(image)
    plt.title(title)
    plt.axis('off')
    
# Mengunggah file gambar di sidebar
st.sidebar.subheader('Upload Gambar Biji kopi anda disini')
st.sidebar.write('Prediksi akan lebih akurat apabila gambar yang di seleksi dalam bentuk biji kopi satuan dengan background polos atau tanpa background')
uploaded_file = st.sidebar.file_uploader('Drag file disini', type=['png', 'jpg', 'jpeg'])

gambar_roast = uploaded_file

st.markdown("---")

st.subheader('Hasil prediksi')
if uploaded_file != None:
    # Membaca gambar
    image = Image.open(uploaded_file).convert('RGB')
    image = image.resize((256, 256))
    image = img_to_array(image) / 255.0  # Preproses gambar
    image = np.expand_dims(image, axis=0)  # Tambahkan dimensi batch

    # Membuat prediksi dan mendapatkan confidence level
    predictions = modelclassification.predict(image)
    pred_label_idx = np.argmax(predictions)
    pred_label = class_beanclassification[pred_label_idx]
    confidence = np.max(predictions)  # Confidence level

    # Menampilkan gambar dan prediksi jenis biji kopi
    st.image(uploaded_file)
    st.write(f'Gambar ini termasuk dalam kategori jenis {pred_label} dengan tingkat keyakinan {confidence:.2%}')

    # Jika prediksi bukan "Bukan Biji Kopi", tampilkan prediksi roast level
    if pred_label != 'Bukan Biji Kopi':
        if gambar_roast:
            # Membaca gambar roast
            image_roast = Image.open(gambar_roast).convert('RGB')
            image_roast = image_roast.resize((256, 256))
            image_roast = img_to_array(image_roast) / 255.0  # Preproses gambar
            image_roast = np.expand_dims(image_roast, axis=0)  # Tambahkan dimensi batch

            # Membuat prediksi roast level dan mendapatkan confidence level
            roast_predictions = modelbean.predict(image_roast)
            roast_pred_label_idx = np.argmax(roast_predictions)
            roast_pred_label = class_roast[roast_pred_label_idx]
            roast_confidence = np.max(roast_predictions)  # Confidence level

            st.write(f'Biji kopi ini termasuk dalam kategori roasting {roast_pred_label} dengan tingkat keyakinan {roast_confidence:.2%}')
            if roast_pred_label == 'Dark':
                st.write(f'Biji {roast_pred_label} roasted adalah tingkat kematangannya paling tinggi pada proses roasting kopi.')
    
            if roast_pred_label == 'Light':
                st.write(f'Biji {roast_pred_label} roasted adalah tingkat kematangannya paling rendah pada proses roasting kopi.')
    
            if roast_pred_label == 'Medium':
                st.write(f'Biji {roast_pred_label} roasted adalah tingkat kematangannya seimbang antara light dan dark roasted pada proses roasting kopi.')
    
            if roast_pred_label == 'Green':
                st.write(f'Biji {roast_pred_label} roasted adalah biji yang belum di sangrai pada proses roasting kopi.')
    else:
        st.write(f"Gambar ini {pred_label}")

else:
    st.write('Upload gambar biji kopi di sidebar')
    st.write('Prediksi akan lebih akurat apabila gambar yang di seleksi dalam bentuk biji kopi satuan dengan background polos atau tanpa background')
    st.write('Sidebar ada di menu atas kiri pencet ini "<" Untuk membuka sidebar')