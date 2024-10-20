import streamlit as st
import google.generativeai as gen_ai

# Configure Streamlit page settings
st.set_page_config(
    page_title="Chat with Gemini",
    page_icon=":brain:",
    layout="centered"
)

# Access the Google API key from Streamlit Secrets
GOOGLE_API_KEY = st.secrets["GOOGLE_API_KEY"]

# Set up Google Gemini AI model
gen_ai.configure(api_key=GOOGLE_API_KEY)
model = gen_ai.GenerativeModel('gemini-1.5-flash')

# Function to translate roles between Gemini and Streamlit terminology
def translate_role_for_streamlit(user_role):
    if user_role == "model":
        return "assistant"
    else:
        return user_role
    
# Initialize chat session in Streamlit if not already present
if "chat_session" not in st.session_state:
    st.session_state.chat_session = model.start_chat(history=[])

# Display chatbot's title
st.title("🤖 Gemini ChatBot")
st.divider()

# Display chat history
for message in st.session_state.chat_session.history:
    with st.chat_message(translate_role_for_streamlit(message.role)):
        st.markdown(message.parts[0].text)

# Input field for user's message
user_prompt = st.chat_input("Ask Gemini...")
if user_prompt:
    # Add user's message to chat
    st.chat_message("user").markdown(user_prompt)

    # Send user's message to Gemini & get response
    gemini_response = st.session_state.chat_session.send_message(user_prompt)

    # Display Gemini's message
    with st.chat_message("assistant"):
        st.markdown(gemini_response.text)
