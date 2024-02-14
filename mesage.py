import streamlit as st
import pandas as pd
import re
import json

#DETECTAR EL SEPARADOR DE UN ARCHIVO CSV
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

# Función para formatear el mensaje con los valores del DataFrame
def formatear_mensaje(mensaje, df):
    if df is not None:    
        # Expresión regular para encontrar las variables dentro del mensaje
        patron = r'{([^{}]*)}'
        coincidencias = re.findall(patron, mensaje)

        mensajes_formateados = []  # Lista para almacenar los mensajes formateados para cada fila del DataFrame

        # Iterar sobre cada fila del DataFrame
        for index, fila in df.iterrows():
            mensaje_formateado = mensaje  # Iniciar con el mensaje original
            # Reemplazar cada variable en el mensaje con el valor correspondiente de la fila
            for variable in coincidencias:
                # Obtener el valor de la variable de la fila actual
                valor_variable = fila.get(variable.strip(), '')
                # Reemplazar la variable con su valor en el mensaje formateado
                mensaje_formateado = mensaje_formateado.replace("{" + variable + "}", str(valor_variable))
            # Agregar el mensaje formateado a la lista de mensajes formateados
            mensajes_formateados.append(mensaje_formateado)
    else:
        mensajes_formateados = ["No se ha cargado ningún archivo."] # Si no se ha cargado un archivo, agregar un mensaje de error

    return mensajes_formateados


# DataFrame de ejemplo
file = st.file_uploader("Sube un archivo CSV, TXT, XLSX, XLSM o JSON", type=["csv", "txt", "xlsx", "xlsm", "json"])
df = leer_archivo(file)
st.table(df.head())
# Componente de entrada de texto para el mensaje
mensaje = st.text_area("Ingresa tu mensaje, recuerda que los saltos de linea se hacen con '%0A' ")

# Si se ha ingresado un mensaje
if mensaje is not None:
    # Formatear el mensaje con los valores del DataFrame
    mensaje_formateado = formatear_mensaje(mensaje, df)
    
    # Mostrar el mensaje formateado
    st.write(mensaje_formateado)