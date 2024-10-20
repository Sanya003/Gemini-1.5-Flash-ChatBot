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
    with st.chat_message(translate_role_for_streamlit(message['author'])):
        st.markdown(message['content'])

# User input section
if prompt := st.chat_input("Say something..."):
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Add user input to the chat history
    st.session_state.chat_session.history.append({'author': 'user', 'content': prompt})
    
    # Get the model's response
    with st.chat_message("assistant"):
        response = st.session_state.chat_session.message(prompt)
        st.markdown(response['content'])
        
    # Add model's response to the chat history
    st.session_state.chat_session.history.append({'author': 'model', 'content': response['content']})
