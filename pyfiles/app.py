import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import streamlit as st
import plotly.express as px
st.set_page_config(
    page_title="Changement climatique en Afrique",
    page_icon="🌍",
    layout="wide"
)

st.header("Changement climatique en Afrique")

@st.cache_data
def load_data():
    df = pd.read_csv("/Users/alphaamadoudiallo/Desktop/Changement climatique en Afrique/data/Africa_climate_change.csv")
    df['PRCP'] = df['PRCP'].fillna(df['PRCP'].median())
    df['TMIN'] = df['TMIN'].interpolate()
    df['TMAX'] = df['TMAX'].interpolate()
    df['TAVG'] = df['TAVG'].fillna((df['TMAX'] + df['TMIN']) / 2)
#Suppression de la ligne 20
    df = df.drop(index=20)
    return df

df = load_data()
st.download_button('Download the dataset', df.to_csv(index=False), 'Africa_climate_change.csv')

st.write(df)