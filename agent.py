import os
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables from .env (explicit path for reliability)
dotenv_path = os.path.join(os.getcwd(), '.env')
load_dotenv(dotenv_path=dotenv_path)

api_key = os.getenv("GOOGLE_API_KEY")

if not api_key:
    print("❌ ERROR: API key not found in .env file.")
    exit()

# Configure Gemini API
genai.configure(api_key=api_key)

# Define free generative models and their descriptions
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

# Features/help text
HELP_TEXT = '''\nFeatures:\n- Chat with Gemini or Gemma models\n- Switch models at any time with: /model\n- List available models: /models\n- Show this help: /help\n- Exit: exit\n'''

def print_models():
    print("\nAvailable models:")
    for idx, m in enumerate(MODELS, 1):
        print(f"  {idx}. {m['desc']}  (id: {m['name']})")
    print()

def select_model():
    print_models()
    while True:
        choice = input("Select model number: ").strip()
        if choice.isdigit() and 1 <= int(choice) <= len(MODELS):
            return MODELS[int(choice)-1]['name']
        else:
            print("Invalid choice. Please enter a number from the list.")

# Start with Gemma 3 4B IT as default model
current_model_name = 'models/gemma-3-4b-it'
model = genai.GenerativeModel(current_model_name)
print(f"🔮 Gemini Agent Ready. Using: {current_model_name}\nType '/help' for features, '/model' to switch models, or 'exit' to quit.")

while True:
    prompt = input("You: ").strip()
    if prompt.lower() == "exit":
        print("👋 Exiting Gemini Agent. Goodbye!")
        break
    elif prompt.lower() == "/help":
        print(HELP_TEXT)
        continue
    elif prompt.lower() == "/models":
        print_models()
        continue
    elif prompt.lower() == "/model":
        new_model_name = select_model()
        model = genai.GenerativeModel(new_model_name)
        current_model_name = new_model_name
        print(f"✅ Switched to: {current_model_name}")
        continue
    try:
        response = model.generate_content(prompt)
        print("Gemini:", response.text)
    except Exception as e:
        print("❌ Error:", e)
