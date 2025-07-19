import streamlit as st
import os
from dotenv import load_dotenv
import google.generativeai as genai
import time

# Load environment variables
load_dotenv()

# Configure page
st.set_page_config(
    page_title="AI Agent - Ghulama Sarwar Khan",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #666;
        text-align: center;
        margin-bottom: 2rem;
    }
    .chat-message {
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
    }
    .user-message {
        background-color: #e3f2fd;
        border-left: 4px solid #2196f3;
    }
    .ai-message {
        background-color: #f3e5f5;
        border-left: 4px solid #9c27b0;
    }
    .error-message {
        background-color: #ffebee;
        border-left: 4px solid #f44336;
        color: #c62828;
    }
    .token-info {
        background-color: #e8f5e8;
        border-left: 4px solid #4caf50;
        font-size: 0.9rem;
        padding: 0.5rem;
        margin-top: 0.5rem;
        border-radius: 5px;
    }
    .stButton > button {
        width: 100%;
        border-radius: 10px;
        height: 3rem;
        font-size: 1.1rem;
    }
    .clear-button {
        background-color: #ff5722 !important;
        color: white !important;
    }
    .clear-button:hover {
        background-color: #d84315 !important;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'messages' not in st.session_state:
    st.session_state.messages = []
if 'current_model' not in st.session_state:
    st.session_state.current_model = 'models/gemini-1.5-pro-latest'

# Available models
MODELS = {
    'Gemini 1.5 Pro (Latest)': 'models/gemini-1.5-pro-latest',
    'Gemini 1.5 Flash (Latest)': 'models/gemini-1.5-flash-latest',
    'Gemini 2.5 Pro': 'models/gemini-2.5-pro',
    'Gemini 2.5 Flash': 'models/gemini-2.5-flash',
    'Gemma 3 1B IT': 'models/gemma-3-1b-it',
    'Gemma 3 4B IT': 'models/gemma-3-4b-it'
}

# Function to initialize Gemini
def initialize_gemini():
    """Initialize Gemini API with error handling"""
    try:
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            st.error("❌ API key not found. Please check your .env file.")
            return None
        
        genai.configure(api_key=api_key)
        return True
    except Exception as e:
        st.error(f"❌ Error initializing Gemini: {str(e)}")
        return None

# Function to get model response
def get_model_response(model, prompt):
    """Get response from Gemini model with error handling"""
    try:
        genai_model = genai.GenerativeModel(model)
        response = genai_model.generate_content(prompt)
        return response, None
    except Exception as e:
        error_msg = str(e)
        
        # Handle specific quota errors
        if "429" in error_msg and "quota" in error_msg.lower():
            return None, "QUOTA_EXCEEDED"
        elif "quota" in error_msg.lower():
            return None, "QUOTA_EXCEEDED"
        else:
            return None, error_msg

# Function to clear chat
def clear_chat():
    """Clear the chat history"""
    st.session_state.messages = []
    st.rerun()

# Initialize Gemini
if not initialize_gemini():
    st.stop()

# Header with profile picture
col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    try:
        st.image("GSK Profile Pic.jpeg", width=150, caption="Ghulama Sarwar Khan")
    except:
        st.markdown("👤 **Profile Picture**")
    
    st.markdown('<h1 class="main-header">I am your Artificial Intelligence Agent</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">on behalf of <strong>Ghulama Sarwar Khan</strong><br>You can ask me your questions!</p>', unsafe_allow_html=True)

# Sidebar for controls
with st.sidebar:
    st.header("⚙️ Settings")
    
    # Model selection
    st.subheader("🤖 Select Model")
    selected_model_name = st.selectbox(
        "Choose your AI model:",
        list(MODELS.keys()),
        index=0,
        help="Different models have different capabilities and response times"
    )
    
    # Update current model if changed
    if MODELS[selected_model_name] != st.session_state.current_model:
        st.session_state.current_model = MODELS[selected_model_name]
        st.success(f"✅ Switched to {selected_model_name}")
    
    st.markdown("---")
    
    # Clear chat button
    st.subheader("🗑️ Chat Management")
    if st.button("Clear Chat History", key="clear_chat", help="Remove all conversation history"):
        clear_chat()
    
    st.markdown("---")
    
    # Voice input section (placeholder for future implementation)
    st.subheader("🎤 Voice Input")
    st.info("Voice input feature coming soon!")
    
    # Add voice input button (disabled for now)
    voice_input = st.button("🎤 Record Voice", disabled=True, help="Voice input not yet implemented")
    
    st.markdown("---")
    
    # Information
    st.subheader("ℹ️ About")
    st.markdown("""
    **Features:**
    - 🤖 Multiple AI models
    - 💬 Real-time chat
    - 🔄 Model switching
    - 🗑️ Chat clearing
    - 📊 Token usage display
    
    **Current Model:** {model}
    """.format(model=selected_model_name))
    
    st.markdown("---")
    
    # Quota information
    st.subheader("📊 API Quota Info")
    with st.expander("View Free Tier Limits"):
        st.markdown("""
        **Free Tier Limits:**
        - ⏱️ **15 requests per minute** per model
        - 📅 **1,500 requests per day** per model  
        - 🔤 **2M input tokens per minute** per model
        
        **Tips:**
        - Switch models if one hits limits
        - Wait 1 minute between heavy usage
        - Daily limits reset at midnight UTC
        """)
    
    # Quota status indicator
    if st.button("🔄 Check Quota Status", help="Check if you're near quota limits"):
        st.info("💡 Quota status checking not available in free tier. Monitor usage manually.")

# Main chat interface
st.markdown("---")

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(f'<div class="chat-message {message["role"]}-message">{message["content"]}</div>', unsafe_allow_html=True)
        
        # Display token usage if available
        if "token_usage" in message and message["token_usage"]:
            st.markdown(f'<div class="token-info">📊 Token Usage: {message["token_usage"]}</div>', unsafe_allow_html=True)

# Chat input
if prompt := st.chat_input("Ask me anything..."):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Display user message
    with st.chat_message("user"):
        st.markdown(f'<div class="chat-message user-message">{prompt}</div>', unsafe_allow_html=True)
    
    # Display assistant message with loading spinner
    with st.chat_message("assistant"):
        with st.spinner("🤔 Thinking..."):
            try:
                # Get response from model
                response, error = get_model_response(st.session_state.current_model, prompt)
                
                if error:
                    # Handle API errors
                    if error == "QUOTA_EXCEEDED":
                        quota_message = """
                        ⚠️ **API Quota Exceeded**
                        
                        You've reached the free tier limits for Google Gemini API. Here are your options:
                        
                        **🕐 Wait and Retry:**
                        - Free tier resets every minute for requests
                        - Daily limits reset at midnight UTC
                        
                        **🔄 Try a Different Model:**
                        - Switch to a lighter model like Gemma 3 1B IT
                        - Some models have different quota limits
                        
                        **💳 Upgrade (Optional):**
                        - Visit [Google AI Studio](https://aistudio.google.com/) to upgrade
                        - Higher quotas available with billing enabled
                        
                        **📊 Current Limits (Free Tier):**
                        - 15 requests per minute per model
                        - 1,500 requests per day per model
                        - 2M input tokens per minute per model
                        """
                        st.markdown(f'<div class="chat-message error-message">{quota_message}</div>', unsafe_allow_html=True)
                    else:
                        error_message = f"⚠️ Sorry, something went wrong with the API. Please try again later.\n\n**Error:** {error}"
                        st.markdown(f'<div class="chat-message error-message">{error_message}</div>', unsafe_allow_html=True)
                    
                    st.session_state.messages.append({
                        "role": "assistant", 
                        "content": quota_message if error == "QUOTA_EXCEEDED" else error_message,
                        "token_usage": None
                    })
                else:
                    # Display successful response
                    response_text = response.text
                    st.markdown(f'<div class="chat-message ai-message">{response_text}</div>', unsafe_allow_html=True)
                    
                    # Extract token usage information
                    token_usage = None
                    if hasattr(response, 'usage_metadata') and response.usage_metadata:
                        usage = response.usage_metadata
                        token_usage = f"Input: {usage.get('prompt_token_count', 'N/A')} | Output: {usage.get('candidates_token_count', 'N/A')} | Total: {usage.get('total_token_count', 'N/A')}"
                    
                    # Display token usage if available
                    if token_usage:
                        st.markdown(f'<div class="token-info">📊 Token Usage: {token_usage}</div>', unsafe_allow_html=True)
                    
                    # Add assistant message to chat history
                    st.session_state.messages.append({
                        "role": "assistant", 
                        "content": response_text,
                        "token_usage": token_usage
                    })
                    
            except Exception as e:
                # Handle unexpected errors
                error_message = f"⚠️ An unexpected error occurred. Please try again.\n\n**Error:** {str(e)}"
                st.markdown(f'<div class="chat-message error-message">{error_message}</div>', unsafe_allow_html=True)
                st.session_state.messages.append({
                    "role": "assistant", 
                    "content": error_message,
                    "token_usage": None
                })

# Footer
st.markdown("---")
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.markdown("""
    <div style="text-align: center; color: #666; font-size: 0.9rem;">
        <p>🤖 Powered by Google Gemini AI | 👨‍💻 Created by Ghulama Sarwar Khan</p>
        <p>💡 Ask me anything - I'm here to help!</p>
    </div>
    """, unsafe_allow_html=True) 