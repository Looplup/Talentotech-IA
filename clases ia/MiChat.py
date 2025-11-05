#IMPORTAMOS Streamlit
#pip install streamlit | python -m install streamlit
#para correr = python -m streamlit run MiChat.py
import streamlit as st
from groq import Groq

st.set_page_config(page_title="BMO IA", page_icon="🤖")
st.title("Soy la inteligencia artificial BMO")

nombre = st.text_input("Como te llamo??")
if st.button("saludar a BMO!"):
    st.write(f"Hola {nombre}! Bienvenidx a talento tech")

#MODELOS = ["modelo 1", "modelo 2", "modelo 3"]
MODELOS = ['llama-3.1-8b-instant', 'llama-3.3-70b-versatile', 'deepseek-r1-distill-llama-70b']

def configurar_pagina():
    st.title("Pregunta lo que quieras a la IA -Lucila Guarino")
    st.sidebar.title("configuracion de la IA")

    elegirModelo = st.sidebar.selectbox(
        "Elegi un modelo",
        options = MODELOS,
        index =0
    )

    return elegirModelo



def crear_usuario_groq():
    clave_secreta = st.secrets["CLAVE_API"]
    return Groq(api_key= clave_secreta)

def configurar_modelo(cliente, modelo, mensajeDeEntrada):
    return cliente.chat.completions.create(
        model = modelo,
        messages = [{"role":"user", "content": mensajeDeEntrada}],
        stream = True  #si es true está comprimido y false es descomprimido
    )

def inicializar_estado():
    if "mensajes" not in st.session_state:
        st.session_state.mensajes = []


#Funciones agregadas en CLASE 8
def actualizar_historial(rol, contenido, avatar):
    st.session_state.mensajes.append({"role": rol, "content": contenido, "avatar": avatar})

def mostrar_historial():
    for mensaje in st.session_state.mensajes:
        with st.chat_message(mensaje["role"], avatar= mensaje["avatar"]) : st.markdown(mensaje["content"])

def area_chat():
    contenedorDelChat = st.container(height=400, border= True)
    with contenedorDelChat: mostrar_historial()


# Clase 9 - funciones
def generar_respuestas(chat_completo):
    respuesta_completa = ""
    for frase in chat_completo:
        print(frase.choices[0].delta.content)
        if frase.choices[0].delta.content:
            respuesta_completa += frase.choices[0].delta.content
            yield frase.choices[0].delta.content
    return respuesta_completa


# Main - > Todas las funciones para correr el Chatbot
def main ():
    clienteUsuario = crear_usuario_groq()
    inicializar_estado()
    modelo = configurar_pagina()
    area_chat() #Nuevo 
    mensaje = st.chat_input("Escribi tu mensaje:")

    if mensaje:
        actualizar_historial("user", mensaje, "😁")
        chat_completo = configurar_modelo(clienteUsuario, modelo, mensaje)
        if chat_completo:
                with st.chat_message("assistant"):
                    respuesta_completa = st.write_stream(generar_respuestas(chat_completo))
                    actualizar_historial("assistant", respuesta_completa, "🤖")
                    st.rerun()
        
if __name__ == "__main__":
    main()

    





#-----Dentro del condicional-------------------------------------
#if mensaje:
#    actualizar_historial("user", mensaje, "😁")
#    chat_completo = configurar_modelo(clienteUsuario, modelo, mensaje)
#    actualizar_historial("assistant", respuesta_completa, "🤖")
#    st.rerun()

    
