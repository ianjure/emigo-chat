import streamlit as st


prompt = st.chat_input("Say something")
if prompt:
    st.write(f"User has sent the following prompt: {prompt}")
    message = st.chat_message("assistant")
    message.write("Hello human")