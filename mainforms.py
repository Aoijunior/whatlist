import pickle
from pathlib import Path
import streamlit as st
import streamlit_authenticator as stauth
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import time as ts
from datetime import time
import re
import os
secret_key = os.urandom(16)

# --User Authentication--
names = ["Junior Alata", "Isabel Alata", "Maria Sihues"]
usernames = ["junioralata", "isabelalata", "mariasihues"]

# load hashed passwords
file_path = Path(__file__).parent / "hashed_pw.pkl"
with file_path.open("rb") as file:
    hashed_passwords = pickle.load(file)

authenticator = stauth.Authenticate(usernames, hashed_passwords, key=secret_key, cookie_expiry_days=30)

name, authentication_status, username = authenticator.login("Login", "main")

if authentication_status == False:
    st.error("Tu contraseña o usuario es incorrecto")

if authentication_status == None:
    st.error("Debes ingresar tu usuario y contraseña")

if authentication_status:
    st.success(f"Bienvenido {name}")
#--SideBar
authenticator.logout("Logout", "sidebar")
st.sidebar.tittle(f"Bienvenido {name}")

st.sidebar.header("Please Filter Here:")

st.markdown("<h1 style='text-align: center;'>Registro de usuario</h1>", unsafe_allow_html=True)

with st.form("Form 1"):
    col1,col2=st.columns(2)
    Name = col1.text_input("Nombres")
    Fullname = col2.text_input("Apellidos")
    nacimiento, ocupacion, sexo = st.columns(3) 
    nacimiento = nacimiento.date_input("Fecha de nacimiento", None, None, None, format="DD/MM/YYYY")
    ocupacion = ocupacion.text_input("Ocupación")
    sexo = sexo.selectbox("Sexo", ["Masculino", "Femenino", "LGBTIZKAI","Prefiero no decirlo"], None,placeholder="Selecciona una opción")
    email = st.text_input("Correo electronico")
    password = st.text_input("Contraseña", type="password")
    confi_password = st.text_input("Confirma tu contraseña", type="password")
    s_tate = st.form_submit_button("Submit")

if s_tate:
    if Name == "":
        st.error("Debes ingresar tu nombre")
    elif Fullname == "":
        st.error("Debes ingresar tu apellido")
    elif nacimiento == "":
        st.error("Debes ingresar tu fecha de nacimiento")
    elif ocupacion == "":
        st.error("Debes ingresar tu ocupación")
    elif sexo == "":
        st.error("Debes ingresar tu sexo")
    elif email == "":
        st.error("Debes ingresar tu correo electronico")
    elif password == "":
        st.error("Debes ingresar tu contraseña")
    elif len(password) < 8:
        st.error("La contraseña debe tener al menos 8 caracteres.") 
    elif not re.search("[A-Z]", password):
        st.error("La contraseña debe contener al menos una letra mayúscula.")
    elif not re.search("[!@#$%^&*()-+=]", password):
        st.error("La contraseña debe contener al menos un carácter especial (!@#$%^&*()-+=).")
    elif not re.search("[0-9]", password):
        st.error("La contraseña debe contener al menos un dígito.")
    elif confi_password == "":
        st.error("Debes confirmar tu contraseña")
    elif password != confi_password:
        st.error("Las contraseñas no coinciden")     
    else:
        st.success(f"Tu registro fue exitoso, bienvenido {Name} {Fullname}")

