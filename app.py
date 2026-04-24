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
    api_key = st.secrets["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"]
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

