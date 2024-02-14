import streamlit as st
import streamlit_authenticator as stauth
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
from datetime import time
import re
from streamlit_option_menu import option_menu
import time as ts
import webbrowser as web
import pyautogui as pg
import requests
import json


# Función para aplicar filtro básico
def filtro_basico(df, columna, valores):
    if valores:
        return df[df[columna].isin(valores)]
    else:
        return df

# Función para aplicar filtro avanzado
def filtro_avanzado(df, columna, logica, valor):
    if logica == 'Mayor':
        return df[df[columna] > valor]
    elif logica == 'Mayor o igual':
        return df[df[columna] >= valor]
    elif logica == 'Menor':
        return df[df[columna] < valor]
    elif logica == 'Menor o igual':
        return df[df[columna] <= valor]
    elif logica == 'Igual':
        return df[df[columna] == valor]
    elif logica == 'Diferente':
        return df[df[columna] != valor]

# Detectar el separador de un archivo CSV
def detectar_separador_csv(file):
    # Leer las primeras líneas del archivo para detectar el separador
    lineas = file.getvalue().decode().split('\n')
    for linea in lineas:
        if ',' in linea:
            return ','
        elif ';' in linea:
            return ';'
    # Si no se encuentra ninguna coma ni punto y coma, asumir que el separador es coma
    return ','


# Función para leer archivos
def leer_archivo(file):
    if file is not None:
        # Leer archivos CSV y TXT
        if file.type == 'text/csv' or file.type == 'text/plain':
            # Detectar el separador del archivo CSV
            separador = detectar_separador_csv(file)
            # Leer el archivo CSV con el separador detectado
            df = pd.read_csv(file, sep=separador)
            return df
        # Leer archivos Excel (XLSX y XLSM)
        elif file.type == 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet' or file.type == 'application/vnd.ms-excel':
            df = pd.read_excel(file)
            return df
        # Leer archivos JSON
        elif file.type == 'application/json':
            df = pd.DataFrame(json.load(file))
            return df
        else:
            st.write("Formato de archivo no válido. Por favor, sube un archivo CSV, TXT, XLSX, XLSM o JSON.")




# INICIO DE LA APLICACIÓN (Menu de navegación)
selected2 = option_menu(None, ["Inicio", "Registro", "Iniciar Sesión", "Gmail-Bot", 'Whatsapp-Bot', 'Settings'], 
    icons=['house','person-fill-add', 'person', "google", "whatsapp",'gear'], 
    menu_icon="cast", default_index=0, orientation="horizontal")

# Condicionales para la selección de las opciones de navegación
if selected2 == "Inicio":

    # Estilo CSS para personalizar la apariencia
    css_style = """
        <style>
            /* Estilo cyberpunk */
            body {
                background-color: #0f0f0f;
                color: #00ff00;
            }
            h1, h2, p {
                font-family: 'Courier New', monospace;
            }
            /* Estilo centrado horizontalmente */
            .center-text {
                text-align: center;
            }
            /* Estilo de borde para columnas */
            .column-border {
                border: 2px solid #00ff00;
                padding: 10px;
                border-radius: 10px;
                margin-bottom: 20px;
            }
            /* Estilo para ajustar la altura de los títulos y centrarlos verticalmente */
            .column-title {
                height: 80px; /* Ajusta esta altura según sea necesario */
                display: flex;
                justify-content: center;
                align-items: center;
                margin: 0; /* Elimina el margen para una mejor alineación */
            }
            /* Estilo para alinear verticalmente las imágenes */
            .column-img {
                display: flex;
                justify-content: center;
                align-items: center;
                margin: 0; /* Elimina el margen para una mejor alineación */
            }
            /* Estilo para alinear el texto */
            .column-text {
                text-align: justify;
            }
        </style>
    """

    # Aplicar el estilo CSS
    st.markdown(css_style, unsafe_allow_html=True)

    # Título principal
    st.markdown("<h1 style='text-align: center;'>Bienvenido a la primera plataforma de RPA para CyC Gestión</h1>", unsafe_allow_html=True)
    st.write("En esta plataforma podrás encontrar diferentes herramientas para la automatización de procesos")

    # División en columnas
    col1, col2, col3 = st.columns(3)

    # Contenido de las columnas
    with col1:
        st.markdown("<h2 class='column-title center-text'>Bot de Gmail</h2>", unsafe_allow_html=True)
        st.markdown("<p class='column-text'>Con este Bot podrás enviar correos masivos con mensajes personalizados, e incluso adjuntar archivos de manera personalizada.</p>", unsafe_allow_html=True)
        st.markdown("<div class='column-img'><img src='https://img.icons8.com/ios-filled/50/00ff00/gmail.png' alt='Gmail Icon'/></div>", unsafe_allow_html=True)

    with col2:
        st.markdown("<h2 class='column-title center-text'>Whatsapp Bot</h2>", unsafe_allow_html=True)
        st.markdown("<p class='column-text'>Con este bot de Gmail podrás automatizar los mensajes de Whatsapp utilizando el módulo OS.</p>", unsafe_allow_html=True)
        st.markdown("<div class='column-img'><img src='https://img.icons8.com/fluent/50/00ff00/whatsapp.png' alt='Whatsapp Icon'/></div>", unsafe_allow_html=True)

    with col3:
        st.markdown("<h2 class='column-title center-text'>Conversor de archivos</h2>", unsafe_allow_html=True)
        st.markdown("<p class='column-text'>Esta herramienta aún está en desarrollo, pero te permitirá manipular los archivos y convertirlos al formato que desees en un futuro.</p>", unsafe_allow_html=True)
        st.markdown("<div class='column-img'><img src='https://img.icons8.com/ios-filled/50/00ff00/document.png' alt='File Icon'/></div>", unsafe_allow_html=True)


elif selected2 == "Registro":
     # --Formulario de Registro--
    st.markdown("<h1 style='text-align: center;'>Registro de usuario</h1>", unsafe_allow_html=True)

    with st.form("Form 1"):
        col1, col2 = st.columns(2)
        Name = col1.text_input("Nombres")
        Fullname = col2.text_input("Apellidos")
        nacimiento, ocupacion, sexo = st.columns(3) 
        nacimiento = nacimiento.date_input("Fecha de nacimiento", None, None, None, format="DD/MM/YYYY")
        ocupacion = ocupacion.text_input("Ingresa tu username")
        sexo = sexo.selectbox("Sexo", ["Masculino", "Femenino", "LGBTIZKAI","Prefiero no decirlo"], None,placeholder="Selecciona una opción")
        email = st.text_input("Correo electronico")
        password = st.text_input("Contraseña", type="password")
        confi_password = st.text_input("Confirma tu contraseña", type="password")
        s_tate = st.form_submit_button("Registrarse")

    if s_tate:
        if Name == "":
            st.error("Debes ingresar tu nombre")
        elif Fullname == "":
            st.error("Debes ingresar tu apellido")
        elif nacimiento == "":
            st.error("Debes ingresar tu fecha de nacimiento")
        elif ocupacion == "":
            st.error("Ingresa tu username")
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
elif selected2 == "Iniciar Sesión":
     # --Inicio de sesión--
    st.markdown("<h1 style='text-align: center;'>Iniciar Sesión</h1>", unsafe_allow_html=True)

    with st.form("Form 1"):
        username = st.text_input("Usuario")
        password = st.text_input("Contraseña", type="password")
        s_tate = st.form_submit_button("Iniciar sesión")
elif selected2 == "Gmail-Bot":
    st.markdown("<h1 style='text-align: center;'>El Karma es mi papá (Bot de Whatsapp)</h1>", unsafe_allow_html=True)
    
    st.write("Este bot te permite enviar mensajes personalizados a través de WhatsApp Web.")
    exp = st.expander("Instrucciones", expanded=True)
    exp.write("1. Sube tu archivo con los datos de los contactos, de preferencia en formato xlsx o csv.")
    exp.write("2. Confirma los valores que deseas filtrar.")
    exp.write("3. Revisa en la tabla que contenga las personas deseadas.")
    exp.write("4. Ingresa tu mensaje personalizado, donde las variables se pueden llamar entre llaves, por ejemplo: Hola {nombre}, tu supervisor es {supervisor}.")
    exp.write("5. Presiona CTRL + ENTER, para previsualizar el mensaje.")
    exp.write("6. Si todo está correcto, presiona el botón 'Enviar mensaje' e iniciar el programa.")
    exp.write("7. El programa utiliza el modulo OS para poder realizar la automatización por lo tanto no cierres la ventana de WhatsApp Web y no manipules la computadora hasta que se termine de enviar todo los mensajes.")
    file = st.file_uploader("Sube tu archivo", type=["csv","txt","xlsx","xlmx", "json"])
    
elif selected2 == "Whatsapp-Bot":

    st.markdown("<h1 style='text-align: center;'>El Karma is my ... (Bot de Whatsapp)</h1>", unsafe_allow_html=True)
    
    st.write("Este bot te permite enviar mensajes personalizados a través de WhatsApp Web.")
    exp = st.expander("Instrucciones", expanded=True)
    exp.write("1. Sube tu archivo con los datos de los contactos, de preferencia en formato xlsx o csv.")
    exp.write("2. Confirma los valores que deseas filtrar.")
    exp.write("3. Revisa en la tabla que contenga las personas deseadas.")
    exp.write("4. Ingresa tu mensaje personalizado, donde las variables se pueden llamar entre llaves, por ejemplo: Hola {nombre}, tu supervisor es {supervisor}.")
    exp.write("5. Presiona CTRL + ENTER, para previsualizar el mensaje.")
    exp.write("6. Si todo está correcto, presiona el botón 'Enviar mensaje' e iniciar el programa.")
    exp.write("7. El programa utiliza el modulo OS para poder realizar la automatización por lo tanto no cierres la ventana de WhatsApp Web y no manipules la computadora hasta que se termine de enviar todo los mensajes.")
    file, file2 = st.columns(2)
    file = file.file_uploader("Sube tu primer archivo", type=["csv","txt","xlsx","xlmx", "json"])
    file2 = file2.file_uploader("Sube tu segundo archivo", type=["csv","txt","xlsx","xlmx", "json"])

    # Lista de filtros
    df = leer_archivo(file)  # Cambia el método de lectura según el tipo de archivo
    df_2 = leer_archivo(file2)  # Cambia el método de lectura según el tipo de archivo
    if "filtros" not in st.session_state:
            st.session_state.filtros = []

    # Seleccionar tipo de filtro
    filtro = st.selectbox("Tipo de filtro", ["Básico", "Avanzado"], key="tipo_filtro")

    # Botón para agregar filtro
    if st.button("Agregar filtro"):
            st.session_state.filtros.append(filtro)

    # Mostrar filtros
    for i, filtro in enumerate(st.session_state.filtros):
            st.markdown(f"> Filtro {i+1}")
            if filtro == "Básico":
                columna, valores = st.columns(2)
                columna = columna.selectbox("Selecciona la columna", df.columns, key=f"columna_basico_{i}")
                valores = valores.multiselect("Selecciona los valores", df[columna].unique(), key=f"valores_basico_{i}")
                df = filtro_basico(df, columna, valores)
            elif filtro == "Avanzado":
                col1, col2, col3 = st.columns(3)
                columna = col1.selectbox("Selecciona la columna", df.columns, key=f"columna_avanzado_{i}")
                logica = col2.selectbox("Selecciona la lógica", ['None','Mayor', 'Mayor o igual', 'Menor', 'Menor o igual', 'Igual', 'Diferente'], key=f"logica_avanzado_{i}")
                valor = col3.number_input("Ingresa el valor", step=1, key=f"valor_avanzado_{i}")
                df = filtro_avanzado(df, columna, logica, valor)
            
            # Botón para eliminar filtro
            if st.button(f"Eliminar filtro {i+1}"):
                del st.session_state.filtros[i]

    # Aplicar filtros al presionar un botón
    st.table(df)

                
    mensaje = st.text_area("Ingresa tu mensaje, recuerda que los saltos de linea se hacen con '%0A' ")
    if mensaje is not None:
            # Iterar sobre cada fila del dataframe filtrado
        for index, row in df.iterrows():
                # Obtener el nombre y apellido de cada fila
                ejecutivo = row["EJECUTIVO"]
                supervisor = row["SUPERVISORES"]
                
                # Formatear el mensaje con los valores del dataframe
                mensaje_formateado = (mensaje.format(nombre=ejecutivo, supervisor=supervisor))
                
                # Mostrar el mensaje formateado
                st.write(mensaje_formateado)

        # Crear un botón
    clicked = st.button("Enviar mensaje")

        # Verificar si el botón ha sido clickeado
    if clicked:
            # Aquí va tu script
            for i in range(len(df)):
                # Verificar si el dataframe filtrado no está vacío
                if not df.empty:
                    celular = str(df.iloc[i]['NUMERO'])  # Convertir a string para que se añada al mensaje
                    nombre = df.iloc[i]['EJECUTIVO']
                    producto = str(df.iloc[i]['DNI'])  # Convertir a string para que se añada al mensaje
                    supervisor = df.iloc[i]['SUPERVISORES']
                    
                    # Crear mensaje personalizado
                    mensaje_personalizado = requests.utils.quote(mensaje.format(nombre=nombre, supervisor=supervisor, producto=producto))
                    
                    # Aquí irían las acciones para enviar el mensaje por WhatsApp
                    # (puedes agregar el código que usas para abrir WhatsApp Web, escribir y enviar el mensaje)
                    # Por simplicidad, he omitido estas acciones en este ejemplo
                    chrome_path = r"C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe %s"
                    web.open("https://web.whatsapp.com/send?phone=" + celular + "&text=" + mensaje_personalizado)
                    
                    ts.sleep(9)           # Esperar 8 segundos a que cargue
                    pg.click(1230,964)      # Hacer click en la caja de texto
                    ts.sleep(2)           # Esperar 2 segundos 
                    pg.press('enter')       # Enviar mensaje 
                    ts.sleep(3)           # Esperar 3 segundos a que se envíe el mensaje
                    pg.hotkey('ctrl', 'w')  # Cerrar la pestaña
                    ts.sleep(2)
                else:
                    st.write("El DataFrame filtrado está vacío. No se pueden enviar mensajes.")
else:
    pass