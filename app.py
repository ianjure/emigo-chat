import streamlit as st
import os
from langchain_google_genai import ChatGoogleGenerativeAI

os.environ["GOOGLE_API_KEY"] = "AIzaSyCkoQCn0rlZuRaUZioYsuEAy9JFWrfInc0"

# Create a session state variable to store the chat messages. This ensures that the
# messages persist across reruns.
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display the existing chat messages via `st.chat_message`.
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Create a chat input field to allow the user to enter a message. This will display
# automatically at the bottom of the page.
prompt = st.chat_input("Say something.")
if prompt:

    # Store and display the current prompt.
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Generate a response using the Gemini LLM.
    stream = ChatGoogleGenerativeAI(
            model="gemini-pro",
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            stream=True,
        )
    """
    llm = ChatGoogleGenerativeAI(model="gemini-pro",)
    messages= [
        {"role": m["role"], "content": m["content"]}
        for m in st.session_state.messages
    ]
    stream = llm.invoke(messages)
    """

    with st.chat_message("assistant"):
        response = st.write_stream(stream)
    st.session_state.messages.append({"role": "assistant", "content": response})