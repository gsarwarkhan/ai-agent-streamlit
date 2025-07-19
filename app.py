import os
import streamlit as st
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables from .env
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    st.error("❌ ERROR: API key not found in .env file.")
    st.stop()

genai.configure(api_key=api_key)

MODELS = [
    {
        'name': 'models/gemini-1.5-pro-latest',
        'desc': 'Gemini 1.5 Pro (latest): General-purpose, high-quality, multimodal.'
    },
    {
        'name': 'models/gemini-1.5-flash-latest',
        'desc': 'Gemini 1.5 Flash (latest): Fast, cost-effective, good for chat and summarization.'
    },
    {
        'name': 'models/gemini-2.5-pro',
        'desc': 'Gemini 2.5 Pro: Most advanced, high-quality, multimodal.'
    },
    {
        'name': 'models/gemini-2.5-flash',
        'desc': 'Gemini 2.5 Flash: Fastest, optimized for speed and cost.'
    },
    {
        'name': 'models/gemma-3-1b-it',
        'desc': 'Gemma 3 1B IT: Lightweight, open, instruction-tuned.'
    },
    {
        'name': 'models/gemma-3-4b-it',
        'desc': 'Gemma 3 4B IT: Larger, open, instruction-tuned.'
    },
]

st.set_page_config(page_title="GSK AI Agent", page_icon="🤖", layout="centered")

# --- Professional UI Styling ---
st.markdown("""
    <style>
    .block-container {padding-top: 2rem;}
    .stButton>button {
        background: #0069d9;
        color: white;
        border-radius: 4px;
        font-weight: 600;
        padding: 0.5rem 1.5rem;
        border: none;
        box-shadow: 0 2px 8px rgba(0,0,0,0.04);
    }
    .stTextInput>div>div>input {
        border-radius: 8px;
        border: 1.5px solid #0069d9;
        padding: 0.5rem 1rem;
        font-size: 1.1rem;
    }
    .stMarkdown {
        font-size: 1.08rem;
    }
    </style>
""", unsafe_allow_html=True)

# --- Profile Header ---
profile_pic_path = "GSK Profile Pic.jpeg"

col1, col2 = st.columns([1, 4])
with col1:
    st.image(profile_pic_path, width=110, caption="Ghulam Sarwar Khan", output_format="auto")
with col2:
    st.markdown(
        "<h2 style='margin-bottom:0.2rem; color:#22223b;'>I am your Artificial Intelligence Agent</h2>"
        "<h4 style='margin-top:0; color:#4a4e69;'>I am here on behalf of <b>Mr. Ghulam Sarwar Khan</b></h4>"
        "<p style='font-size:1.1rem; color:#22223b;'>You can ask me your questions and I will assist you professionally.</p>",
        unsafe_allow_html=True
    )

st.markdown("---")

# --- Model selection sidebar ---
if 'messages' not in st.session_state:
    st.session_state['messages'] = []
if 'model_name' not in st.session_state:
    st.session_state['model_name'] = 'models/gemma-3-4b-it'

with st.sidebar:
    st.header("Model Selection")
    model_options = [f"{m['desc']}" for m in MODELS]
    idx = [m['name'] for m in MODELS].index(st.session_state['model_name'])
    selected = st.selectbox("Choose a model:", model_options, index=idx)
    new_model_name = MODELS[model_options.index(selected)]['name']
    if new_model_name != st.session_state['model_name']:
        st.session_state['model_name'] = new_model_name
        st.session_state['messages'] = []
        st.success(f"Switched to: {new_model_name}")
    st.markdown("""
    **Features:**
    - Chat with Gemini or Gemma models
    - Switch models anytime
    - All models are free (subject to Google API quotas)
    - Share this app after deployment!
    """)

model = genai.GenerativeModel(st.session_state['model_name'])

# --- Chat UI ---
for msg in st.session_state['messages']:
    if msg['role'] == 'user':
        st.markdown(f"**You:** {msg['content']}", unsafe_allow_html=True)
    else:
        st.markdown(f"**AI:** {msg['content']}", unsafe_allow_html=True)

prompt = st.text_input("Type your message and press Enter:", key="input")
if st.button("Send", use_container_width=True) or (prompt and st.session_state.get('last_prompt') != prompt):
    if prompt:
        st.session_state['messages'].append({'role': 'user', 'content': prompt})
        try:
            response = model.generate_content(prompt)
            st.session_state['messages'].append({'role': 'ai', 'content': response.text})
        except Exception as e:
            st.session_state['messages'].append({'role': 'ai', 'content': f"❌ Error: {e}"})
        st.session_state['last_prompt'] = prompt
        st.rerun() 