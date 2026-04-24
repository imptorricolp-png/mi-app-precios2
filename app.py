import streamlit as st
import pandas as pd
import os  # <--- ASEGÚRATE DE QUE ESTA LÍNEA ESTÉ AQUÍ
from langchain_experimental.agents import create_pandas_dataframe_agent
from langchain_openai import ChatOpenAI

# 1. Configuración de la página
st.set_page_config(page_title="Asistente de Precios IA")
st.title("Consultor de Precios con IA 🤖")

# 2. Cargar el Excel
df = pd.read_excel("precios.xlsx")

# 3. Configurar la IA (Necesitas una API Key de OpenAI)
# Nota: OpenAI da créditos gratis al inicio, pero requiere registro.
if "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" in st.secrets:
    os.environ["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"] = st.secrets["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"]
else:
    os.environ["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"] = "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"
llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0, openai_api_key=os_api_key)

# 4. Crear el Agente que lee el Excel
agente = create_pandas_dataframe_agent(llm, df, verbose=True, allow_dangerous_code=True)

# 5. Interfaz de usuario
pregunta = st.text_input("¿Qué precio deseas consultar?")

if pregunta:
    respuesta = agente.run(f"Eres un asistente de ventas. Si no especifican tipo de precio, da el minorista. Pregunta: {pregunta}")
    st.write(respuesta)
