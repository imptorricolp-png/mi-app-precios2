import streamlit as st
import pandas as pd
import os
from langchain_experimental.agents import create_pandas_dataframe_agent
from langchain_openai import ChatOpenAI

# 1. Configuración (Esto ya lo tienes)
st.title("Consultor de Precios con IA 🤖")

# 2. Cargar el Excel
df = pd.read_excel("precios.xlsx")

# 3. Configurar la API KEY (Aquí estaba el error)
# Usamos st.secrets para leer la clave que pegaste en Streamlit Cloud
if "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" in st.secrets:
    api_key = st.secrets["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]
else:
    api_key = "TU_API_KEY_LOCAL_AQUI" # Solo para cuando pruebes en tu PC

# 4. Configurar el modelo con la variable correcta
llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0, openai_api_key=api_key)

# 5. Crear el Agente
agente = create_pandas_dataframe_agent(llm, df, verbose=True, allow_dangerous_code=True)

# 6. Interfaz
pregunta = st.text_input("¿Qué precio deseas consultar?")
if pregunta:
    respuesta = agente.run(f"Eres un asistente de ventas profesional. Pregunta: {pregunta}")
    st.write(respuesta)

