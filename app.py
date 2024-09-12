import streamlit as st
import time
import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate

os.environ["GOOGLE_API_KEY"] = "AIzaSyCkoQCn0rlZuRaUZioYsuEAy9JFWrfInc0"

# Stream bot response
def stream_data(content):
    for word in content.split(" "):
        yield word + " "
        time.sleep(0.08)

# remove top padding
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

# Sticky Header
header = st.container()
header.markdown("<p style='text-align: center; font-size: 3.4rem; font-weight: 800; line-height: 0.8;'>emigo</p>", unsafe_allow_html=True)
header.markdown("<p style='text-align: center; font-size: 1rem; font-weight: 500; line-height: 1.2;'>Your AI Study Buddy!</p>", unsafe_allow_html=True)
header.write("""<div class='fixed-header'/>""", unsafe_allow_html=True)

# Custom CSS for the sticky header
sticky_header = """
    <style>
        div[data-testid="stVerticalBlock"] div:has(div.fixed-header) {
            position: sticky;
            margin-top: 1rem;
            margin-bottom: -0.5rem;
            top: 2rem;
            background-color: #0e1118;
            z-index: 999;
        }
        .fixed-header {
            border-bottom: 0px solid black;
        }
    </style>
    """
st.markdown(sticky_header, unsafe_allow_html=True)

# Greetings
with st.chat_message("assistant"):
    st.write("What's up? Ask me anything.")

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
user_input = st.chat_input("Say something.")
if user_input:

    # Store and display the current prompt.
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)
    
    # Generate a response using the Gemini LLM.
    template = """
    You are my study buddy who has general knowledge about anything.
    Answer this question: {question} 
    Explain like im ten in a simple and concise way,
    not more than 3 sentences.
    """
    prompt = PromptTemplate.from_template(template)

    llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", stream=True)
    chain = prompt | llm
    result = chain.invoke({"question": user_input})
    content = result.content

    # Stream the response to the chat using `st.write_stream`, then store it in 
    # session state.
    st.session_state.messages.append({"role": "assistant", "content": content})
    with st.chat_message("assistant"):
        response = st.write(stream_data(content))
