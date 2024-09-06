import streamlit as st
import time
import os
from langchain_google_genai import ChatGoogleGenerativeAI

os.environ["GOOGLE_API_KEY"] = "AIzaSyCkoQCn0rlZuRaUZioYsuEAy9JFWrfInc0"

# Stream bot response
def stream_data(content):
    for word in content.split(" "):
        yield word + " "
        time.sleep(0.08)

top = """
        <style>
        .block-container {
                padding-top: 0rem;
                padding-bottom: 0rem;
                margin-top: 0rem;
        }
        </style>
        """
st.markdown(top, unsafe_allow_html=True)

def sticky_container(height=150):
    STICKY_CONTAINER_HTML = """
    <style>
    div[data-testid="stVerticalBlock"] div:has(div.fixed-header)
        position: sticky;
        top: 1.8rem;
        background-color: white;
        z-index: 999;
    </style>
    <div class='fixed-header'/>
    """
    container = st.container(height=height, border=False)
    container.markdown(STICKY_CONTAINER_HTML, unsafe_allow_html=True)
    return container

with sticky_container():
    # TITLE
    st.markdown("<p style='text-align: center; font-size: 3.4rem; font-weight: 800; line-height: 0.8;'>emigo</p>", unsafe_allow_html=True)
    # SUBTITLE
    st.markdown("<p style='text-align: center; font-size: 1rem; font-weight: 500; line-height: 1.2;'>Your AI Study Buddy!</p>", unsafe_allow_html=True)

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
    llm = ChatGoogleGenerativeAI(model="gemini-pro", stream=True)
    result = llm.invoke(prompt)
    content = result.content

    # Stream the response to the chat using `st.write_stream`, then store it in 
    # session state.
    st.session_state.messages.append({"role": "assistant", "content": content})
    with st.chat_message("assistant"):
        response = st.write(stream_data(content))