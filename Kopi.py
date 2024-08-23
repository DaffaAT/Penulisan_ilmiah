import streamlit as st
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
from tensorflow.keras.models import Model, load_model
from tensorflow.keras.preprocessing.image import load_img, img_to_array

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
    
st.title('Website Klasifikasi Biji Kopi')

st.subheader('Jenis Biji Kopi ada apa saja?')
st.write('-Robusta')
st.write('-Arabika')
st.write('-Liberika')

st.subheader('Apa itu Kopi Arabika?')
st.write('Kopi Arabika adalah kopi yang populer di dunia. Kopi terkenal karena rasanya yang halus dan aromanya yang komplex. Ciri-Ciri Kopi Arabika memiliki kandungan asam yang lebih tinggi dan rasa yang lebih kayak di banding dengan jenis kopi lainnya.')
st.write('Kopi ini di namakan Arabika karena pada abad ke-7 biji kopi ini dibawa dari sebuah dataran rendah di Arab. Arabika ditanam di berbagai wilayah di seluruh dunia, terutama di daerah pegunungan dengan iklim sejuk dan curah hujan yang cukup. ')
st.subheader('Apa itu Kopi Robusta?')
st.write('Kopi Robusta adalah salah satu jenis kopi yang paling umum dibudidayakan di dunia. Robusta berasal dari tanaman kopi Coffea canephora, yang dikenal lebih tahan terhadap penyakit dan dapat tumbuh di dataran yang lebih rendah serta di iklim yang lebih panas. Seperti di Vietnam, Brasil, Indonesia dan India.')
st.subheader('Apa itu Kopi Liberika?')
st.write('Kopi Liberika adalah salah satu jenis kopi utama yang dibudidayakan secara komersial di dunia. Kopi ini berasal dari tanaman kopi Coffea liberica, yang pertama kali ditemukan di Liberia, Afrika Barat, dan sekarang juga dibudidayakan di berbagai daerah tropis lainnya. ')

st.subheader('Apa itu Roast level?')
st.write('Roast level adalah indikator warna dari biji kopi dan secara mendasar roast level di bedakan menjadi 4 level:')
st.write('Green bean atau biji yang belum disangrai/roasted')
st.write('Light roasted')
st.write('Medium roasted')
st.write('Dark roasted')

st.subheader('Light Roasted')
st.write('Light roast adalah sebuah teknik roasting yang memiliki tingkat kematangan paling rendah. Biji kopi yang telah disangrai beberapa menit akan sedikit mengembang.Pada proses ini menghasilkan rasa yang asam, namun aroma sangrai kurang tercium. Biji kopi berubah menjadi warna coklat terang karena proses penyerapan panas yang dilakukan tidak terlalu lama, biji kopi juga tidak mengeluarkan minyak dan cenderung kering. Suhu biji kopi sekitar 180°C-205°C. Pada suhu sekitar 205°C terjadi first crack dan proses roasting selesai. ')
st.write('Istilah lain untuk level sangrai seperti ini adalah Half City, Light City, New England, atau Cinnamon.')

st.subheader('Medium Roasted')
st.write('Medium roast adalah teknik yang paling sering digunakan. Proses ini membutuhkan waktu selama 6-8 menit. Biji kopi yang dihasilkan akan lebih gelap dari light roast dan lebih terang dari dark roast. Biji kopi pada proses ini menghasilkan rasa manis dan kafein yang rendah. Serta kamu bisa mencium aroma asap penyangraian karena biji kopi banyak mengeluarkan asap. Pada proses ini, biji kopi juga tidak mengeluarkan minyak pada permukaannya. Suhu biji kopi pada kisaran 210°C dan 220°C. Pada suhu tersebut, terjadi first crack. Proses roasting akan berhenti sebelum terjadi second crack.')
st.write('Istilah lain untuk level roasting ini adalah City, Breakfast, Regular, dan American.')

st.subheader('Dark Roasted')
st.write('Dark roast adalah tingkatan paling matang pada proses roasting kopi. Jangan coba untuk melebihi tingkatan ini karena kopi akan tidak enak. Warna biji kopi yang dihasilkan lebih gelap dibanding tingkatan lainnya. Biji kopi akan mengeluarkan minyak di permukannya. Rasa kopi cenderung pahit dan menutupi rasa khas kopi. Proses dark roast selesai di roasting ketika terjadi second crack yaitu sekitar suhu sekita 240°C.')
st.write('Istilah lain untuk level roasting ini adalah High, Continental, New Orleans, European, Espresso, Viennese, Italian, French.')
st.markdown("---")
st.subheader('Model yang digunakan')
st.write('Website ini menggunakan model machine learning yang di latih dengan metode Convolutional Neural Networks(CNN)')
st.write('Convolutional Neural Networks (CNN) adalah jenis model deep learning yang sangat cocok untuk mengelola gambar.')
st.write('Model CNN memproses gambar melalui beberapa lapisan yang mendeteksi fitur-fitur seperti tepi, tekstur, dan pola, hingga akhirnya menentukan kategori dan memberikan skor keyakinan untuk prediksi tersebut.')

# Mengunggah file gambar di sidebar
st.sidebar.subheader('Upload Gambar Biji kopi anda disini')
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
    st.write('Sidebar ada di menu atas kiri pencet ini "<" Untuk membuka sidebar')