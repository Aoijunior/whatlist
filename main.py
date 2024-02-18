import streamlit as st
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

# Función para formatear el mensaje con los valores del DataFrame
def formatear_mensaje(mensaje, df):
    if df is not None:    
        # Expresión regular para encontrar las variables dentro del mensaje
        patron = r'{([^{}]*)}'
        coincidencias = re.findall(patron, mensaje)

        mensajes_formateados = []  # Lista para almacenar los mensajes formateados y los números de celular

        # Iterar sobre cada fila del DataFrame
        for index, fila in df.iterrows():
            mensaje_formateado = mensaje  # Iniciar con el mensaje original
            # Reemplazar cada variable en el mensaje con el valor correspondiente de la fila
            for variable in coincidencias:
                # Obtener el valor de la variable de la fila actual
                valor_variable = fila.get(variable.strip(), '')
                # Reemplazar la variable con su valor en el mensaje formateado
                mensaje_formateado = mensaje_formateado.replace("{" + variable + "}", str(valor_variable))
            # Agregar el mensaje formateado y el número de celular a la lista de mensajes formateados
            mensajes_formateados.append((mensaje_formateado, fila['Numero']))
    else:
        mensajes_formateados = [("No se ha cargado ningún archivo.", "")] # Si no se ha cargado un archivo, agregar un mensaje de error

    return mensajes_formateados

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

#################### AQUI INIICA LA APLICACIÓN ####################

st.markdown("<h1 style='text-align: center;'>(Bot de Whatsapp)</h1>", unsafe_allow_html=True)
    
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

                
# Componente de entrada de texto para el mensaje
mensaje = st.text_area("Ingresa tu mensaje, para personalizarlo, escribe los nombres de las columnas entre llaves, por ejemplo: Hola {EJECUTIVO}, tu supervisor es {SUPERSIVOR}.")

    # Si se ha ingresado un mensaje
if mensaje is not None:
        # Formatear el mensaje con los valores del DataFrame
        mensaje_formateado = formatear_mensaje(mensaje, df)
        
        # Mostrar el mensaje formateado
        st.write(mensaje_formateado)

        # Crear un botón
# Crear un botón
clicked = st.button("Enviar mensaje")

# Verificar si el botón ha sido clickeado
if clicked:
    # Aquí va tu script
    for mensaje, celular in mensaje_formateado:
        # Verificar si el mensaje o el número de celular no están vacíos
        if mensaje and celular:
            # Crear mensaje personalizado
            mensaje_personalizado = requests.utils.quote(mensaje.encode('utf-8'))

            # Aquí irían las acciones para enviar el mensaje por WhatsApp
            # (puedes agregar el código que usas para abrir WhatsApp Web, escribir y enviar el mensaje)
            # Por simplicidad, he omitido estas acciones en este ejemplo
            chrome_path = r"C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe %s"
            web.open("https://web.whatsapp.com/send?phone=" + str(celular) + "&text=" + mensaje_personalizado)
                
            ts.sleep(11)           # Esperar 8 segundos a que cargue
            pg.click(1230,964)      # Hacer click en la caja de texto
            ts.sleep(3)           # Esperar 2 segundos 
            pg.press('enter')       # Enviar mensaje 
            ts.sleep(3)           # Esperar 3 segundos a que se envíe el mensaje
            pg.hotkey('ctrl', 'w')  # Cerrar la pestaña
            ts.sleep(2)
        else:
            st.write("El mensaje o el número de celular están vacíos. No se pueden enviar mensajes.")