import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
import numpy as np
import seaborn as sns

# Fungsi Label di plot bar
def add_labels(x, y):
    for i in range(len(x)):
        plt.text(i, y[i], y[i], ha='center')

# Fungsi untuk menghitung total pemesanan masing-masing user
def count_users(df):
    casual = df['casual'].sum()
    registered = df['registered'].sum()
    total_count = df['count'].sum()
    return casual, registered, total_count

# Fungsi membuat line plot
def make_line_plot(df_x, df_y, xlabel=None, ylabel=None, rotation=0):
    fig, ax = plt.subplots(figsize=(10, 3))
    ax.plot(df_x, df_y)
    ax.set_ylabel(ylabel)
    ax.set_xlabel(xlabel)
    ax.tick_params(axis='y', labelsize=10)
    ax.tick_params(axis='x', labelsize=10, rotation=rotation)
    st.pyplot(fig)

# Fungsi untuk menghitung total pemesanan masing-masing kategori waktu
def count_time_category(df):
    data = df[['time_category', 'count']].groupby(by='time_category').sum().reset_index()
    if data.empty:
        Morning, Afternoon, Evening, Night = 0, 0, 0, 0
    else:
        Morning = data.loc[data['time_category'] == 'Morning', 'count'].values[0]        
        Afternoon = data.loc[data['time_category'] == 'Afternoon', 'count'].values[0]
        Evening = data.loc[data['time_category'] == 'Evening', 'count'].values[0]
        Night = data.loc[data['time_category'] == 'Night', 'count'].values[0]
    return Morning, Afternoon, Evening, Night

# Fungsi membuat bar plot
def make_bar_plot(df_x, df_y, xlabel=None, ylabel=None, rotation=0):
    fig, ax = plt.subplots(figsize=(6, 6))
    ax.bar(df_x, df_y, color='#72BCD4')
    ax.tick_params(axis='x', labelsize=10, rotation=rotation)
    ax.set_ylabel(ylabel)
    ax.set_xlabel(xlabel)
    add_labels(df_x, df_y)
    st.pyplot(fig)

# Membaca File csv
day_df = pd.read_csv("dashboard/day_clean.csv")
hour_df = pd.read_csv("dashboard/hour_clean.csv")

# Mengolah data
day_df.sort_values(by="rental_date", inplace=True)
hour_df.sort_values(by="rental_date", inplace=True)
day_df['rental_date'] = pd.to_datetime(day_df['rental_date'])
hour_df['rental_date'] = pd.to_datetime(hour_df['rental_date'])

# Membuat Sidebar 
min_date = hour_df["rental_date"].min()
max_date = hour_df["rental_date"].max()
with st.sidebar:
    st.image("dashboard/downoad.png")

    # Membuat filter rentang tanggal
    start_date, end_date = st.date_input(
        label='time span', min_value=min_date, max_value=max_date, value=[min_date, max_date]
    )

# Mengolah data sesuai rentang tanggal yang diinput
main_day_df = day_df[(day_df["rental_date"] >= str(start_date)) & (day_df["rental_date"] <= str(end_date))]
main_hour_df = hour_df[(hour_df["rental_date"] >= str(start_date)) & (hour_df["rental_date"] <= str(end_date))]

# Dashboard
st.title('Welcome To Rental Bersama IMA :sparkles:')
st.markdown("""---""")

# Membuat Grafik pemesanan harian
st.header('Daily Rentals :date:')
tab1, tab2, tab3 = st.tabs(["ALL", "holiday", "working day"])
# Grafik jumlah rental di semua hari (sesuai rentang yang diinput)
with tab1:
    casual, registered, count = count_users(main_day_df)
    col1, col2, col3 = st.columns(3)
    with col1:
        st.write("Casual User")
        st.subheader(casual)
    with col2:
        st.write("Registered User")
        st.subheader(registered)    
    with col3:
        st.write("Count")
        st.subheader(count)
    make_line_plot(main_day_df['rental_date'], main_day_df['count'], None, None, 45) 
# Grafik jumlah rental di hari libur (sesuai rentang yang diinput)
with tab2:
    df_holiday = main_day_df[main_day_df['holiday'] == 1]
    casual, registered, count = count_users(df_holiday)
    col1, col2, col3 = st.columns(3)
    with col1:
        st.write("Casual User")
        st.subheader(casual)
    with col2:
        st.write("Registered User")
        st.subheader(registered)    
    with col3:
        st.write("Count")
        st.subheader(count)
    make_line_plot(df_holiday['rental_date'], df_holiday['count'], None, None, 45)
# Grafik jumlah rental di hari kerja (sesuai rentang yang diinput)
with tab3:
    df_workday = main_day_df[main_day_df['workingday'] == 1]
    casual, registered, count = count_users(df_workday)
    col1, col2, col3 = st.columns(3)
    with col1:
        st.write("Casual User")
        st.subheader(casual)
    with col2:
        st.write("Registered User")
        st.subheader(registered)    
    with col3:
        st.write("Count")
        st.subheader(count)
    make_line_plot(df_workday['rental_date'], df_workday['count'], None, None, 45)

# Membuat Grafik pemesanan berdasarkan kategori waktu
