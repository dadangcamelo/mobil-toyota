import pickle
import streamlit as st
import time

st.set_page_config(page_title="Prediksi Harga Mobil", page_icon="🚗")

model = pickle.load(open('prediksi_hargamobil.sav', 'rb'))

st.markdown("<h1 style='text-align: center;'>Estimasi Prediksi Harga Mobil Toyota Bekas</h1>", unsafe_allow_html=True)

st.image('mobil1.png', use_column_width=True)

# Menambahkan opsi untuk model mobil
car_models = [
    'GT86', 'Corolla', 'RAV4', 'Yaris', 'Auris', 'Aygo', 
    'C-HR', 'Prius', 'Avensis', 'Verso', 'Hilux', 
    'PROACE VERSO', 'Land Cruiser', 'Supra', 'Camry', 'IQ', 
    'Urban Cruiser'
]
selected_model = st.selectbox('Pilih Model Mobil', car_models)

# Menambahkan opsi untuk jenis transmisi
transmission_options = ['Manual', 'Automatic', 'Semi-Auto']
transmission = st.selectbox('Pilih Jenis Transmisi Mobil', transmission_options)

# Menambahkan opsi untuk jenis mesin
engine_types = ['Petrol', 'Diesel', 'Hybrid', 'Other']
selected_engine_type = st.selectbox('Pilih Jenis Mesin Mobil', engine_types)

year = st.number_input('Input Tahun Keluaran Mobil', min_value=0, step=1, format="%d")
mileage = st.number_input('Input Jarak Tempuh Mobil (Kilometer)')
tax = st.number_input('Input Biaya Pajak Mobil (Euro)')
mpg = st.number_input('Input Konsumsi BBM Mobil (Liter)')
engineSize = st.number_input('Input Engine Size Mobil')

def format_number_with_dots(number):
    # Convert the number to an integer to remove decimal digits
    integer_value = int(number)
    # Format the integer with dots as a thousands separator
    return "{:,}".format(integer_value).replace(",", ".")

if st.button('Prediksi Harga Mobil Bekas', key='predict_button'):
    if year == 0 or mileage == 0 or tax == 0 or mpg == 0 or engineSize == 0:
        st.warning("Input data terlebih dahulu")
    else:
        with st.empty():
            st.info("Sedang memproses prediksi...")
            with st.spinner():
                time.sleep(2)
            st.success("Selesai!")
            time.sleep(1)

        # Faktor untuk transmisi
        transmission_factor = 1.0  # Default factor
        if transmission == 'Automatic':
            transmission_factor = 1.1  # Misalnya, harga lebih tinggi untuk transmisi otomatis
        elif transmission == 'Semi-Auto':
            transmission_factor = 1.05  # Misalnya, harga sedikit lebih tinggi untuk semi-otomatis

        # Faktor untuk model mobil
        model_factor = 1.0  # Default factor
        if selected_model in ['GT86', 'Supra']:
            model_factor = 1.2  # Misalnya, model sport lebih mahal
        elif selected_model in ['Corolla', 'Yaris']:
            model_factor = 0.9  # Misalnya, model ini lebih terjangkau

        # Faktor untuk jenis mesin
        engine_type_factor = 1.0  # Default factor
        if selected_engine_type == 'Diesel':
            engine_type_factor = 1.1  # Misalnya, harga lebih tinggi untuk mesin diesel
        elif selected_engine_type == 'Hybrid':
            engine_type_factor = 1.15  # Misalnya, harga lebih tinggi untuk mesin hybrid
        elif selected_engine_type == 'Other':
            engine_type_factor = 0.95  # Misalnya, harga lebih rendah untuk jenis mesin lain

        # Menghitung prediksi dengan mempertimbangkan faktor transmisi, model, dan jenis mesin
        predict = model.predict([[year, mileage, tax, mpg, engineSize]])
        predicted_price_in_euro = predict[0] * transmission_factor * model_factor * engine_type_factor
        predicted_price_in_rupiah = predicted_price_in_euro * 16741  # Mengonversi ke Rupiah

        st.write('Prediksi Harga Mobil Bekas dalam EURO adalah', format_number_with_dots(predicted_price_in_euro))
        st.write('Prediksi Harga Mobil Bekas dalam Rupiah adalah', format_number_with_dots(predicted_price_in_rupiah))

        formatted_price = format_number_with_dots(predicted_price_in_rupiah)
        st.success(f"Harga mobil bekas berdasarkan data di atas adalah Rp {formatted_price}.")
        
def add_bg_from_url():
    st.markdown(
         f"""
         <style>
         .stApp {{
             background-image: url("https://img.freepik.com/free-vector/dark-black-background-with-silver-lines_1017-31886.jpg?t=st=1737613709~exp=1737617309~hmac=4d2aec882e5e419450b2d7e79a006d6a6854c229b62a5b7237e9582ecfa10dd2&w=1380");
             background-attachment: fixed;
             background-size: cover;
         }}
         </style>
         """,
         unsafe_allow_html=True
     )

add_bg_from_url()