import streamlit as st
import os
import urllib.parse
from datetime import datetime
import google.generativeai as genai
from dotenv import load_dotenv
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import base64

# Load environment variables
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    st.error("❌ GEMINI_API_KEY not found in .env file.")
    st.stop()

# Configure Gemini
genai.configure(api_key=api_key)

# Available Models
MODELS = {
    'Gemini 1.5 Pro': 'models/gemini-1.5-pro-latest',
    'Gemini 1.5 Flash': 'models/gemini-1.5-flash-latest',
    'Gemini 2.5 Pro': 'models/gemini-2.5-pro',
    'Gemini 2.5 Flash': 'models/gemini-2.5-flash',
    'Gemma 3 1B IT': 'models/gemma-3-1b-it',
    'Gemma 3 4B IT': 'models/gemma-3-4b-it',
}

# UI: Page Setup
st.set_page_config(
    page_title="AI Agent - Ghulam Sarwar Khan",
    page_icon="🤖",
    layout="wide",
)

# Function to encode image
def get_image_as_base64(path):
    if not os.path.exists(path):
        return None
    with open(path, "rb") as img:
        return base64.b64encode(img.read()).decode()

# Custom CSS
st.markdown("""
<style>
body, .stApp {
    background: #f0f2f5 !important;
}
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
.sidebar-profile img {
    width: 80px;
    height: 80px;
    border-radius: 50%;
    border: 4px solid #1877f2;
}
</style>
""", unsafe_allow_html=True)

# SIDEBAR
with st.sidebar:
    st.markdown('<div class="sidebar-profile">', unsafe_allow_html=True)
    pic_b64 = get_image_as_base64("GSK Profile Pic.jpeg")
    if pic_b64:
        st.markdown(f'<img src="data:image/jpeg;base64,{pic_b64}">', unsafe_allow_html=True)
    st.markdown('<div class="name"><b>Ghulam Sarwar Khan</b></div>', unsafe_allow_html=True)
    st.markdown('<div class="role">AI Agent Creator</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("---")

    st.image("https://www.gifs-paradise.com/animations/animated-gifs-robots-0026.gif", use_container_width=True)

    st.header("🤖 AI Agent Controls")
    selected_model = st.selectbox("Choose AI Model", list(MODELS.keys()))
    if st.button("🧹 Clear Chat"):
        st.session_state.messages = []
        st.rerun()

    st.markdown("---")

    st.subheader("💬 Stay Connected")
    number = st.text_input("Your WhatsApp Number:")
    if st.button("Submit Number"):
        if number:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            os.makedirs("logs", exist_ok=True)
            with open("logs/visitors.txt", "a") as f:
                f.write(f"{timestamp}, {number}\n")
            try:
                scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
                if 'gcp_service_account' in st.secrets:
                    creds = ServiceAccountCredentials.from_json_keyfile_dict(st.secrets["gcp_service_account"], scope)
                else:
                    creds = ServiceAccountCredentials.from_json_keyfile_name("service_account.json", scope)
                client = gspread.authorize(creds)
                sheet = client.open("Visitor Log - AI Agent").sheet1
                sheet.append_row([timestamp, number])
                st.success("✅ Synced to Google Sheets!")
            except FileNotFoundError:
                st.warning("⚠️ service_account.json missing.")
            except Exception as e:
                st.warning(f"⚠️ Could not sync: {e}")
        else:
            st.warning("Please enter a valid number.")

    st.markdown("---")

    st.markdown("📞 [WhatsApp Creator](https://wa.me/923232777272?text=Hi%2C%20I%20visited%20your%20AI%20agent.)")

# MAIN CONTENT
st.markdown('<div class="main-content">', unsafe_allow_html=True)
st.markdown('<h1 class="main-header">I am your Artificial Intelligence Agent</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">I am here on behalf of Mr. Ghulam Sarwar Khan. Ask anything.</p>', unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    avatar = "GSK Profile Pic.jpeg" if msg["role"] == "bot" else "👤"
    with st.chat_message(msg["role"], avatar=avatar):
        st.markdown(msg["content"])

# User input
if prompt := st.chat_input("How can I assist you today?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar="👤"):
        st.markdown(prompt)

    with st.chat_message("bot", avatar="GSK Profile Pic.jpeg"):
        with st.spinner("Thinking..."):
            try:
                model = genai.GenerativeModel(MODELS[selected_model])
                response = model.generate_content(prompt)
                st.markdown(response.text)
                st.session_state.messages.append({"role": "bot", "content": response.text})
            except Exception as e:
                st.error(f"❌ Error: {e}")
                st.session_state.messages.append({"role": "bot", "content": f"Error: {e}"})

st.markdown("</div>", unsafe_allow_html=True)
