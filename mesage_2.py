import streamlit as st
import pandas as pd


############### AQUI INICIA EL CÓDIGO DE LECTURA DE ARCHIVOS ####################

# Rutas de los archivos XLSX
archivo_data_xlsx = r"C:\Users\WIN10\Desktop\FFVV - SUPERVISOR (1).xlsx"
archivo_df_total_xlsx = r"C:\Users\WIN10\Desktop\asignacion de cajas.xlsx"

# Nombre de las hojas que deseas leer
nombre_de_la_hoja_data = 'Hoja1'
nombre_de_la_hoja_df_total = 'main'

# Lee los archivos XLSX en DataFrames de pandas
data = pd.read_excel(archivo_data_xlsx, sheet_name=nombre_de_la_hoja_data)
df_total = pd.read_excel(archivo_df_total_xlsx, sheet_name=nombre_de_la_hoja_df_total)

############### AQUI FINALIZA EL CÓDIGO DE LECTURA DE ARCHIVOS ####################

############### AQUI INICIA EL CÓDIGO DE PROCESAMIENTO DE DATOS ####################

# Filtra los valores en la columna 'DÍAS' mayores a 30 en 'df_total'
df_filtrado = df_total[df_total['DÍAS'] > 30]

# Agrupa por 'EJECUTIVO' y aplica una función personalizada para crear una tabla con la información requerida
def crear_tabla_grupo(group):
    # Crea un DataFrame con la información del grupo
    tabla = group[['MODELO', 'DÍAS', 'CAJA']].reset_index(drop=True)
    return tabla

# Aplica la función personalizada y obtiene un DataFrame con la información de cada grupo
df_tabla = df_filtrado.groupby('EJECUTIVO').apply(crear_tabla_grupo)

# Une el DataFrame resultante con 'data' para obtener un nuevo DataFrame con la información necesaria
df_nuevo = pd.merge(data[['EJECUTIVO', 'SUPERVISOR', 'DNI', 'Correo', 'Numero']], df_tabla, on='EJECUTIVO', how='left')

# Muestra el nuevo DataFrame
with st.expander("Visualizar el Dataframe"):
    st.table(df_nuevo)

# Si deseas mostrar esta tabla en el mensaje formateado
mensaje = st.text_area("Ingresa tu mensaje, recuerda que los saltos de linea se hacen con '%0A' ")

# Si se ha ingresado un mensaje
if mensaje is not None:
    # Formatear el mensaje con los valores del DataFrame
    mensaje_formateado = mensaje.replace("{tabla}", df_nuevo.to_string())
    
    # Mostrar el mensaje formateado
    st.write(mensaje_formateado)
