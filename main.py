import streamlit as st
import pandas as pd
from datetime import time
import re
import time as ts
import webbrowser as web
import pyautogui as pg
import requests
import json

# Configuración de la página
st.set_page_config(layout="wide")

################## AQUI INICIA LAS FUNCINES PARA EL BOT DE WHATSAPP ##################

# Función para formatear el mensaje con los valores del DataFrame
def formatear_mensaje(mensaje, df):
    """
    Función para formatear un mensaje con valores de un DataFrame.

    Args:
        mensaje (str): El mensaje con variables a formatear.
        df (DataFrame): El DataFrame que contiene los valores para las variables.

    Returns:
        list: Una lista de tuplas con mensajes formateados y números de celular.
    """
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
            mensajes_formateados.append((mensaje_formateado, fila['NUMERO']))
    else:
        mensajes_formateados = [("No se ha cargado ningún archivo.", "")] # Si no se ha cargado un archivo, agregar un mensaje de error

    return mensajes_formateados

# Función para aplicar filtro básico
def filtro_basico(df, columna, valores):
    """
    Aplica un filtro básico a un DataFrame.

    Args:
        df (DataFrame): El DataFrame al que se le aplicará el filtro.
        columna (str): El nombre de la columna en la que se aplicará el filtro.
        valores (list): La lista de valores que se usarán para filtrar la columna.

    Returns:
        DataFrame: El DataFrame filtrado.
    """
    if valores:
        return df[df[columna].isin(valores)]
    else:
        return df

# Función para aplicar filtro avanzado
def filtro_avanzado(df, columna, logica, valor):
    """
    Aplica un filtro avanzado a un DataFrame.

    Args:
        df (DataFrame): El DataFrame al que se le aplicará el filtro.
        columna (str): El nombre de la columna en la que se aplicará el filtro.
        logica (str): La operación lógica a aplicar (Mayor, Mayor o igual, Menor, Menor o igual, Igual, Diferente).
        valor (int): El valor con el que se comparará la columna.

    Returns:
        DataFrame: El DataFrame filtrado.
    """
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
    """
    Detecta el separador de un archivo CSV.

    Args:
        file (file): El archivo CSV.

    Returns:
        str: El separador detectado (',' o ';').
    """
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
    """
    Lee un archivo y devuelve un DataFrame.

    Args:
        file (file): El archivo a leer.

    Returns:
        DataFrame: El DataFrame generado a partir del archivo.
    """
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

#################### AQUI INICIA LA APLICACIÓN ####################

# Configuración de la interfaz de usuario

# Agregar el título con el icono de WhatsApp utilizando HTML y CSS
st.write("""
    <div style="display: flex; justify-content: center; position: relative; top: 20px;">
        <h1 style="text-align: center;"> 
            <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" fill="currentColor" class="bi bi-whatsapp" viewBox="0 0 16 16" style="margin-right: 10px;">
                <path d="M13.601 2.326A7.85 7.85 0 0 0 7.994 0C3.627 0 .068 3.558.064 7.926c0 1.399.366 2.76 1.057 3.965L0 16l4.204-1.102a7.9 7.9 0 0 0 3.79.965h.004c4.368 0 7.926-3.558 7.93-7.93A7.9 7.9 0 0 0 13.6 2.326zM7.994 14.521a6.6 6.6 0 0 1-3.356-.92l-.24-.144-2.494.654.666-2.433-.156-.251a6.56 6.56 0 0 1-1.007-3.505c0-3.626 2.957-6.584 6.591-6.584a6.56 6.56 0 0 1 4.66 1.931 6.56 6.56 0 0 1 1.928 4.66c-.004 3.639-2.961 6.592-6.592 6.592m3.615-4.934c-.197-.099-1.17-.578-1.353-.646-.182-.065-.315-.099-.445.099-.133.197-.513.646-.627.775-.114.133-.232.148-.43.05-.197-.1-.836-.308-1.592-.985-.59-.525-.985-1.175-1.103-1.372-.114-.198-.011-.304.088-.403.087-.088.197-.232.296-.346.1-.114.133-.198.198-.33.065-.134.034-.248-.015-.347-.05-.099-.445-1.076-.612-1.47-.16-.389-.323-.335-.445-.34-.114-.007-.247-.007-.38-.007a.73.73 0 0 0-.529.247c-.182.198-.691.677-.691 1.654s.71 1.916.81 2.049c.098.133 1.394 2.132 3.383 2.992.47.205.84.326 1.129.418.475.152.904.129 1.246.08.38-.058 1.171-.48 1.338-.943.164-.464.164-.86.114-.943-.049-.084-.182-.133-.38-.232"/>
            </svg> 
            Whatslit 
        </h1>
    </div>
""", unsafe_allow_html=True)


st.markdown("---")    
st.write("Este bot te permite enviar mensajes personalizados a través de WhatsApp Web.")
exp = st.expander("Instrucciones", expanded=True)
exp.write("1. Sube tu archivo con los datos de los contactos, de preferencia en formato xlsx, csv o txt.")
exp.markdown("> **Nota**: Asegúrate de que la columna que contiene los números de teléfono se llame '**NUMERO**', y que los números estén formateados correctamente, comenzando con el código de país, por ejemplo, para Perú sería (51) seguido del número de teléfono sin espacios ni guiones intermedios, como en el siguiente formato: (51) 987654321.")
exp.write("2. Selecciona un filtro para filtrar los datos según tu necesidad y puedes agregar cuantos filtros desees.")
exp.write("3. Revisa en la tabla que contenga las personas deseadas.")
exp.write("4. Ingresa tu mensaje personalizado, donde las variables se pueden llamar entre llaves, por ejemplo: Hola {nombre}, tu supervisor es {supervisor}.")
exp.write("5. Presiona CTRL + ENTER, para previsualizar el mensaje.")
exp.write("6. Si todo está correcto, presiona el botón 'Enviar mensaje' e iniciar el programa.")
exp.write("7. El programa utiliza el modulo OS para poder realizar la automatización por lo tanto no cierres la ventana de WhatsApp Web y no manipules la computadora hasta que se termine de enviar todo los mensajes.")

# Componentes para cargar archivos
file = st.file_uploader("Sube tu primer archivo", type=["csv","txt","xlsx","xlmx", "json"])

# Lista de filtros
df = leer_archivo(file)  # Cambia el método de lectura según el tipo de archivo
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
mensaje = st.text_area("Ingresa tu mensaje, para personalizarlo, escribe los nombres de las columnas entre llaves, por ejemplo: Hola {contacto}, tu supervisor es {supervisor}.")

# Verificar si se ha ingresado un mensaje
if mensaje is not None:
        # Formatear el mensaje con los valores del DataFrame
        mensaje_formateado = formatear_mensaje(mensaje, df)
        
        # Mostrar el mensaje formateado
        st.write(mensaje_formateado)


#Ingresa el chorme path
# Campo de entrada de texto para la ruta del ejecutable del navegador
chrome_path_name = st.text_input("Ingrese la ruta del ejecutable de Chrome")

# Verificar si se ha ingresado una ruta válida
if chrome_path_name:
    # Utilizar la ruta ingresada para definir la variable chrome_path
    chrome_path_name = r"{}".format(chrome_path_name + " %s")

    # Mostrar la ruta ingresada
    st.write("La ruta del ejecutable del navegador es:", chrome_path_name)
        
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
            chrome_path = chrome_path_name
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