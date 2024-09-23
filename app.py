import time
import json
import streamlit as st
from PIL import Image
from streamlit_float import *
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.schema import HumanMessage, SystemMessage, AIMessage

# [STREAMLIT] PAGE CONFIGURATION
icon = Image.open("icon.png")
st.set_page_config(page_title="Emigo", page_icon=icon)
st.logo("logo.svg")

# [LANGCHAIN] GOOGLE API KEY CONFIGURATION
GOOGLE_API_KEY = st.secrets["GOOGLE_API_KEY"]

# [STREAMLIT] CUSTOMIZE FILE UPLOAD COMPONENT
upload_btn = """
    <style>
    [data-testid='stFileUploader'] {
        display: flex;
        align-items: center;
        width: inherit;
    }
    [data-testid='stFileUploader'] section {
        padding: 0;
        width: inherit;
    }
    [data-testid='stFileUploader'] section > input + div {
        display: none;
    }
    [data-testid='stFileUploader'] section > input + div + button {
        border: 2px solid #a2a8b8;
        height: 2.8rem;
        width: inherit;
    }
    [data-testid='stFileUploader'] section > input + div + button:before {
        width: calc(100% - 18px);
        content: "IMPORT";
        position: absolute;
        background-color: white;
    }
    [class='st-emotion-cache-fis6aj e1b2p2ww10'] {
        display: none;
    }
    </style>
    """
st.markdown(upload_btn, unsafe_allow_html=True)

# [STREAMLIT] HIDE MENU
hide_menu = """
    <style>
    #MainMenu {
        visibility: hidden;
    }
    footer {
        visibility: hidden;
    }
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
    [data-testid="stToolbar"] {
        display: none;
    }
    </style>
    """
st.markdown(hide_menu, unsafe_allow_html=True)

# [STREAMLIT] ADJUST ICON SIZE
icon = """
    <style>
    [data-testid="stChatMessageAvatarCustom"] {
        width: 2.5rem;
        height: 2.5rem;
        background-color: transparent;
    }
    [data-testid="stIconMaterial"] {
        font-size: 2.5rem;
        color: #24A9E1;
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

# [STREAMLIT] ADJUST BUTTON BORDER
btn_border = """
    <style>
    [data-testid="stBaseButton-secondary"] {
        border: 2px solid #a2a8b8;
        height: 2.8rem;
    }
    </style>
        """
st.markdown(btn_border, unsafe_allow_html=True)

# [STREAMLIT] ADJUST TOP PADDING
top = """
    <style>
    .block-container {
        padding-top: 0rem;
        padding-bottom: 0rem;
        margin-top: -5rem;
    }
    </style>
        """
st.markdown(top, unsafe_allow_html=True)

# [STREAMLIT] ADJUST HEADER
header = """
    <style>
    [data-testid="stHeader"] {
        height: 6rem;
        width: auto;
        z-index: 1;
    }
    </style>
        """
st.markdown(header, unsafe_allow_html=True)

# [STREAMLIT] ADJUST USER CHAT ALIGNMENT
reverse = """
    <style>
    [class="stChatMessage st-emotion-cache-1c7y2kd eeusbqq4"] {
        flex-direction: row-reverse;
        text-align: right;
        font-style: italic;
    }
    </style>
        """
st.markdown(reverse, unsafe_allow_html=True)

# [STREAMLIT] HIDE USER ICON
hide_icon = """
    <style>
    [data-testid="stChatMessageAvatarUser"] {
        display: none;
    }
    </style>
        """
st.markdown(hide_icon, unsafe_allow_html=True)

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

# [STREAMLIT] CHAT BOT GREETINGS
with st.chat_message("assistant", avatar=":material/robot_2:"):
    st.markdown("What's up? 👋 I am **Emigo**, your **AI study buddy**. You can ask me anything! 😃")

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
    with st.chat_message("assistant", avatar=":material/robot_2:"):
        response = st.write(stream(response.content))

# [STREAMLIT] CHAT HISTORY OPTIONS
float_init()

@st.dialog("History Options")
def open_options():
    st.write("**Clear Chat History**")
    
    if st.button("**CLEAR**", type="primary", use_container_width=True):

        # [STREAMLIT] CLEAR SESSION STATES
        st.session_state.history = []
        st.session_state.messages = [SystemMessage(content="""
                                                           You are Emigo, an AI study buddy. Your name comes from the Spanish word 'Amigo'.
                                                           You help users understand complicated topics by answering and explaining in a simple
                                                           and concise way.
                                                           """)]
        st.rerun()
        
    st.write("**Import / Export Chat History**")
    col1, col2 = st.columns(2)
    
    with col1:
        uploaded_file = st.file_uploader("", type='json', label_visibility="collapsed")
        
        if uploaded_file is not None:
            
            # [STREAMLIT] CLEAR SESSION STATES
            st.session_state.history = []
            st.session_state.messages = [SystemMessage(content="""
                                                               You are Emigo, an AI study buddy. Your name comes from the Spanish word 'Amigo'.
                                                               You help users understand complicated topics by answering and explaining in a simple
                                                               and concise way.
                                                               """)]
        
            stringio = uploaded_file.getvalue().decode("utf-8")
            stringjson = json.loads(stringio)

            # [STREAMLIT] REPLACE SESSION STATE WITH IMPORTED CHAT HISTORY
            for string in stringjson:
                st.session_state.history.append({"role": string["role"], "content": string["content"]})
                if string["role"] == "user":
                    st.session_state.messages.append(HumanMessage(content=string["content"]))
                else:
                    st.session_state.messages.append(AIMessage(content=string["content"]))

            st.rerun()
                
    with col2:
        if len(st.session_state.history) == 0:
            st.button("EXPORT", use_container_width=True, disabled=True)
        else:
            export = st.download_button("EXPORT", data=json.dumps(st.session_state.history), file_name="chat-history.json", use_container_width=True)

            # [STREAMLIT] DOWNLOAD CHAT HISTORY AS JSON
            if export:
                st.rerun()
                
button_container = st.container()
with button_container:
    if st.button("⚙️", type="secondary"):
        open_options()
    
button_css = float_css_helper(width="1.8rem", height="2rem", right="3rem", top="2rem", transition=0)
button_container.float(button_css)
