import streamlit as st
import os
import urllib.parse
from datetime import datetime
import google.generativeai as genai
from dotenv import load_dotenv
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import base64

# --- Page Configuration ---
st.set_page_config(
    page_title="AI Agent - Ghulam Sarwar Khan",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Utility function to encode images ---
def get_image_as_base64(path):
    if not os.path.exists(path):
        return None
    with open(path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode()

# --- Custom CSS for a Polished, Professional Look ---
st.markdown("""
<style>
    /* Base and Background */
    body, .stApp {
        background: #f0f2f5 !important;
    }

    /* Main Content Area */
    .main-content {
        background-color: white;
        padding: 2rem;
        border-radius: 15px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.08);
    }
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1c1e21;
        text-align: center;
    }
    .sub-header {
        font-size: 1.1rem;
        color: #606770;
        text-align: center;
        margin-bottom: 2rem;
    }

    /* Sidebar Styling */
    .st-emotion-cache-18ni7ap {
        background: #FFFFFF;
        border-right: 1px solid #e0e0e0;
    }
    .sidebar-profile {
        text-align: center;
        padding-top: 1rem;
    }
    .sidebar-profile img {
        width: 100px;
        height: 100px;
        border-radius: 50%;
        border: 4px solid #1877f2;
        margin-bottom: 0.5rem;
    }
    .sidebar-profile .name {
        font-weight: bold;
        color: #1c1e21;
        font-size: 1.2rem;
    }
    .sidebar-profile .role {
        color: #606770;
        font-size: 1rem;
        margin-bottom: 1rem;
    }
    .sidebar-gif img {
        border-radius: 10px;
    }
    
    /* Footer Styling */
    .footer {
        text-align: center;
        color: #606770;
        font-size: 0.9rem;
        margin-top: 3rem;
    }
    .footer a {
        color: #1877f2;
        text-decoration: none;
        margin: 0 0.5rem;
    }
    .footer a:hover {
        text-decoration: underline;
    }
</style>
""", unsafe_allow_html=True)


# --- Load Environment Variables & API Key ---
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")

if not api_key:
    st.error("Error: GOOGLE_API_KEY not found in .env file.")
    st.stop()
try:
    genai.configure(api_key=api_key)
except Exception as e:
    st.error(f"Failed to configure Gemini API: {e}")
    st.stop()

# --- Model Definitions ---
MODELS = {
    'Gemini 1.5 Pro': 'models/gemini-1.5-pro-latest',
    'Gemini 1.5 Flash': 'models/gemini-1.5-flash-latest',
    'Gemma 3 4B IT': 'models/gemma-3-4b-it',
    'Gemma 3 1B IT': 'models/gemma-3-1b-it',
}

# =================================================================================================
#                                         SIDEBAR
# =================================================================================================
with st.sidebar:
    st.markdown('<div class="sidebar-profile">', unsafe_allow_html=True)
    profile_pic_b64 = get_image_as_base64("GSK Profile Pic.jpeg")
    if profile_pic_b64:
        st.markdown(f'<img src="data:image/jpeg;base64,{profile_pic_b64}">', unsafe_allow_html=True)
    st.markdown('<div class="name">Ghulam Sarwar Khan</div>', unsafe_allow_html=True)
    st.markdown('<div class="role">AI Agent Creator</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("---")
    
    st.markdown('<div class="sidebar-gif">', unsafe_allow_html=True)
    st.image("https://www.gifs-paradise.com/animations/animated-gifs-robots-0026.gif", use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    st.header("👨‍💻 AI Agent Controls")
    selected_model_name = st.selectbox("Select AI Model", list(MODELS.keys()))
    if st.button("Clear Chat History"):
        st.session_state.messages = []
        st.rerun()

    st.markdown("---")

    st.subheader("Stay Connected")
    visitor_number = st.text_input("Enter your WhatsApp number...", key="whatsapp_input")
    if st.button("Submit Number"):
        if visitor_number:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            # 1. Local Logging
            os.makedirs("logs", exist_ok=True)
            with open("logs/visitors.txt", "a") as f:
                f.write(f"{timestamp}, {visitor_number}\n")

            # 2. Google Sheets Sync
            try:
                scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
                if 'gcp_service_account' in st.secrets:
                    creds = ServiceAccountCredentials.from_json_keyfile_dict(st.secrets["gcp_service_account"], scope)
                else: 
                    creds = ServiceAccountCredentials.from_json_keyfile_name("service_account.json", scope)

                client = gspread.authorize(creds)
                sheet = client.open("Visitor Log - AI Agent").sheet1
                sheet.append_row([timestamp, visitor_number])
                st.success("✅ Synced to Google Sheets!")
            except FileNotFoundError:
                st.warning("Google Sheets sync not configured (service_account.json not found). Logged locally.")
            except Exception as e:
                st.warning(f"⚠️ Could not sync to Sheets: {e}")
        else:
            st.warning("Please enter a valid number.")
    
    st.markdown("---")

    st.subheader("Contact Creator")
    creator_msg = urllib.parse.quote("Hi, I visited your AI agent and would love to connect.")
    st.markdown(f"👉 [WhatsApp Ghulam Sarwar Khan](https://wa.me/923232777272?text={creator_msg})")


# =================================================================================================
#                                          MAIN CHAT INTERFACE
# =================================================================================================
st.markdown('<div class="main-content">', unsafe_allow_html=True)

st.markdown('<h1 class="main-header">I am your Artificial Intelligence Agent</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">I am here on behalf of Mr. Ghulam Sarwar Khan.<br>You can ask me your questions and I will assist you professionally.</p>', unsafe_allow_html=True)

# --- Initialize Chat History ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- Display existing messages ---
user_avatar_b64 = get_image_as_base64("user_avatar.png") # Optional: provide a path to a generic user icon
for message in st.session_state.messages:
    avatar = profile_pic_b64 if message["role"] == "bot" else user_avatar_b64
    with st.chat_message(message["role"], avatar=avatar):
        st.markdown(message["content"])

# --- Handle new user input ---
if prompt := st.chat_input("How can I help you today?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar=user_avatar_b64):
        st.markdown(prompt)

    with st.chat_message("bot", avatar=profile_pic_b64):
        with st.spinner("🤔 Thinking..."):
            try:
                model = genai.GenerativeModel(MODELS[selected_model_name])
                response = model.generate_content(prompt)
                response_text = response.text
                st.markdown(response_text)
                st.session_state.messages.append({"role": "bot", "content": response_text})
            except Exception as e:
                st.error(f"⚠️ Sorry, an error occurred: {e}")
                st.session_state.messages.append({"role": "bot", "content": f"Error: {e}"})

# --- Footer ---
st.markdown("""
<div class="footer">
    🤖 Powered by Google Gemini AI | 👨‍💻 Created by Ghulam Sarwar Khan<br>
    <a href="https://www.linkedin.com/in/ghulam-sarwar-khan-b989b48a/" target="_blank">LinkedIn</a> |
    <a href="https://www.facebook.com/sarwaronline" target="_blank">Facebook</a> |
    <a href="https://www.youtube.com/channel/UC1cipUgPINuc-XFgtJCb30g" target="_blank">YouTube</a> |
    <a href="https://github.com/gsarwarkhan" target="_blank">GitHub</a>
</div>
""", unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True) 