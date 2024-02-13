import streamlit as st
import pandas as pd
########################################33
### Nueva sección
def new_section(Titulo, texto):
    st.markdown("---")
    st.markdown(Titulo)
    st.markdown(texto)


#####################################################
# Eliminando el hambuguer and footer
st.markdown("""
<style>
.st-emotion-cache-6q9sum.ef3psqc4 /* Esto es la class del incono del hambuguer */
{
            visibility: hidden;
}            
</style>



""", unsafe_allow_html=True)



###################################################
st.title("Hello world, my first tittle with streamlit")
st.header("Este es un Header")
st.subheader("Este es un subheader")
st.text("Esto es un texto que va debajo de un subheader")
st.write("This is a simple text")
st.markdown("# Titulo con markdown")
st.markdown("#### Este es un texto con Markdown")
st.markdown("Esto es un `codigo` con markdown ```Print('Hello world')```")
st.markdown("---")
st.caption("Esto es una leyenda")
st.latex(r"\text{Esto es una matriz 2x2 con Latex}")
st.latex(r"\begin{pmatrix}a&b\\c&d\end{pmatrix}")
json = {"a": "1,2,3", "b": "4,5,6", "c": "7,8,9"}
st.json(json)

code= """
print ("Hello world")

def funct():
    return "Hello world"
"""
st.text("Esto es un codigo en python con el atributo code de streamlit")
st.code(code, language="python")
st.markdown("---")
st.write("Esto es una metrica con streamlit")
st.metric(label="Temperatura", value="28°", delta="Sensación termica de 33°")

st.markdown("---")

tabel = pd.DataFrame({"Column 1": [1,2,3,4,6,7], "Apellido": ["Alata","Aramburu","Angulo","Anaristo","Alata","Antogasto"]})
st.table(tabel)

filtro_tabel = tabel["Apellido"].unique()

imagen = "wallpaper.png"

st.image(imagen, caption="Esto es una imagen")

audio = r"C:\Users\Aoijunior\Desktop\Streamlit\Grabación.m4a"

st.audio(audio)

video =r"C:\Users\Aoijunior\Desktop\Diplomado de Econometría Aplicada\Modulo 3\Sesión 01  Macroeconometría (Docente PABLO LORENZO VILLACAMPA)  11-11.mp4"
st.video(video)

st.markdown("---")
st.markdown("# Wigets basicos con streamlit")
st.markdown("**Estos son Cheackbox con streamlit**")
def change():
    print(st.session_state.checker)

state = st.checkbox("Esto es un checkbox", value=True, on_change=change, key="checker")

if state == True:
    st.write("El checkbox esta activado")
else:
    pass

st.markdown("---")
st.markdown("**Estos son Radio buttons con streamlit**")
rdbuttons = st.radio("Escoge tu opción preferida", ("Perú", "Argentina", "Tu mamá calata"))

if rdbuttons == "Perú":
    st.write("Viva el Perú Carajo")
elif rdbuttons == "Argentina":
    st.write("Pochita y Milei presidente")
elif rdbuttons == "Tu mamá calata":
    st.write("Tu cuchillo no corta")

else:
    pass

new_section("####  Esto es un boton con streamlit", "Esto es un boton con la función on_click")

def bt_click():
    print("Button clicked")
btn = st.button("Esto es un boton", on_click=bt_click)

new_section("####  Esto es un selectbox con streamlit", "Esto es un selectbox con la función on_change")

def selectbox():
    print(st.session_state.selectbox)
select = st.selectbox("Escoge tu opción preferida", filtro_tabel, key="selectbox", on_change=selectbox)

new_section("####  Esto es un multiselect con streamlit", "Esto es un multiselect con la función on_change")

def multiselect():
    print(st.session_state.multiselect)
multiselect = st.multiselect("Escoge tu opción preferida", filtro_tabel, key="multiselect", on_change=multiselect)
st.write(multiselect)