import streamlit as st
import pandas as pd

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

# Función principal
def main():
    # Cargar archivo
    file = st.file_uploader("Sube tu archivo", type=["csv", "txt", "xlsx", "xlmx", "json"])
    if file:
        df = pd.read_excel(file)  # Cambia el método de lectura según el tipo de archivo

        # Lista de filtros
        if "filtros" not in st.session_state:
            st.session_state.filtros = []

        # Seleccionar tipo de filtro
        filtro = st.selectbox("Tipo de filtro", ["Básico", "Avanzado"], key="tipo_filtro")

        # Botón para agregar filtro
        if st.button("Agregar filtro"):
            st.session_state.filtros.append(filtro)

        # Mostrar filtros
        for i, filtro in enumerate(st.session_state.filtros):
            st.markdown(f"###### Filtro {i+1}")
            if filtro == "Básico":
                columna, valores = st.columns(2)
                columna = columna.selectbox("Selecciona la columna", df.columns, key=f"columna_basico_{i}")
                valores = valores.multiselect("Selecciona los valores", df[columna].unique(), key=f"valores_basico_{i}")
                df = filtro_basico(df, columna, valores)
            elif filtro == "Avanzado":
                col1, col2, col3 = st.columns(3)
                columna = col1.selectbox("Selecciona la columna", df.columns, key=f"columna_avanzado_{i}")
                logica = col2.selectbox("Selecciona la lógica", ['None','Mayor', 'Mayor o igual', 'Menor', 'Menor o igual', 'Igual', 'Diferente'], key=f"logica_avanzado_{i}")
                valor = col3.number_input("Ingresa el valor", step=0.01, key=f"valor_avanzado_{i}")
                df = filtro_avanzado(df, columna, logica, valor)
            
            # Botón para eliminar filtro
            if st.button(f"Eliminar filtro {i+1}"):
                del st.session_state.filtros[i]

        # Aplicar filtros al presionar un botón
        st.table(df)

# Ejecutar la función principal
if __name__ == "__main__":
    main()