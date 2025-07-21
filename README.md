# GSK AI Agent - A Professional Streamlit Chat Application

This project is a sophisticated AI chat agent built with Python and Streamlit. It features a professional, clean user interface and integrates with Google's powerful Gemini and Gemma language models.

![AI Agent Screenshot](https://raw.githubusercontent.com/gsarwarkhan/ai-agent-streamlit/main/screen.jpg)

## ✨ Key Features

- **Interactive Chat Interface**: A clean, modern, and responsive UI for seamless conversations.
- **Multi-Model Support**: Easily switch between different Gemini and Gemma models (`Gemini 1.5 Pro`, `Gemini 1.5 Flash`, etc.) directly from the sidebar.
- **Professional Branding**: Features a prominent profile section for the creator, Ghulam Sarwar Khan.
- **WhatsApp Visitor Logging**: An integrated form allows visitors to submit their WhatsApp number to stay connected.
- **Google Sheets Sync**: Automatically syncs visitor contact information to a Google Sheet for easy management.
- **Robust Error Handling**: Gracefully handles API errors, configuration issues, and provides clear user feedback.
- **Polished UI/UX**: Includes an animated GIF, custom CSS for a professional look, and a responsive layout for all devices.

## 🛠️ Tech Stack

- **Framework**: Streamlit
- **Language**: Python
- **AI Models**: Google Generative AI (Gemini & Gemma)
- **Data Sync**: gspread & Google Sheets API
- **Dependencies**: `python-dotenv`, `oauth2client`

## 🚀 How to Run Locally

### 1. **Prerequisites**
- Python 3.8+
- A Google API Key with the Generative AI API enabled.
- A Google Cloud Platform project with the Google Sheets API enabled and a `service_account.json` file.

### 2. **Clone the Repository**
```bash
git clone https://github.com/gsarwarkhan/ai-agent-streamlit.git
cd ai-agent-streamlit
```

### 3. **Set up Environment**
- Create a `.env` file in the root directory and add your Google API key:
  ```
  GOOGLE_API_KEY="your_google_api_key_here"
  ```
- Place your `service_account.json` file in the root directory for Google Sheets integration.
- Add your profile picture as `GSK Profile Pic.jpeg` in the root directory.

### 4. **Install Dependencies**
```bash
pip install -r requirements.txt
```

### 5. **Run the App**
```bash
streamlit run app.py
```
The application will be available at `http://localhost:8501`.

## ☁️ Deployment

This application is ready to be deployed on [Streamlit Community Cloud](https://streamlit.io/cloud).

1.  Push your code to your GitHub repository.
2.  Connect your GitHub to Streamlit Cloud.
3.  Deploy the app.
4.  **Important**: Add your `GOOGLE_API_KEY` and the contents of your `service_account.json` as secrets in your Streamlit Cloud app settings.

---

**Developed by Ghulam Sarwar Khan**
- [LinkedIn](https://www.linkedin.com/in/gsarwarkhan/)
- [Facebook](https://www.facebook.com/gsarwarkhan)
- [GitHub](https://github.com/gsarwarkhan)
