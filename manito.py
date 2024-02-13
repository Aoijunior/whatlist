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

#Condicionales para la selección de las opciones de navegación
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
    file = st.file_uploader("Sube tu archivo", type=["csv","txt","xlsx","xlmx", "json"])
    

    if file is not None:
        file_1 = leer_archivo(file)
        file_c1 = file_1.columns[0]
        file_c2 = file_1.columns[1]
        file_c3 = file_1.columns[2]
        file_c4 = file_1.columns[3]
        file_c5 = file_1.columns[4]
        # Filtrar el dataframe file_1 basado en los valores seleccionados
        columna, valor, genero = st.columns(3)
        columna_seleccionada = columna.selectbox("Selecciona la columna", file_1.columns.unique())
        columna_genero = genero.selectbox("Selecciona la columna", file_1[file_c4].unique(), None)
        valores_seleccionados = valor.multiselect("Selecciona los valores", file_1[columna_seleccionada].unique(), None)
        if valores_seleccionados:
            file_filtrado = file_1[file_1[columna_seleccionada].isin(valores_seleccionados)]
        elif columna_genero:
            file_filtrado = file_1[file_1["GENERO"] == columna_genero]
        else:
            file_filtrado = file_1
            
        st.table(file_filtrado)
                
        mensaje = st.text_area("Ingresa tu mensaje, recuerda que los saltos de linea se hacen con '%0A' ")
        if mensaje is not None:
            # Iterar sobre cada fila del dataframe filtrado
            for index, row in file_filtrado.iterrows():
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
            for i in range(len(file_filtrado)):
                # Verificar si el dataframe filtrado no está vacío
                if not file_filtrado.empty:
                    celular = str(file_filtrado.iloc[i]['NUMERO'])  # Convertir a string para que se añada al mensaje
                    nombre = file_filtrado.iloc[i]['EJECUTIVO']
                    producto = str(file_filtrado.iloc[i]['DNI'])  # Convertir a string para que se añada al mensaje
                    supervisor = file_filtrado.iloc[i]['SUPERVISORES']
                    
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