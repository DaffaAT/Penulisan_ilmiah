import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Set page configuration
st.set_page_config(page_title="Trend Konsumsi Kopi", layout="wide")

# Title
st.title("Trend Konsumsi Kopi di Dunia")

# Load data
@st.cache_data
def load_data():
    # Baca data
    df = pd.read_csv("pages/worldwide_coffee_habits.csv")
    # Urutkan berdasarkan Country dan Year
    df = df.sort_values(['Country', 'Year'])
    return df

# Load the data
df = load_data()

# Sidebar filters
st.sidebar.header("Filters")

# Country selection
selected_countries = st.sidebar.multiselect(
    "Select Countries",
    options=sorted(df['Country'].unique()),
    default=sorted(df['Country'].unique())[:3]
)

# Year range
year_range = st.sidebar.slider(
    "Select Year Range",
    min_value=int(df['Year'].min()),
    max_value=int(df['Year'].max()),
    value=(int(df['Year'].min()), int(df['Year'].max()))
)

# Filter data based on selection
filtered_df = df[
    (df['Country'].isin(selected_countries)) &
    (df['Year'].between(year_range[0], year_range[1]))
]

# Aggregate data by year for trend analysis
yearly_total = filtered_df.groupby(['Year', 'Country']).agg({
    'Coffee Consumption (kg per capita per year)': 'sum',
    'Population (millions)': 'mean',
    'Average Coffee Price (USD per kg)': 'mean'
}).reset_index()

# Main content
col1, col2 = st.columns(2)

with col1:
    st.subheader("Distribusi Tipe Kopi Per Negara")
    # Hitung rata-rata konsumsi per negara dan jenis kopi
    avg_consumption = filtered_df.groupby(['Country', 'Type of Coffee Consumed'])['Coffee Consumption (kg per capita per year)'].mean().reset_index()
    
    fig1 = px.bar(
        avg_consumption,
        x='Country',
        y='Coffee Consumption (kg per capita per year)',
        color='Type of Coffee Consumed',
        barmode='group',
        title='Rata - Rata Konsumsi Kopi dari Jenis dan Negara',
    )
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    st.subheader("Trend Konsumsi Kopi Per Tahun")
    fig2 = px.line(
        yearly_total,  # Menggunakan data yang sudah diagregasi
        x='Year',
        y='Coffee Consumption (kg per capita per year)',
        color='Country',
        title='Trend Total Konsumsi Kopi Per Negara',
        markers=True,
    )
    # Tambahkan konfigurasi untuk memastikan tahun ditampilkan dengan benar
    fig2.update_xaxes(tickmode='linear', dtick=1)
    st.plotly_chart(fig2, use_container_width=True)

# Additional insights
st.subheader("Analisis Harga Kopi Vs Konsumsi Kopi")
fig3 = px.scatter(
    yearly_total,  # Menggunakan data yang sudah diagregasi
    x='Average Coffee Price (USD per kg)',
    y='Coffee Consumption (kg per capita per year)',
    color='Country',
    size='Population (millions)',
    hover_data=['Year'],
    title='Harga Kopi Vs Konsumsi Kopi (Ukuran Gelembung Merepresentasikan Populasi])'
)
st.plotly_chart(fig3, use_container_width=True)

# Summary statistics using aggregated data
st.subheader("Kesimpulan Statistik")
col3, col4 = st.columns(2)

with col3:
    avg_consumption = yearly_total['Coffee Consumption (kg per capita per year)'].mean()
    st.metric("Rata - Rata Total Konsumsi", f"{avg_consumption:.2f} kg/capita/year")

with col4:
    avg_price = yearly_total['Average Coffee Price (USD per kg)'].mean()
    st.metric("Harga Rata - Rata", f"${avg_price:.2f}/kg")

# Show raw data
if st.checkbox("Tampilkan Tabel Data"):
    st.subheader("Tabel Data")
    st.write("Aggregasi Data Per Tahun:")
    st.dataframe(yearly_total.sort_values(['Country', 'Year']))
    
    st.write("Data Asli:")
    st.dataframe(filtered_df.sort_values(['Country', 'Year']))
