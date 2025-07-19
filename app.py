import streamlit as st
import bloque1 # type: ignore
import bloque2 # type: ignore
import bloque3
import bloque4

# Configuración general (solo UNA vez en toda la app)
st.set_page_config(page_title="App Estadística Inferencial", layout="wide")

st.title("📊 App de Estadística Inferencial - Modular")

if "pagina" not in st.session_state:
    st.session_state.pagina = "Bloque 1"

menu = ["Bloque 1", "Bloque 2", "Bloque 3", "Bloque 4"]

st.sidebar.title("Navegación")
seleccion = st.sidebar.radio("Seleccione un bloque", menu)
st.session_state.pagina = seleccion

if seleccion == "Bloque 1":
    bloque1.run()
elif seleccion == "Bloque 2":
    bloque2.run()
elif seleccion == "Bloque 3":
    bloque3.run()
elif seleccion == "Bloque 4":
    bloque4.run()
