import streamlit as st
import os

os.environ["GOOGLE_API_KEY"] = "AIzaSyCj6LMLXmGUXBr2k2OObddZWkVyPxE2cp8"

from langchain_google_genai import ChatGoogleGenerativeAI

llm = ChatGoogleGenerativeAI(model="gemini-pro")
our_query = "What is the currency of India?"
result = llm.invoke(our_query)

prompt = st.chat_input("Say something")
if prompt:
    st.write(f"User has sent the following prompt: {prompt}")
    message = st.chat_message("assistant")
    message.write("Hello human")