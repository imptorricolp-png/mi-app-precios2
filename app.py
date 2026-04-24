import streamlit as st
import pandas as pd
import os
from langchain_experimental.agents import create_pandas_dataframe_agent
from langchain_openai import ChatOpenAI

# 1. Configuración de la App
st.set_page_config(page_title="Consultor de Precios", layout="wide")
st.title("Consultor de Precios con IA 🤖")

# 2. Gestión de la API KEY (FORZADO PARA CLOUD)
# Intentamos obtener la clave de los Secrets de Streamlit
if "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" in st.secrets:
    openai_api_key = st.secrets["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"]
else:
    # Si no encuentra el Secret, intentará buscarla en las variables del sistema (local)
    openai_api_key = os.getenv("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")

# 3. Cargar el Excel
try:
    df = pd.read_excel("precios.xlsx")
except Exception as e:
    st.error(f"No se pudo leer el archivo Excel: {e}")
    st.stop()

# 4. Inicializar el Modelo e Interfaz
if not openai_api_key:
    st.error("⚠️ No se encontró la API KEY. Verifica los Secrets en Streamlit Cloud.")
else:
    try:
        # Definimos el modelo usando la clave obtenida arriba
        llm = ChatOpenAI(
            model="gpt-3.5-turbo", 
            temperature=0, 
            openai_api_key=openai_api_key
        )

        # Crear el agente que interactúa con el Excel
        agente = create_pandas_dataframe_agent(
            llm, 
            df, 
            verbose=True, 
            allow_dangerous_code=True
        )

        pregunta = st.text_input("Escribe tu consulta de precios aquí:")

        if pregunta:
            with st.spinner("Consultando base de datos..."):
                # Instrucción maestra para los 3 precios
                prompt_full = (
                    f"Contexto: Tienes 3 precios: Minorista, Institucional y Mayorista. "
                    f"Si el usuario no especifica, usa el Minorista. "
                    f"Pregunta: {pregunta}"
                )
                respuesta = agente.run(prompt_full)
                st.info(respuesta)

    except Exception as e:
        st.error(f"Error en la consulta: {e}")
