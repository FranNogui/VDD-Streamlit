import streamlit as st

st.set_page_config(
  page_title="Home",
  page_icon="🏠",
  layout="wide"
)

st.header("Página de Introducción")

st.write("Para el trabajo final de la asignatura de Visualización de Datos se pide realizar, " \
"mediante la herramienta de Streamlit, una web en la que se expongan un conjunto de datos interactuables con widgets. " \
"Así, se ha decidido mantener los datos trabajados en las tareas previas, de tal forma que finalmente se cuenta con" \
"las siguientes páginas:")
st.markdown(
"""
- Titulados en Extremadura
- Centros Universitarios en España
- Tipos de titulaciones impartidas en España
- PAU en España
- Profesorado por género en España
"""
)