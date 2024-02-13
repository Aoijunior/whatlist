import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import time as ts
from datetime import time


def new_section(Titulo, texto):
    st.markdown("---")
    st.markdown(Titulo)
    st.markdown(texto)

st.markdown("# Uploading Files")
st.markdown("En esta sección te permite subir archivos")
st.markdown("---")
dat = st.file_uploader("Please upload an file", type=["csv","txt","xls","png"])
df = pd.read_csv(dat, sep=";")

if dat is not None:
    st.table(df)
else:
    pass

column_select = st.selectbox("Select a column", df.columns)

if column_select == "Apellido":
    seleccion_ape = st.selectbox("Slecciona el valor", df["Apellido"].unique())
    st.write(f"Seleccionaste la siguiente opción {seleccion_ape}")
elif column_select == "Nombre":
    seleccion_nom = st.selectbox("Selecciona el valor", df["Nombre"].unique())
    st.write(f"Seleccionaste la siguiente opción {seleccion_nom}")
else:
    pass

new_section("# Esto es un slider", "Esto es un nuevo widget que da una linea de valores deslizables del 1 al 100")
def slider():
    print(st.session_state.slider)

val = st.slider("Escoge un valor", 1, 100, key="slider", on_change=slider)
st.write(f"El valor seleccionado es {val}")

new_section("# Esto es un input", "Esto es un nuevo widget que da un espacio para ingresar texto")
def input():
    print(st.session_state.input)

text = st.text_input("Ingresa un texto", key="input", on_change=input)
st.write(f"El texto ingresado es {text}")

new_section("# Estos es un area de texto", "Esto es un nuevo widget que da un espacio para ingresar texto")
def textarea():
    print(st.session_state.textarea)

text_area = st.text_area("Ingresa un texto", key="textarea", on_change=textarea)

new_section("# Esto es un date input", "Esto es un nuevo widget una fecha")
def date():
    print(st.session_state.date)
    
date = st.date_input("Ingresa una fecha, el formato es Año/Mes/Día", key="date", on_change=date)
st.write(f"La fecha seleccionada es {date}")

new_section("# Esto es un time input", "Esto es un nuevo widget para ingresar la hora")
def time():
    print(st.session_state.time)

time = st.time_input("Ingresa una hora, el formato es Hora:Minutos", key="time", on_change=time)
st.write(f"La hora seleccionada es {time}")

new_section("# Esto es un progress bar", "Esto es un nuevo widget que genera una barra de progreso")
def progress():
    print(st.session_state.progress)
def converter(value):
    m,s,mm = value.split(":")
    t_s = int(m)*60 + int(s) + int(mm)/1000
    return t_s

bar = st.progress(0)
for i in range(10):
    bar.progress((i+1)*10)
    
    ts.sleep(0.1)
