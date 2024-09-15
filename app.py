import time
from PIL import Image
import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.schema import HumanMessage, SystemMessage, AIMessage

# [STREAMLIT] PAGE CONFIGURATION
icon = Image.open("icon.png")
st.set_page_config(page_title="Emigo", page_icon=icon)
st.logo("logo.svg")

# [LANGCHAIN] GOOGLE API KEY CONFIGURATION
GOOGLE_API_KEY = st.secrets["GOOGLE_API_KEY"]

# [STREAMLIT] HIDE MENU
hide_menu = """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    div[data-testid="stDecoration"] {
    visibility: hidden;
    height: 0%;
    position: fixed;
    }
    div[data-testid="stStatusWidget"] {
    visibility: hidden;
    height: 0%;
    position: fixed;
    }
    </style>
    """
st.markdown(hide_menu, unsafe_allow_html = True)

# [STREAMLIT] ADJUST ICON SIZE
icon = """
    <style>
    [data-testid="stChatMessageAvatarAssistant"] {
        width: 2.5rem;
        height: 2.5rem;
        background-color: #24A9E1;
    }
    [data-testid="stChatMessageAvatarUser"] {
        width: 2.5rem;
        height: 2.5rem;
        background-color: #E1C324;
    }
    [class="eyeqlp53 st-emotion-cache-1pbsqtx ex0cdmw0"] {
        width: 2rem;
        height: auto;
    }
    </style>
        """
st.markdown(icon, unsafe_allow_html=True)

# [STREAMLIT] ADJUST LOGO SIZE
logo = """
    <style>
    [data-testid="stLogo"] {
        width: 10rem;
        height: auto;
    }
    </style>
        """
st.markdown(logo, unsafe_allow_html=True)

# [STREAMLIT] REMOVE TOP PADDING
top = """
    <style>
    .block-container {
        padding-top: 1rem;
        padding-bottom: 0rem;
        margin-top: 0rem;
    }
    </style>
        """
st.markdown(top, unsafe_allow_html=True)

# [STREAMLIT] ADJUST HEADER HEIGHT
header = """
    <style>
    [data-testid="stHeader"] {
        height: 6rem;
    }
    </style>
        """
st.markdown(header, unsafe_allow_html=True)

# [STREAMLIT] ADJUST CHAT INPUT PADDING
bottom = """
    <style>
    [data-testid="stBottom"] {
        padding-bottom: 2rem;
        background: white;
    }
    </style>
        """
st.markdown(bottom, unsafe_allow_html=True)

# [STREAMLIT] CHAT INPUT BORDER
chat_border = """
    <style>
    [data-testid="stChatInput"] {
        border: 2px solid #a2a8b8;
    }
    </style>
        """
st.markdown(chat_border, unsafe_allow_html=True)

# [STREAMLIT] TEXT AREA BORDER
text_border = """
    <style>
    [data-baseweb="textarea"] {
        border: 1px;
    }
    </style>
        """
st.markdown(text_border, unsafe_allow_html=True)

# [STREAMLIT] STREAM BOT RESPONSE
def stream(content):
    for word in content.split(" "):
        yield word + " "
        time.sleep(0.03)

# [STREAMLIT] CHAT BOT GREETINGS
with st.chat_message("assistant"):
    st.markdown("What's up? 👋 I am **Emigo**, your **AI study buddy**. You can ask me anything! 😃")

# [STREAMLIT] CREATE A SESSION STATE VARIABLE TO STORE THE CHAT MESSAGES FOR THE MODEL
if "messages" not in st.session_state:
    st.session_state.messages = [SystemMessage(content="""
                                                       You are Emigo, an AI study buddy. Your name comes from the Spanish word 'Amigo'.
                                                       You help users understand complicated topics by answering and explaining in a simple
                                                       and concise way.
                                                       """)]

# [STREAMLIT] CREATE A SESSION STATE VARIABLE TO STORE THE CHAT HISTORY
if "history" not in st.session_state:
    st.session_state.history = []

# [STREAMLIT] DISPLAY THE EXISTING CHAT HISTORY
for message in st.session_state.history:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# [STREAMLIT] MAIN UI
user_input = st.chat_input("Say something.")

# [STREAMLIT] IF SEND BUTTON IS CLICKED
if user_input:

    # [STREAMLIT] STORE USER MESSAGE IN SESSION STATE
    st.session_state.messages.append(HumanMessage(content=user_input))
    st.session_state.history.append({"role": "user", "content": user_input})

    # [STREAMLIT] SHOW USER MESSAGE
    with st.chat_message("user"):
        st.markdown(user_input)
    
    # [LANGCHAIN] GENERATE A RESPONSE USING THE GEMINI CHAT MODEL
    chat = ChatGoogleGenerativeAI(model="gemini-1.5-flash", google_api_key=GOOGLE_API_KEY)
    response = chat.invoke(st.session_state.messages)

    # [STREAMLIT] STORE AI MESSAGE IN SESSION STATE
    st.session_state.messages.append(AIMessage(content=response.content))
    st.session_state.history.append({"role": "assistant", "content": response.content})

    # [STREAMLIT] SHOW RESPONSE
    with st.chat_message("assistant"):
        response = st.write(stream(response.content))
